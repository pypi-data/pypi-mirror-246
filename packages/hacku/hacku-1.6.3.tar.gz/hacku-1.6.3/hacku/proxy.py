# coding=utf-8

import asyncio
import pickle
import random
import socket
import struct
import sys
import time
from socketserver import StreamRequestHandler, ThreadingTCPServer

import httpx
import select
import socks
from loguru import logger

SOCKS_VERSION = 5


class SocksProxy(StreamRequestHandler):
    username = ''
    password = ''

    def handle(self):
        address = bind_address = remote = None
        """
        一、客户端认证请求
            +----+----------+----------+
            |VER | NMETHODS | METHODS  |
            +----+----------+----------+
            | 1  |    1     |  1~255   |
            +----+----------+----------+
        """
        # 从客户端读取并解包两个字节的数据
        header = self.connection.recv(2)
        ver, nmethods = struct.unpack("!BB", header)
        # 设置socks5协议，METHODS字段的数目大于0
        assert ver == SOCKS_VERSION, 'SOCKS版本错误'
        # 接受支持的方法
        # 无需认证：0x00    用户名密码认证：0x02
        # assert NMETHODS > 0
        methods = self.is_available(nmethods)
        # 检查是否支持该方式，不支持则断开连接
        """ 
        二、服务端回应认证
            +----+--------+
            |VER | METHOD |
            +----+--------+
            | 1  |   1    |
            +----+--------+
        """
        # 发送协商响应数据包 
        if self.username != '' and self.password != '':
            if 2 not in set(methods):
                logger.warning(f'[-] 客户端:  {self.client_address}  无账密信息，无法与客户端验证-已挂断连接')
                self.server.close_request(self.request)
                return
            self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 2))
            if not self.verify_auth():
                return
        elif self.username == '' and self.password == '':
            if 0 not in set(methods):
                self.server.close_request(self.request)
                return
            self.connection.sendall(struct.pack("!BB", SOCKS_VERSION, 0))
        """
        三、客户端连接请求(连接目的网络)
            +----+-----+-------+------+----------+----------+
            |VER | CMD |  RSV  | ATYP | DST.ADDR | DST.PORT |
            +----+-----+-------+------+----------+----------+
            | 1  |  1  |   1   |  1   | Variable |    2     |
            +----+-----+-------+------+----------+----------+
        """
        version, cmd, _, address_type = struct.unpack("!BBBB", self.connection.recv(4))
        assert version == SOCKS_VERSION, 'socks版本错误'
        if address_type == 1:  # IPv4
            # 转换IPV4地址字符串（xxx.xxx.xxx.xxx）成为32位打包的二进制格式（长度为4个字节的二进制字符串）
            address = socket.inet_ntoa(self.connection.recv(4))
        elif address_type == 3:  # Domain
            domain_length = ord(self.connection.recv(1))
            address = self.connection.recv(domain_length).decode()
        port = struct.unpack('!H', self.connection.recv(2))[0]
        """
        四、服务端回应连接
            +----+-----+-------+------+----------+----------+
            |VER | REP |  RSV  | ATYP | BND.ADDR | BND.PORT |
            +----+-----+-------+------+----------+----------+
            | 1  |  1  |   1   |  1   | Variable |    2     |
            +----+-----+-------+------+----------+----------+
        """
        # 响应，只支持CONNECT请求
        # 校验用户名和密码
        try:
            if cmd == 1:  # CONNECT
                remote = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                remote.connect((address, port))
                bind_address = remote.getsockname()
                p = socks.getdefaultproxy()
                logger.info(f'[+] 客户端:  {self.client_address}  已建立连接: {address, str(port)} 代理服务器: {":".join([p[1], str(p[2])])}')
            else:
                self.server.close_request(self.request)
            addr = struct.unpack("!I", socket.inet_aton(bind_address[0]))[0]
            port = bind_address[1]
            reply = struct.pack("!BBBBIH", SOCKS_VERSION, 0, 0, address_type, addr, port)
        except Exception as err:
            logger.error(f'[-] 客户端:  {self.client_address} 连接: {address, str(port)}  发生错误: {err}')
            # 响应拒绝连接的错误
            reply = struct.pack("!BBBBIH", SOCKS_VERSION, 5, 0, address_type, 0, 0)
        self.connection.sendall(reply)  # 发送回复包
        # 建立连接成功，开始交换数据
        if reply[1] == 0 and cmd == 1:
            self.exchange_data(self.connection, remote)
        self.server.close_request(self.request)

    def is_available(self, n):
        """ 
        检查是否支持该验证方式 
        """
        methods = []
        for i in range(n):
            methods.append(ord(self.connection.recv(1)))
        return methods

    def verify_auth(self):
        """
        校验用户名和密码
        """
        version = ord(self.connection.recv(1))
        assert version == 1
        username_len = ord(self.connection.recv(1))
        username = self.connection.recv(username_len).decode('utf-8')
        password_len = ord(self.connection.recv(1))
        password = self.connection.recv(password_len).decode('utf-8')
        if username == self.username and password == self.password:
            # 验证成功, status = 0
            response = struct.pack("!BB", version, 0)
            self.connection.sendall(response)
            return True
        # 验证失败, status != 0
        logger.warning(f"[-] 客户端:  {self.client_address}  密码验证错误 已断开连接!")
        response = struct.pack("!BB", version, 0xFF)
        self.connection.sendall(response)
        self.server.close_request(self.request)
        return False

    def exchange_data(self, client, remote):
        """ 
        交换数据 
        """
        while True:
            # 等待数据
            try:
                rs, ws, es = select.select([client, remote], [], [])
                if client in rs:
                    data = client.recv(4096)
                    if remote.send(data) <= 0:
                        break
                if remote in rs:
                    data = remote.recv(4096)
                    if client.send(data) <= 0:
                        break
            except Exception as err:
                logger.error(f'客户端:  {self.client_address}  发生错误: {err}')
                pass


