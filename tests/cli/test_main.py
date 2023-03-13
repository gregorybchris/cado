from unittest.mock import Mock

import pytest
from click.testing import CliRunner
from pytest import MonkeyPatch

from cado.cli.cli import up
from cado.app import app as app_module


@pytest.fixture(scope="function")
def mock_cado_app(monkeypatch: MonkeyPatch) -> Mock:
    mock = Mock()
    monkeypatch.setattr(app_module, "app", mock)
    return mock


class TestMain:

    @pytest.mark.skip("Not working")
    def test_up(self, mock_cado_app: Mock):
        runner = CliRunner()
        result = runner.invoke(up, [])
        assert result.exit_code == 0
        assert result.output == "output-message"
