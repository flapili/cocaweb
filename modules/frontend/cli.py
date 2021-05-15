# coding: utf-8
import subprocess
import shutil
from typing import List
from pathlib import Path


import typer

from modularapi.utils import _on_rmtree_error

cli = typer.Typer()


cli_yarn = typer.Typer(name="yarn")
cli.add_typer(cli_yarn)

cwd = Path(__file__).resolve().parent / "src"


@cli_yarn.command(name="dev")
def cli_yarn_dev(port: int = typer.Option(8080, "--port", "-p")):
    subprocess.run(["yarn", "dev", "-p", str(port)], check=True, cwd=cwd)


@cli_yarn.command(name="build")
def cli_yarn_build(
    analyze: bool = typer.Option(False, "--analyze", "-a", help="analyse webpack bundle",),
):
    args = ["yarn", "build"]
    if analyze is True:
        args.append("--analyze")
    subprocess.run(args, check=True, cwd=cwd)


@cli_yarn.command(name="add")
def cli_yarn_add(packages: List[str] = typer.Argument(..., help="Packages to install")):
    subprocess.run(["yarn", "add", *packages], check=True, cwd=cwd)


cli_purge = typer.Typer(name="purge")
cli.add_typer(cli_purge)


@cli_purge.command(name="cache")
def cli_purge_cache():
    shutil.rmtree(cwd / "node_modules" / ".cache", onerror=_on_rmtree_error)
