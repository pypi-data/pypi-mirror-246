"""Main file for the thendisnever package."""
import os
from typing import Optional

from rich import print
from rich.progress import Progress, SpinnerColumn, TextColumn
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TextStreamer,
)
import torch
import typer
from typing_extensions import Annotated

from .__init__ import __version__

# Disable HF parallelism warning message
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Define the app
app = typer.Typer(
    rich_markup_mode="rich",
)

# Define the default arguments
DEFAULT_MODEL_NAME = "togethercomputer/RedPajama-INCITE-Base-3B-v1"  # https://huggingface.co/togethercomputer/RedPajama-INCITE-Base-3B-v1
DEFAULT_PROMPT = "THE END IS NEVER THE END IS NEVER "  # https://thestanleyparable.fandom.com/wiki/The_End_Is_Never...
DEFAULT_MAX_MEMORY_RATIO = 0.5  # Randomly chosen

# Define useful variables
STATE = {"verbose": False, "super_verbose": False}
DEVICE = "cuda:0" if torch.cuda.is_available() else "cpu"
CONNECTION_ERROR_MSG = "Connection error, retrying...\n\n"


# Define helper functions
def clear_terminal():
    if os.name == "nt":  # For Windows
        _ = os.system("cls")
    else:  # For macOS and Linux
        _ = os.system("clear")


def download_model(model_name: str):
    model = AutoModelForCausalLM.from_pretrained(model_name)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    streamer = TextStreamer(
        tokenizer,
        skip_prompt=True,
    )
    if STATE["super_verbose"]:
        print("Model downloaded")
    return model, tokenizer, streamer


def download_model_with_progress(model_name: str):
    if STATE["super_verbose"]:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Downloading model...", total=None)
            return download_model(model_name)
    else:
        return download_model(model_name)


# Callbacks
def version_print(value: bool):
    if value:
        print(f"Thendisnever version: {__version__}")
        raise typer.Exit()


def change_verbose(value: int):
    if value:
        if value > 0:
            STATE["verbose"] = True
        if value > 1:
            STATE["super_verbose"] = True


# Main functions
def run(model_name, prompt, max_memory_ratio):
    # Download model and tokenizer
    try:
        model, tokenizer, streamer = download_model_with_progress(model_name)
    except Exception as e:
        if "valid" in str(e):  # To catch invalid model names
            if STATE["super_verbose"]:
                print("Invalid model name, using default model\n\n")
            model_name = DEFAULT_MODEL_NAME  # To use the default model
            model, tokenizer, streamer = download_model_with_progress(model_name)
        elif "timed out" in str(e):  # To catch connection errors
            raise Exception(
                CONNECTION_ERROR_MSG
            ) from None  # from None suppresses multiple tracebacks
        else:
            raise Exception(e) from None

    # Generate text
    try:
        # Define model.generate() arguments
        max_length = (
            model.config.max_length
        )  # Context window size of the model (in tokens)
        max_memory = int(max_length * max_memory_ratio) + 1

        # Check if prompt is too long
        inputs = tokenizer(
            [prompt],  # Wrap prompt as a list since inputs are usually a batch
            return_tensors="pt",  # Return PyTorch tensors
        )["input_ids"][
            0
        ]  # Text to tokens, index 0 because only one prompt
        if len(inputs) >= max_length:
            inputs = inputs[
                : max_length - 1
            ]  # Only keep the first max_length - 1 tokens
            prompt = tokenizer.decode(
                inputs,
                skip_special_tokens=True,
            )
        clear_terminal()
        print(prompt)

        # Set up the conversation loop, where the response is used as the next prompt
        while True:
            inputs = tokenizer(
                [prompt],  # Wrap prompt as a list since inputs are usually a batch
                return_tensors="pt",
            )
            inputs, model = inputs.to(DEVICE), model.to(
                DEVICE
            )  # Move to GPU if available
            response = model.generate(
                **inputs,
                streamer=streamer,
                max_length=max_length,
                num_return_sequences=1,  # To return only one response
                pad_token_id=tokenizer.eos_token_id,  # To remove warning message in console
                do_sample=True,
                num_beams=1,
            )  # Arguments from here: https://huggingface.co/docs/transformers/generation_strategies#multinomial-sampling
            prompt = tokenizer.decode(
                response[0][-max_memory:],
                skip_special_tokens=True,
            )
    except Exception as e:
        raise Exception(e) from None


@app.command(
    name="isnever",
    help=":infinity: [bold red]Endless[/bold red] text generation with [italic]Hugging Face models.[/italic]",
    epilog="Made by [bold blue]Andrew Hinh.[/bold blue] :mechanical_arm::person_climbing:",
    context_settings={"allow_extra_args": False, "ignore_unknown_options": True},
)
def main(
    model_name: Annotated[
        Optional[str],
        typer.Option(
            "--name",
            "-n",
            help="Model to generate text with, more info here: https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoModelForCausalLM",
        ),
    ] = DEFAULT_MODEL_NAME,
    prompt: Annotated[
        Optional[str],
        typer.Option(
            "--prompt",
            "-p",
            help="Initial prompt for model, length (in tokens) < the model's max_length",
        ),
    ] = DEFAULT_PROMPT,
    max_memory_ratio: Annotated[
        Optional[float],
        typer.Option(
            "--ratio",
            "-r",
            min=0,
            max=1,
            clamp=True,
            help="% of past tokens to remember, 0 < x < 1",
        ),
    ] = DEFAULT_MAX_MEMORY_RATIO,
    version: Annotated[
        Optional[bool],
        typer.Option("--version", "-V", callback=version_print, is_eager=True),
    ] = None,
    verbose: Annotated[
        Optional[int],
        typer.Option(
            "--verbose",
            "-v",
            callback=change_verbose,
            is_eager=True,
            count=True,
        ),
    ] = None,
):
    while True:
        try:
            run(model_name, prompt, max_memory_ratio)
        except (KeyboardInterrupt, Exception) as e:
            if str(e) == CONNECTION_ERROR_MSG:
                if STATE["super_verbose"]:
                    print(CONNECTION_ERROR_MSG)
                continue  # Retry
            else:
                if STATE["verbose"]:
                    print("\n\nExiting...")
                break  # Exit


if __name__ == "__main__":
    app()
