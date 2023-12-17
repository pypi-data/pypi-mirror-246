import typer

app = typer.Typer()

@app.command()
def me():
    print("Hi!")
    print("Welcome to tlylt utility scripts!")

@app.command()
def git():
    print("git utility scripts")


if __name__ == "__main__":
    app()