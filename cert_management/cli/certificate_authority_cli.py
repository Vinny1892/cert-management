from typer import Typer, Argument

app = Typer()

@app.command()
def create(
        path: str = Argument('', help="Path to the certificate file"),
):
    print("create ca")