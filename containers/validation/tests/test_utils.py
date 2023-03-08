import pathlib
import yaml
from app.utils import load_config, validate_error_types, validate_config

config_path = pathlib.Path(__file__).parent.parent / "config" / "sample_ecr_config.yaml"


def test_load_config():
    config = load_config(config_path)
    assert config != ""


def test_validate_error_types():
    valid_ets = "errors,warnings"
    invalid_ets = "blah,information"
    invalid_ets2 = "blah, nope, wrong"
    invalid_ets3 = "information,blah, nope, wrong,warnings"
    invalid_ets4 = "info,warnings"
    null_ets = ""

    assert validate_error_types(valid_ets) == ["errors", "warnings"]
    assert validate_error_types(invalid_ets) == ["information"]
    assert validate_error_types(invalid_ets2) == []
    assert validate_error_types(invalid_ets3) == ["information", "warnings"]
    assert validate_error_types(invalid_ets4) == ["warnings"]
    assert validate_error_types(null_ets) == []
    assert validate_error_types(None) == []


def test_validate_config_bad():
    with open(
        pathlib.Path(__file__).parent.parent.parent.parent
        / "tests"
        / "assets"
        / "sample_ecr_config_bad.yaml",
        "r",
    ) as file:
        config_bad = yaml.safe_load(file)
        result = validate_config(config_bad)
        assert not result


def test_validate_config_good():
    with open(
        pathlib.Path(__file__).parent.parent.parent.parent
        / "tests"
        / "assets"
        / "sample_ecr_config.yaml",
        "r",
    ) as file:
        config = yaml.safe_load(file)
        result = validate_config(config)
        assert result
