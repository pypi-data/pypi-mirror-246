import os
from pathlib import Path

import typer
from rich import print
from typing_extensions import Annotated

from anylearn.cli._utils import HostOption
from anylearn.sdk.artifacts.dataset import DatasetArtifact
from anylearn.sdk.artifacts.model import ModelArtifact
from anylearn.sdk.auth import authenticate
from anylearn.sdk.context import init
from anylearn.sdk.errors import (
    AnylearnArtifactDuplicationError,
    AnylearnInvalidResponseError,
)
from anylearn.sdk.jumps.channel import JumpsChannel
from anylearn.sdk.jumps.uploader import JumpsUploader


app = typer.Typer()


@app.command()
def dataset(
    name: Annotated[str, typer.Argument(
        help="The name of the dataset to create.",
    )],
    path: Annotated[Path, typer.Argument(
        help="The local path (file or directory) of the dataset to upload.",
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    )],
    compress: Annotated[bool, typer.Option(
        help="Compress data during transfer (ex. rsync -z).",
    )] = True,
    host: str = HostOption,
):
    init(host)
    authenticate(host)
    dataset = _create_dataset(name=name)
    _upload_via_jumps_channel(
        artifact_id=dataset.id,
        path=path,
        compress=compress,
    )
    print("[green]Upload OK[/green]")


@app.command()
def model(
    name: Annotated[str, typer.Argument(
        help="The name of the model to create.",
    )],
    path: Annotated[Path, typer.Argument(
        help="The local path (file or directory) of the model to upload.",
        exists=True,
        file_okay=True,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    )],
    compress: Annotated[bool, typer.Option(
        help="Compress data during transfer (ex. rsync -z).",
    )] = True,
    host: str = HostOption,
):
    init(host)
    authenticate(host)
    model = _create_model(name=name)
    _upload_via_jumps_channel(
        artifact_id=model.id,
        path=path,
        compress=compress,
    )
    print("[green]Upload OK[/green]")


def _create_dataset(name: str) -> DatasetArtifact:
    try:
        print(f"Creating dataset {name}...")
        return DatasetArtifact.create(name=name)
    except AnylearnArtifactDuplicationError:
        print(f"Dataset {name} already exists in your namespace.")
        raise typer.Abort()
    except AnylearnInvalidResponseError:
        print(f"Failed to create dataset {name}.")
        raise typer.Abort()
    except Exception as e:
        print(f"An error occurred during dataset creation: {e}")
        raise typer.Abort()


def _create_model(name: str) -> ModelArtifact:
    try:
        print(f"Creating model {name}...")
        return ModelArtifact.create(name=name)
    except AnylearnArtifactDuplicationError:
        print(f"Model {name} already exists in your namespace.")
        raise typer.Abort()
    except AnylearnInvalidResponseError:
        print(f"Failed to create model {name}.")
        raise typer.Abort()
    except Exception as e:
        print(f"An error occurred during model creation: {e}")
        raise typer.Abort()


def _upload_via_jumps_channel(
    artifact_id: str,
    path: os.PathLike,
    compress: bool,
) -> None:
    try:
        print("Creating jump server channel...")
        jc = JumpsChannel.create(
            artifact_id=artifact_id,
            artifact_local_path=path,
        )
    except FileNotFoundError:
        print(f"Local path {path} not found.")
        raise typer.Abort()
    except AnylearnInvalidResponseError:
        print("Failed to create jumps channel.")
        raise typer.Abort()
    except Exception as e:
        print(f"An error occurred during jumps upload: {e}")
        raise typer.Abort()
    print(f"Uploading {path} to jump server...")
    uploader = JumpsUploader(
        channel=jc,
        local_path=path,
        compress=compress,
    )
    if uploader.upload() != 0:
        print("[red]Upload Failed (jump)[/red]")
        raise typer.Abort()
    print("Transforming into Anylearn asset...")
    if not jc.transform():
        print("[red]Upload Failed (transform)[/red]")
        raise typer.Abort()
    jc.finish()
