import pathlib

import yaml
from phdi.validation.validation import validate_ecr, _validate_config


# Test file with known errors
sample_file_bad = open(
    pathlib.Path(__file__).parent.parent / "assets" / "ecr_sample_input_bad.xml"
).read()


# Test good file
sample_file_good = open(
    pathlib.Path(__file__).parent.parent / "assets" / "ecr_sample_input_good.xml"
).read()

# Test file with error
sample_file_error = open(
    pathlib.Path(__file__).parent.parent / "assets" / "ecr_sample_input_error.xml"
).read()

with open(
    pathlib.Path(__file__).parent.parent / "assets" / "sample_ecr_config.yaml", "r"
) as file:
    config = yaml.safe_load(file)


def test_validate_good():
    expected_response = {
        "message_valid": True,
        "validation_results": {
            "fatal": [],
            "errors": [],
            "warnings": [],
            "information": ["Validation complete with no errors!"],
        },
    }
    result = validate_ecr(
        ecr_message=sample_file_good,
        config=config,
        error_types=["fatal", "error", "warn", "info"],
    )

    assert result == expected_response


def test_validate_bad():
    expected_response = {
        "message_valid": False,
        "validation_results": {
            "fatal": [
                "Could not find field: {'fieldName': 'eICR Version Number', "
                + "'cdaPath': '//hl7:ClinicalDocument/hl7:versionNumber', "
                + "'errorType': 'fatal', "
                + "'attributes': [{'attributeName': 'value'}]}",
                "Could not find field: {'fieldName': 'First "
                + "Name', 'cdaPath': "
                + "'//hl7:ClinicalDocument/hl7:recordTarget/hl7:patientRole/"
                + "hl7:patient/hl7:name/hl7:given', "
                + "'errorType': 'fatal', "
                + "'textRequired': 'True', 'parent': 'name', "
                + "'parent_attributes': [{'attributeName': "
                + "'use', 'regEx': 'L'}]}",
                "Could not find field: {'fieldName': "
                + "'City', 'cdaPath': "
                + "'//hl7:ClinicalDocument/hl7:recordTarget/hl7:patientRole/hl7:addr/"
                + "hl7:city', "
                + "'errorType': 'fatal', "
                + "'textRequired': 'True', 'parent': 'addr', "
                + "'parent_attributes': [{'attributeName': "
                + "'use', 'regEx': 'H'}]}",
                "Field: Zip does not match regEx: [0-9]{5}(?:-[0-9]{4})?",
            ],
            "errors": [],
            "warnings": ["Attribute: 'code' for field: 'Sex' not in expected format"],
            "information": [],
        },
    }
    result = validate_ecr(
        ecr_message=sample_file_bad,
        config=config,
        error_types=["error", "warn", "info"],
    )

    assert result == expected_response


def test_validate_error():
    expected_response = {
        "message_valid": True,
        "validation_results": {
            "fatal": [],
            "errors": [
                "Could not find field: {'fieldName': 'Status', 'cdaPath': "
                + "'//hl7:ClinicalDocument/hl7:component/hl7:structuredBody/hl7:"
                + "component/hl7:section/hl7:entry/hl7:act/hl7:code', "
                + "'errorType': 'error', 'attributes': [{'attributeName': 'code'}]}"
            ],
            "warnings": [],
            "information": ["Validation complete with no errors!"],
        },
    }
    result = validate_ecr(
        ecr_message=sample_file_error,
        config=config,
        error_types=["error", "warn", "info"],
    )

    assert result == expected_response


def test_validate_config_bad():
    with open(
        pathlib.Path(__file__).parent.parent / "assets" / "sample_ecr_config_bad.yaml",
        "r",
    ) as file:
        config_bad = yaml.safe_load(file)
        result = _validate_config(config_bad)
        assert not result
