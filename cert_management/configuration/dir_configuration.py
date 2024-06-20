import os

# TODO: pegar via variavel de ambiente ou arquivo de configuração ou parametro de cli
base_dir = "/tmp/test_ca"


class DirConfiguration:
    def __init__(self):
        self.dirs = {
            "certs": os.path.join(base_dir, "certs"),
            "newcerts": os.path.join(base_dir, "newcerts"),
            "private": os.path.join(base_dir, "private"),
            "csr": os.path.join(base_dir, "csr"),
            "crl": os.path.join(base_dir, "crl"),
        }

    def get_dir(self):
        return self.dirs

    def create_dirs(self):
        for path in self.dirs.values():
            if not os.path.exists(path):
                os.makedirs(path)
