from click.testing import CliRunner

from psed import __main__


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(__main__.main)
    assert result.exit_code == 0
    assert "psed.cli.main" in result.output
    help_result = runner.invoke(__main__.main, ["--help"])
    assert help_result.exit_code == 0
    assert "--help  Show this message and exit." in help_result.output
