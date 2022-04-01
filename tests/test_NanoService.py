from pysj.nanoservice import NanoService, NanoServiceClient

if __name__ == "__main__":
    client = NanoServiceClient()
    client.echo("y0")
    # client.query("hei", lo="ke")
