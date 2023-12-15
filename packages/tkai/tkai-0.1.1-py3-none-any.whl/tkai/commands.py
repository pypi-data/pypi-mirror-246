import os
import typer
from tinydb import TinyDB
from typing import Optional
from datetime import datetime
from tkai.chat.commands import app as chat_app

app = typer.Typer()

@app.callback()
def main_callback():
    ctx = typer.get_current_context()

    if not output:
        # Use the invoked sub-command name as the default filename.
        command_name = ctx.invoked_subcommand
        if command_name:
            output = f"{command_name}.json"
        else:
            typer.echo("No command specified. Exiting.", err=True)
            raise typer.Exit(code=1)

    db_path = os.path.join(os.getcwd(), ")
    ctx.db = TinyDB(db_path)

app.add_typer(chat_app, name="chat")

