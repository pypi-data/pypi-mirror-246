# flake8: noqa: B008

import datetime
import logging
import os
from pathlib import Path

import boto3
import typer
from dateutil.parser import parse
from PIL import Image
from pillow_heif import register_heif_opener

_log = logging.getLogger(__name__)

__version__ = "2.3.0"

register_heif_opener()  # register PILLOW plugin

app = typer.Typer(name="twlib")


@app.command()
def snake_say(
    message: str,
):
    # message = " ".join(sys.argv[1:])
    bubble_length = len(message) + 2
    print(
        rf"""
           {"_" * bubble_length}
          ( {message} )
           {"‾" * bubble_length}
            \
             \    __
              \  [oo]
                 (__)\
                   λ \\
                     _\\__
                    (_____)_
                   (________)Oo°"""
    )


@app.command()
def epoch2dt(
    epoch: int = typer.Argument(..., help="epoch in ms"),
    to_local: bool = typer.Option(False, "-l", "--local", help="In local time"),
):
    """Convert epoch in ms (UTC) to datetime (local or UTC)"""
    if to_local:
        dt = datetime.datetime.fromtimestamp(epoch / 1000).strftime("%Y-%m-%d %H:%M:%S")
    else:
        dt = datetime.datetime.utcfromtimestamp(epoch / 1000).strftime(
            "%Y-%m-%d %H:%M:%S"
        )

    typer.echo(dt)


@app.command()
def dt2epoch(
    dt: str = typer.Argument(..., help="datetime string in '%Y-%m-%d %H:%M:%S'"),
    is_local: bool = typer.Option(
        False, "-l", "--local", help="Input is given in local time"
    ),
):
    """Convert naive local datetime (local or UTC) string to epoch in ms (UTC)"""
    if is_local:
        # https://stackoverflow.com/a/39079819
        LOCAL_TIMEZONE = datetime.datetime.now().astimezone().tzinfo

        dt_parsed = parse(dt)  # get naive dt
        dt_parsed = dt_parsed.replace(tzinfo=LOCAL_TIMEZONE)  # localize naive dt
    else:
        dt_parsed = parse(dt)
        dt_parsed = dt_parsed.replace(tzinfo=datetime.timezone.utc)

    epoch = int(dt_parsed.timestamp() * 1000)
    typer.echo(epoch)


@app.command()
def heic2img(input_file: str, *, mode="jpg", out_file: str = None) -> None:
    """
    An HEIC file is a space-saving image format that uses High Efficiency Video Coding (HEVC)
    to compress and store images across your devices.
    Because Apple regularly uses HEIC files, you can easily open them on your Mac with Preview or Photoshop
    """
    _heic2img(input_file=input_file, mode=mode, out_file=out_file)
    typer.secho("Saved {out_file}", fg=typer.colors.GREEN, bold=False)


def _heic2img(input_file: str, mode: str, out_file: str | None) -> None:
    with Image.open(input_file) as img:
        print(
            f"{img.mode=}, {img.size=}, {img.format=}, {img.info.keys()=}, {img.getbands()=}"
        )

        if mode == "jpg":
            if out_file is None:
                out_file = Path(input_file).with_suffix(".jpg")
            Path(out_file).unlink(missing_ok=True)
            Path(out_file).parent.mkdir(parents=True, exist_ok=True)
            img.save(out_file, "JPEG")

        elif mode == "png":
            if out_file is None:
                out_file = Path(input_file).with_suffix(".png")
            Path(out_file).unlink(missing_ok=True)
            Path(out_file).parent.mkdir(parents=True, exist_ok=True)
            img.save(out_file, "PNG")
        else:
            raise ValueError(f"Unknown type {mode}")


@app.command()
def relative(source: str, target: str) -> Path:
    """Calculate the relative path from source dir to target file."""
    if not Path(source).is_dir():
        typer.secho(
            f"Source must be a directory: {source}", fg=typer.colors.RED, bold=True
        )
        raise typer.Abort()
    source_path = Path(source)
    target_path = Path(target).parent

    if not (source_path.is_absolute() and target_path.is_absolute()):
        raise ValueError("Both source and target must be absolute paths")

    name = Path(
        target
    ).name  # Gotcha: source_path.name is not the same as target_path.name
    rel_path = os.path.relpath(target_path, source_path)
    typer.echo(Path(rel_path) / name)
    return Path(rel_path) / name


