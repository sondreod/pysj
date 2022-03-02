from pysj.main import MiniService, MiniServiceClient


service = MiniService()


@service.endpoint()
def func(lol):
    return lol


print(func("lol"))
service.start()
