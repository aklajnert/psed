import re

from click.testing import CliRunner

from psed import __main__

SAMPLE_FILE_1 = """
[ERROR] Some error
[INFO] Some info
[WARNING] Some warning
[ERROR] Other error
[ERROR] There's a lot of errors
[DEBUG] And one debug
"""

SAMPLE_FILE_2 = """
[ERROR] First error
[ERROR] Second error
[INFO] Info message
[WARNING] There were 2 errors
"""


def test_command_line_interface():
    """Test the CLI."""
    runner = CliRunner()
    result = runner.invoke(__main__.main)
    assert result.exit_code == 2
    assert 'Missing option "-i" / "--input"' in result.output
    help_result = runner.invoke(__main__.main, ["--help"])
    assert help_result.exit_code == 0
    assert re.search(r"--help\s+Show this message and exit", help_result.output)


def test_find_full(fs):
    fs.create_file("first_file", contents=SAMPLE_FILE_1)
    fs.create_file("second_file", contents=SAMPLE_FILE_2)

    runner = CliRunner()
    result = runner.invoke(
        __main__.main,
        ["--input", "*_file", "--find", r"\[ERROR\]", "--find", r"\[WARNING\]", "-vv"],
    )

    assert result.exit_code == 0
    assert result.output == (
        "Find patterns:\n"
        "	- \\[ERROR\\]\n"
        "	- \\[WARNING\\]\n"
        "Glob has matched following files:\n"
        "	- first_file\n"
        "	- second_file\n"
        "first_file: 4 matches:\n"
        "	(1, 8): [ERROR]\n"
        "	(60, 67): [ERROR]\n"
        "	(80, 87): [ERROR]\n"
        "	(37, 46): [WARNING]\n"
        "second_file: 3 matches:\n"
        "	(1, 8): [ERROR]\n"
        "	(21, 28): [ERROR]\n"
        "	(62, 71): [WARNING]\n"
    )


def test_find_full_no_results(fs):
    fs.create_file("first_file", contents=SAMPLE_FILE_1)
    fs.create_file("second_file", contents=SAMPLE_FILE_2)

    runner = CliRunner()
    result = runner.invoke(
        __main__.main, ["--input", "*_file", "--find", r"\[CRITICAL\]", "-vv"]
    )

    assert result.exit_code == 0
    assert result.output == (
        "Find patterns:\n"
        "	- \\[CRITICAL\\]\n"
        "Glob has matched following files:\n"
        "	- first_file\n"
        "	- second_file\n"
        "No matches.\n"
    )


def test_find_replace(fs):
    fs.create_file("first_file", contents=SAMPLE_FILE_1)
    first_replaced = fs.create_file("first_file_psed")
    fs.create_file("second_file", contents=SAMPLE_FILE_2)
    second_replaced = fs.create_file("second_file_psed")

    runner = CliRunner()
    result = runner.invoke(
        __main__.main,
        ["--input", "*_file", "--find", r"\[(\w+)\]", "--replace", r"{\1}", "-vv"],
    )

    assert result.exit_code == 0
    assert result.output == (
        "Find patterns:\n"
        "	- \\[(\\w+)\\]\n"
        "Replace pattern: {\\1}\n"
        "Glob has matched following files:\n"
        "	- first_file\n"
        "	- second_file\n"
        "Saved file after changes: first_file_psed\n"
        "Saved file after changes: second_file_psed\n"
    )

    assert first_replaced.contents == (
        "\r\n"
        "{ERROR} Some error\r\n"
        "{INFO} Some info\r\n"
        "{WARNING} Some warning\r\n"
        "{ERROR} Other error\r\n"
        "{ERROR} There's a lot of errors\r\n"
        "{DEBUG} And one debug\r\n"
    )

    assert second_replaced.contents == (
        "\r\n"
        "{ERROR} First error\r\n"
        "{ERROR} Second error\r\n"
        "{INFO} Info message\r\n"
        "{WARNING} There were 2 errors\r\n"
    )
