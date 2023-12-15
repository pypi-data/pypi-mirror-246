import ssl
import uuid
import asyncio
import traceback
import urllib.parse
from logging import critical as log


class Server():
    async def _handler(self, reader, writer):
        peer = None
        count = 1

        while True:
            try:
                peer = writer.get_extra_info('socket').getpeername()
                ctx = dict(ip=peer[0])

                cert = writer.get_extra_info('peercert')
                subject = str(uuid.UUID(cert['subject'][0][0][1]))
                ip_list = [y for x, y in cert['subjectAltName']
                           if 'IP Address' == x]

                if peer[0] in ip_list:
                    ctx['subject'] = subject
            except Exception:
                pass

            try:
                line = await reader.readline()
                p = line.decode().split()[1].strip('/').split('/')

                method = p[0]
                params = {k.lower(): urllib.parse.unquote(v)
                          for k, v in zip(p[1::2], p[2::2])}

                length = 0
                while True:
                    line = await reader.readline()
                    line = line.strip()
                    if not line:
                        break
                    k, v = line.decode().split(':', maxsplit=1)
                    if 'content-length' == k.strip().lower():
                        length = int(v.strip())

                if length > 0:
                    params['octets'] = await reader.readexactly(length)
                    if length != len(params['octets']):
                        raise Exception('TRUNCATED_MSG_BODY')
            except Exception:
                return writer.close()

            try:
                octets = await self.methods[method](ctx, **params)
                if type(octets) is not bytes:
                    raise Exception(f'INVALID_RESPONSE_TYPE - {type(octets)}')
                status = '200 OK'
            except Exception:
                traceback.print_exc()
                octets = traceback.format_exc().encode()
                status = '500 Internal Server Error'

            try:
                writer.write(f'HTTP/1.1 {status}\n'.encode())
                writer.write('content-type: text/html\n'.encode())
                writer.write(f'content-length: {len(octets)}\n\n'.encode())
                writer.write(octets)
                await writer.drain()
            except Exception:
                return writer.close()

            params.pop('octets', None)
            log(f'{peer} {count} {method} {status} {params} {len(octets)}')
            count += 1

    async def run(self, cacert, cert, port, methods):
        self.methods = methods

        ctx = ssl.create_default_context(
            cafile=cacert, purpose=ssl.Purpose.CLIENT_AUTH)
        ctx.load_cert_chain(cert, cert)
        ctx.verify_mode = ssl.CERT_OPTIONAL
        ctx.check_hostname = True

        srv = await asyncio.start_server(self._handler, None, port, ssl=ctx)
        async with srv:
            return await srv.serve_forever()


def run(cacert, cert, port, handlers):
    asyncio.run(Server().run(cacert, cert, port, handlers))


class Client():
    def __init__(self, cacert, cert, servers):
        servers = [s.split(':') for s in servers.split(',')]

        self.SSL = ssl.create_default_context(
            cafile=cacert, purpose=ssl.Purpose.SERVER_AUTH)
        self.SSL.load_cert_chain(cert, cert)
        self.SSL.verify_mode = ssl.CERT_REQUIRED
        self.SSL.check_hostname = True

        self.conns = {(ip, int(port)): (None, None) for ip, port in servers}
        self.quorum = int(len(self.conns)/2) + 1

    async def server(self, server, resource, octets=b''):
        status = None

        try:
            if self.conns[server][0] is None or self.conns[server][1] is None:
                self.conns[server] = await asyncio.open_connection(
                    server[0], server[1], ssl=self.SSL)

            reader, writer = self.conns[server]

            writer.write(f'POST {resource} HTTP/1.1\n'.encode())
            writer.write(f'content-length: {len(octets)}\n\n'.encode())
            writer.write(octets)
            await writer.drain()

            status = await reader.readline()

            while True:
                line = await reader.readline()
                line = line.strip()
                if not line:
                    break
                k, v = line.decode().split(':', maxsplit=1)
                if 'content-length' == k.strip().lower():
                    length = int(v.strip())

            octets = await reader.readexactly(length)
            if length != len(octets):
                raise Exception('TRUNCATED_MSG_BODY')

            if status.startswith(b'HTTP/1.1 200 OK'):
                return octets

            raise Exception(octets.decode())
        except Exception:
            if self.conns[server][1] is not None:
                self.conns[server][1].close()

            self.conns[server] = None, None
            raise

    async def cluster(self, resource, octets=b''):
        servers = self.conns.keys()

        return await asyncio.gather(
            *[self.server(s, resource, octets) for s in servers],
            return_exceptions=True)

    def __del__(self):
        for server, (reader, writer) in self.conns.items():
            try:
                writer.close()
            except Exception:
                pass
