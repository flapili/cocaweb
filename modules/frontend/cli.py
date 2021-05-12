# coding: utf-8
import subprocess
from pathlib import Path

import typer

cli = typer.Typer()


@cli.command()
def dev(port: int = typer.Option(8080, "--port", "-p")):
    cwd = Path(__file__).resolve().parent / "src"
    subprocess.run(["yarn", "dev", "-p", str(port)], check=True, cwd=cwd)


@cli.command()
def build():
    cwd = Path(__file__).resolve().parent / "src"
    subprocess.run(["yarn", "build"], check=True, cwd=cwd)
