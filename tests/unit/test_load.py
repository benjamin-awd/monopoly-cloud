from monocloud.storage import load


def test_load(mock_df, mock_statement, tmp_path):
    output_directory = tmp_path / "output"
    output_directory.mkdir()
    output_path = load(mock_df, mock_statement, output_directory)

    assert output_path.is_file()
    assert output_path.stem == "foo-credit-2024-12-a67ee2"
    assert output_path.parent == output_directory