class ProxyPool:
    def __init__(self, nodes: list, rotate=5, detect=30 * 60, check_url="http://checkip.amazonaws.com", proxy_timeout=5, proxy_file='proxy.p'):
        if 'linux' not in sys.platform:
            raise Exception("因为httpx的socks代理问题，目前代理池模块只支持linux平台")
        # assert ((username and password) or (not username and not password))
        # 用list实现FIFO队列
        self.nodes = nodes
        random.shuffle(self.nodes)
        self.detect_interval = detect
        self.rotate_interval = rotate
        self.check_url = check_url
        self.proxy_timeout = proxy_timeout
        self.proxy_file = proxy_file
        # SocksProxy.username = username
        # SocksProxy.password = password

    async def health_check(self):
        to_check = set(self.nodes)
        logger.debug(to_check)
        for n in to_check:
            try:
                async with httpx.AsyncClient(proxies=httpx.Proxy(n), timeout=self.proxy_timeout) as client:
                    resp = await client.get(self.check_url)
                    logger.debug(resp.text)
                    if resp.status_code == 200:
                        continue
            except:
                pass
            while n in self.nodes:
                self.nodes.remove(n)

        with open("proxy.p", "wb") as f:
            pickle.dump(set(self.nodes), f)

    async def set_proxy(self):
        t1 = time.perf_counter()
        while True:
            t2 = time.perf_counter()
            if self.detect_interval != 0 and t2 - t1 >= self.detect_interval:
                await self.health_check()

            if len(self.nodes) == 0:
                raise Exception("没有可用节点了")

            node = self.nodes.pop(0)
            if not node:
                raise Exception("没有可用节点了")
            logger.debug(node)

            try:
                if "@" in node:
                    user_pass = node.split('@')[0].split('://')[1]
                    addr, port = node.split('@')[1].split(':')
                    username, password = user_pass.split(':')
                else:
                    addr, port = node.split('://')[1].split(':')
                    username = password = ''

                # 设置代理
                socks.set_default_proxy(socks.SOCKS5, addr, int(port), rdns=True, username=username, password=password)
                socket.socket = socks.socksocket
                logger.warning(f'服务端当前代理服务器为：{addr}:{port}, 剩余可用节点: {len(set(self.nodes))}')

                time.sleep(self.rotate_interval)
                # 切换时把当前的节点放到队列最后
                self.nodes.append(node)
            except Exception as e:
                logger.error(f'代理服务器超时: {str(e)}')
                pass


def main():
    import argparse

    parser = argparse.ArgumentParser(description='socks5代理池')
    parser.add_argument('-p', type=int, help='指定socks服务监听端口', default=18000)
    parser.add_argument('-r', type=int, help='代理轮换的间隔时间（单位：秒）', default=5)
    parser.add_argument('-d', type=int, help='代理健康检查的间隔时间（单位：分钟）', default=30)
    parser.add_argument('-u', type=str, help='用于测试连通性的URL', default="http://checkip.amazonaws.com")
    parser.add_argument('-t', type=int, help='上游代理连接的超时时间（单位：秒）', default=5)
    parser.add_argument('-i', type=str, help='需导入的代理节点文件路径', default='node.list')
    parser.add_argument('-s', type=str, help='可用代理节点存储文件路径', default='proxy.p')
    args = parser.parse_args()

    async def func(loop, args):
        all_nodes = set()
        try:
            with open(args.s, 'rb') as f:
                all_nodes = pickle.load(f)
        except:
            pass

        server = ThreadingTCPServer(('0.0.0.0', args.p), SocksProxy)
        try:
            if not all_nodes:
                logger.info('获取节点中...... ')
                with open(args.i, 'r', encoding='utf-8') as f:
                    for line in f:
                        if line.startswith("socks5://"):
                            all_nodes.add(line.split('#')[0].strip())
            logger.debug(all_nodes)
            pool = ProxyPool(list(all_nodes), rotate=args.r, detect=args.d, check_url=args.u, proxy_timeout=args.t, proxy_file=args.s)
            await pool.health_check()
            logger.info(f'节点获取完毕！当前可用节点数量：{len(pool.nodes)}，每{pool.detect_interval / 60}分钟检测可用的节点')
            server_task = loop.run_in_executor(None, server.serve_forever)
            check_task = loop.create_task(pool.set_proxy())
            # 等待服务器完成
            await asyncio.gather(server_task, check_task)
        except Exception as e:
            logger.error(e)
            server.shutdown()
            loop.stop()

    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(func(loop, args))
    finally:
        loop.run_until_complete(loop.shutdown_asyncgens())
        loop.close()


if __name__ == '__main__':
    main()
