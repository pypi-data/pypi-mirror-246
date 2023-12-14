# The End is Never

A package to make an LLM talk with itself forever.

```python
from thendisnever.thend import isnever
isnever()
```

## Parameters

- `model_name`: The model to generate text with.
  - [This](https://huggingface.co/togethercomputer/RedPajama-INCITE-Base-3B-v1) is the default model.
  - This must be a model compatible with [AutoModelForCausalLM](https://huggingface.co/docs/transformers/model_doc/auto#transformers.AutoModelForCausalLM).
- `prompt`: The initial prompt for the model.
  - [This](https://thestanleyparable.fandom.com/wiki/The_End_Is_Never...) is the inspiration for the default prompt.
- `max_memory_ratio`: The % of past tokens to remember.
  - This must be a real number between or equal to 0 and 1.

## Notes

- When running `isnever()` for the first time, it will download the model and tokenizer from HuggingFace. This will take a while, but it only needs to be done once.
- If you want to use the CPU (not recommended because it's slow, but it works), make sure you have [PyTorch for CPU](https://pytorch.org/get-started/locally/) installed before installing this package.

## Contributing

Check out [this guide](https://typer.tiangolo.com/tutorial/package/) that describes how to create a package with [Typer](https://typer.tiangolo.com/).

Before testing, make sure to update the version:

- `pyproject.toml` ->  `tool.poetry`
- `src/thendisnever/__init__.py` -> `__version__`

And the dependencies:

- `pyproject.toml` -> `tool.poetry.dependencies`
