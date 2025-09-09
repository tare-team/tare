"""Tare command line interface."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import List

import typer

app = typer.Typer(help="Utilities for developing Tare")


def _spawn(cmd: List[str], cwd: Path | None = None) -> subprocess.Popen:
    """Spawn a subprocess inheriting STDIO."""
    return subprocess.Popen(cmd, cwd=cwd)


@app.command()
def dev() -> None:
    """Start the local development environment.

    This command boots supporting services via Docker, then starts the
    GraphQL API server and the React development server. Processes run until
    interrupted with CTRL+C.
    """

    repo_root = Path(__file__).resolve().parents[2]
    ui_path = repo_root / "js_modules" / "tare-ui"

    typer.echo("Starting Docker services...")
    subprocess.run(["docker", "compose", "up", "-d"], cwd=repo_root, check=False)

    typer.echo("Installing UI dependencies...")
    subprocess.run(["npm", "install"], cwd=ui_path, check=False)

    typer.echo("Starting GraphQL API server...")
    api_proc = _spawn(
        [
            "uv",
            "run",
            "--package",
            "tare-graphql",
            "uvicorn",
            "tare_graphql.main:app",
            "--reload",
        ],
        cwd=repo_root,
    )

    typer.echo("Starting UI dev server...")
    ui_proc = _spawn(["npm", "run", "dev"], cwd=ui_path)

    processes = [api_proc, ui_proc]

    try:
        for proc in processes:
            proc.wait()
    except KeyboardInterrupt:
        pass
    finally:
        for proc in processes:
            if proc.poll() is None:
                proc.terminate()

        typer.echo("Shutting down Docker services...")
        subprocess.run(
            ["docker", "compose", "down"], cwd=repo_root, check=False
        )

