from typer.testing import CliRunner

from .thend import app
from . import __version__

runner = CliRunner()


def test_app_version():
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert __version__ in result.stdout


def test_app_version_shorthand():
    result = runner.invoke(app, ["-V"])
    assert result.exit_code == 0
    assert __version__ in result.stdout
