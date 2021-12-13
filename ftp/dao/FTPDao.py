from ftplib import FTP
import os


class FTPDao:

    def __init__(self, ip, port, username, password):
        self.ftp = FTP()
        self.ftp.connect(ip, port)
        self.ftp.login(username, password)

    def upload(self, local_file, remote_file, remote_file_folder = None):
        if remote_file_folder is not None:
            if remote_file_folder not in self.ftp.nlst():
                self.ftp.mkd(remote_file_folder)
            self.ftp.cwd(remote_file_folder)
        with open(local_file, "rb") as file_handler:
            self.ftp.storbinary("STOR " + remote_file, file_handler, 2048)

        # 返回根目录
        self.ftp.cwd('/')

    def download(self, localpath, filename, remote_file_path = None):
        new_file_path = os.path.join(localpath, filename)
        if remote_file_path is not None:
            self.ftp.cwd(remote_file_path)

        file_handler = open(new_file_path, 'wb').write
        self.ftp.retrbinary("RETR {}".format(filename), file_handler, 1024)

        # 返回根目录
        self.ftp.cwd('/')

    def getFiles(self, remote_file_dir = None):
        if remote_file_dir is not None:
            self.ftp.cwd(remote_file_dir)
        file_list = self.ftp.nlst()

        self.ftp.cwd('/')

        return file_list

    def mkdir(self, dir_name):
        self.ftp.mkd(dir_name)

if __name__ == "__main__":
    dao = FTPDao('localhost', 21, 'Jerry', '123')
    dao.download("C:/Users/Administrator/Desktop/", "1.png", "hurry")