from pysj.main import MiniService, MiniServiceClient

service = MiniService()


@service.endpoint()
def func(*args, **kwargs):
    return args, kwargs


print(func("lol", lolz="kek"))
service.start()
