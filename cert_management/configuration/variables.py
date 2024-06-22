from decouple import Config, RepositoryEmpty


class Configuration:

    @classmethod
    def get(cls, var):
        config = Config(RepositoryEmpty())
        return config(var)