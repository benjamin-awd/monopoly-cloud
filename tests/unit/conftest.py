from unittest.mock import Mock

import pytest
from pandas import DataFrame


class MockStatement:
    def __init__(self, document, statement_config, statement_type, statement_date):
        self.document = document
        self.statement_config = statement_config
        self.statement_type = statement_type
        self.statement_date = statement_date


class MockConfig:
    def __init__(self):
        self.bank_name = "foo"


class MockStatementDate:
    def __init__(self):
        self.year = 2024
        self.month = 12
        self.day = 1


@pytest.fixture
def mock_statement_date():
    return MockStatementDate()


@pytest.fixture
def mock_statement_config():
    return MockConfig()


@pytest.fixture
def mock_statement(mock_statement_config, mock_statement_date):
    mock_document = Mock()
    mock_document.metadata = {"foo"}
    return MockStatement(
        document=mock_document,
        statement_config=mock_statement_config,
        statement_type="credit",
        statement_date=mock_statement_date,
    )


@pytest.fixture
def mock_df():
    return DataFrame({"col1": [1, 2, 3], "col2": [4, 5, 6]})
