from unittest.mock import Mock
from unittest.mock import patch, mock_open
from click.testing import CliRunner

from obsidian_linker.main import analyze_text
from obsidian_linker.main import extract_first_500_words
from obsidian_linker.main import process_markdown_files


def test_extract_first_500_words_with_less_than_500_words():
    text = "This is a short text."
    result = extract_first_500_words(text)
    assert (
        result == text
    ), "The function should return the original text if it contains less than 500 words."


def test_extract_first_500_words_with_exactly_500_words():
    text = "word " * 500
    result = extract_first_500_words(text)
    assert (
        result == text.rstrip()
    ), "The function should return the original text if it contains exactly 500 words."


def test_extract_first_500_words_with_more_than_500_words():
    text = "word " * 501
    expected = "word " * 500
    result = extract_first_500_words(text)
    assert (
        result == expected.rstrip()
    ), "The function should return the first 500 words if the text contains more than 500 words."


def test_extract_first_500_words_with_empty_string():
    text = ""
    result = extract_first_500_words(text)
    assert (
        result == ""
    ), "The function should return an empty string if the input is an empty string."


def test_analyze_text_returns_keywords_when_api_response_is_successful():
    mock_openai_client = Mock()
    mock_openai_client.chat.completions.create.return_value = Mock(
        choices=[Mock(message=Mock(content="keyword1, keyword2"))]
    )
    text = "This is a sample text."
    result = analyze_text(text, mock_openai_client)
    assert result == ["keyword1", "keyword2"]


@patch("os.listdir")
@patch("builtins.open", new_callable=mock_open, read_data="This is a sample text.")
@patch("obsidian_linker.main.get_openai_client")
@patch("obsidian_linker.main.analyze_text", return_value=["keyword1", "keyword2"])
@patch(
    "obsidian_linker.main.extract_first_500_words",
    return_value="This is a sample text.",
)
def test_process_markdown_files_processes_files_when_keywords_are_found(
    mock_extract, mock_analyze, mock_client, mock_file, mock_listdir
):
    mock_listdir.return_value = ["file1.md", "file2.md"]
    runner = CliRunner()
    result = runner.invoke(process_markdown_files, ["--directory", "directory"])
    assert result.exit_code == 0


@patch("os.listdir")
@patch("builtins.open", new_callable=mock_open, read_data="This is a sample text.")
@patch("obsidian_linker.main.get_openai_client")
@patch("obsidian_linker.main.analyze_text", return_value=[])
@patch(
    "obsidian_linker.main.extract_first_500_words",
    return_value="This is a sample text.",
)
def test_process_markdown_files_skips_files_when_no_keywords_are_found(
    mock_extract, mock_analyze, mock_client, mock_file, mock_listdir
):
    mock_listdir.return_value = ["file1.md", "file2.md"]
    runner = CliRunner()
    result = runner.invoke(process_markdown_files, ["--directory", "directory"])
    assert result.exit_code == 0
