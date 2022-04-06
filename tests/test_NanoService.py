from pysj.nanoservice import NanoService, NanoServiceClient

if __name__ == "__main__":
    client = NanoServiceClient()
    result = client.double("y0")
    print(result)