@app.command()
def sqs_purge(
    queue_url: str = typer.Option(None, "-q", "--queue-url", help="Queue URL"),
) -> None:
    session = boto3.Session()
    sqs = session.client("sqs")

    if queue_url is None:
        queue_url = sqs_choice(sqs)
    if not queue_url.startswith("https://"):
        typer.secho(f"Invalid queue URL: {queue_url}", fg=typer.colors.RED, bold=True)
        raise typer.Exit(1)

    # Purge the SQS queue
    response = sqs.purge_queue(QueueUrl=queue_url)

    if response["ResponseMetadata"]["HTTPStatusCode"] == 200:
        typer.echo(f"The queue {queue_url} has been purged.")
    else:
        typer.echo("Failed to purge the queue.")


@app.command()
def sqs(
    n_messages: int = typer.Option(3, "-n", "--n-messages", help="Number of messages"),
    visibility_timeout: int = typer.Option(
        0, "-t", "--visibility-timeout", help="Visibility timeout"
    ),
) -> None:
    session = boto3.Session()
    sqs = session.client("sqs")
    queue_url = sqs_choice(sqs)

    # Get the approximate number of messages in the selected queue
    response = sqs.get_queue_attributes(
        QueueUrl=queue_url, AttributeNames=["ApproximateNumberOfMessages"]
    )
    message_count = response["Attributes"]["ApproximateNumberOfMessages"]

    typer.echo(f"Approximate number of messages in the selected queue: {message_count}")

    if int(message_count) == 0:
        raise typer.Exit()

    response = sqs.receive_message(
        QueueUrl=queue_url,
        AttributeNames=["All"],
        MaxNumberOfMessages=n_messages,
        VisibilityTimeout=visibility_timeout,
    )

    messages = response.get("Messages", [])

    if messages:
        typer.echo(f"Last {len(messages)} messages in the queue:")
        for i, message in enumerate(messages, 1):
            typer.echo(f"Message {i}:")
            typer.echo(f"Message ID: {message['MessageId']}")
            typer.echo(f"Message Body: {message['Body']}")
            typer.echo(f"Receipt Handle: {message['ReceiptHandle']}")
            typer.echo()
    else:
        typer.echo("No messages found in the queue.")


def sqs_choice(sqs):
    typer.echo("Select a queue:")
    response = sqs.list_queues()
    queues = response.get("QueueUrls", [])
    for i, queue_url in enumerate(queues):
        typer.echo(f"{i + 1}: {queue_url}")
    queue_index = typer.prompt("Queue index", type=int)
    if 0 < queue_index <= len(queues):
        queue_url = queues[queue_index - 1]
        typer.echo(f"Selected queue: {queue_url}")
    else:
        typer.secho(f"Invalid queue index: {queue_index}", fg=typer.colors.RED)
        raise typer.Exit()
    return queue_url


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    verbose: bool = typer.Option(False, "-v", "--verbose", help="verbosity"),
    version: bool = typer.Option(False, "-V", "--version", help="show version"),
):
    log_fmt = r"%(asctime)-15s %(levelname)-7s %(message)s"
    if verbose:
        logging.basicConfig(
            format=log_fmt, level=logging.DEBUG, datefmt="%m-%d %H:%M:%S"
        )
    else:
        logging.basicConfig(
            format=log_fmt, level=logging.INFO, datefmt="%m-%d %H:%M:%S"
        )
    logging.getLogger("botocore").setLevel(logging.INFO)
    logging.getLogger("boto3").setLevel(logging.INFO)
    logging.getLogger("urllib3").setLevel(logging.INFO)

    if ctx.invoked_subcommand is None and version:
        ctx.invoke(print_version)
    if ctx.invoked_subcommand is None and not version:
        typer.echo(ctx.get_help())


@app.command("version", help="Show version", hidden=True)
def print_version() -> None:
    typer.echo(f"Confguard version: {__version__}")


if __name__ == "__main__":
    app()
