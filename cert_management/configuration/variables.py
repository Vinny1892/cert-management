from decouple import Config, RepositoryEmpty


class Configuration:
    @classmethod
    def get(cls, var):
        config = Config(RepositoryEmpty())
        try:
          return config(var)
        except Exception:
            return None


__all__ = ['Configuration']