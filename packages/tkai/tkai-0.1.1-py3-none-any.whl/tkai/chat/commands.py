import typer

app = typer.Typer()

@app.command()
def sub_command1():
    typer.echo("Executing sub command 1")

@app.command()
def sub_command2():
    typer.echo("Executing sub command 2")

