import typer

def save_output(ctx: typer.Context, command_name: str, data: str):
    """
    Utility function to either write to the TinyDB database or echo the data.
    Includes a timestamp for when the record is created.
    """
    timestamp = datetime.now().isoformat()
    record = {'command': command_name, 'data': data, 'timestamp': timestamp}

    if ctx.db:
        ctx.db.insert(record)
        typer.echo(f"Data written to TinyDB: {record}")
    else:
        typer.echo(f"Output: {record}")


