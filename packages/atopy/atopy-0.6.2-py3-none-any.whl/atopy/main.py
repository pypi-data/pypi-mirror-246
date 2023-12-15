from loguru import logger

from atopy.typer import typer

app = typer()


@app.command()
def debug(s: str) -> None:
    logger.debug(s)


if __name__ == "__main__":
    app()
