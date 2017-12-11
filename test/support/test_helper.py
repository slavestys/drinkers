from application import Application

Application.init()


class CleanUp:
    @staticmethod
    def clean_up():
        Application.redis.flushdb()