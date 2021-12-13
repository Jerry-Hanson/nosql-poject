class ConnectedSockPool:
    def __init__(self):
        self.pool = list()

    def getSocket(self, username):
        for value in self.pool:
            if value['username'] == username:
                return value['clientsock']
        return None

    def add(self, ip, port, username, clientsock):
        self.pool.append({"ip": ip, "port": port, "username": username, "clientsock": clientsock})

    def has(self, user_ip, user_port):
        for i, item in enumerate(self.pool):
            print(item)
            if item['ip'] == user_ip and item['port'] == user_port:
                return True
        return False

    def isAlive(self, username):
        for value in self.pool:
            if value['username'] == username:
                return True
        return False

    def delSocket(self, user_ip, user_port):
        for i, item in enumerate(self.pool):
            if item['ip'] == user_ip and item['port'] == user_port:
                del self.pool[i]
                break
