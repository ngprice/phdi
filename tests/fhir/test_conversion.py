import pathlib
from unittest import mock

from phdi.fhir.conversion import convert_to_fhir
from phdi.fhir.conversion.convert import _get_fhir_conversion_settings
from phdi.harmonization import standardize_hl7_datetimes


def test_get_fhir_conversion_settings():

    # HL7 case 1 (using the demo message from the HL7 API walkthrough)
    message = ""
    with open(pathlib.Path(__file__).parent.parent / "assets" / "sample_hl7.hl7") as fp:
        message = fp.read()
    settings = _get_fhir_conversion_settings(message)
    assert settings == {
        "root_template": "ORU_R01",
        "input_data_type": "HL7v2",
        "template_collection": "microsofthealth/fhirconverter:default",
    }

    # HL7 case 2, when MSH[3] is set
    message = ""
    with open(
        pathlib.Path(__file__).parent.parent / "assets" / "hl7_with_msh_3_set.hl7"
    ) as fp:
        message = fp.read()
    settings = _get_fhir_conversion_settings(message)
    assert settings == {
        "root_template": "ADT_A01",
        "input_data_type": "HL7v2",
        "template_collection": "microsofthealth/fhirconverter:default",
    }

    # CCDA case (using an example found at https://github.com/HL7/C-CDA-Examples)
    message = ""
    with open(
        pathlib.Path(__file__).parent.parent / "assets" / "ccda_sample.xml"
    ) as fp:
        message = fp.read()
    settings = _get_fhir_conversion_settings(message)
    assert settings == {
        "root_template": "ProcedureNote",
        "input_data_type": "Ccda",
        "template_collection": "microsofthealth/ccdatemplates:default",
    }


@mock.patch("requests.Session")
def test_convert_to_fhir_success(mock_requests_session):

    mock_requests_session_instance = mock_requests_session.return_value

    mock_requests_session_instance.post.return_value = mock.Mock(
        status_code=200,
        json=lambda: {"resourceType": "Bundle", "entry": [{"hello": "world"}]},
    )

    mock_access_token_value = "some-token"
    mock_access_token = mock.Mock()
    mock_access_token.token = mock_access_token_value
    mock_cred_manager = mock.Mock()
    mock_cred_manager.get_access_token.return_value = mock_access_token

    message = ""
    with open(pathlib.Path(__file__).parent.parent / "assets" / "sample_hl7.hl7") as fp:
        message = fp.read()
    response = convert_to_fhir(
        message,
        mock_cred_manager,
        "some-fhir-url",
    )

    mock_requests_session_instance.post.assert_called_with(
        url="some-fhir-url/$convert-data",
        headers={"Authorization": f"Bearer {mock_access_token_value}"},
        json={
            "resourceType": "Parameters",
            "parameter": [
                {
                    "name": "inputData",
                    "valueString": standardize_hl7_datetimes(message),
                },
                {"name": "inputDataType", "valueString": "HL7v2"},
                {
                    "name": "templateCollectionReference",
                    "valueString": "microsofthealth/fhirconverter:default",
                },
                {"name": "rootTemplate", "valueString": "ORU_R01"},
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {"resourceType": "Bundle", "entry": [{"hello": "world"}]}


@mock.patch("requests.Session")
def test_convert_to_fhir_failure(mock_requests_session):

    mock_requests_session_instance = mock_requests_session.return_value
    mock_access_token_value = "some-token"
    mock_access_token = mock.Mock()
    mock_access_token.token = mock_access_token_value
    mock_cred_manager = mock.Mock()
    mock_cred_manager.get_access_token.return_value = mock_access_token
    mock_requests_session_instance.post.return_value = mock.Mock(
        status_code=400,
        text='{ "resourceType": "Bundle", "entry": [{"hello": "world"}] }',
    )

    message = ""
    with open(pathlib.Path(__file__).parent.parent / "assets" / "sample_hl7.hl7") as fp:
        message = fp.read()

    # Most efficient way to verify that the function will raise an exception,
    # since we're not using a unittest class structure and the exception is
    # _not_ merely a unittest.mock.side_effect of the session instance
    response = None
    try:
        response = convert_to_fhir(
            message,
            mock_cred_manager,
            "some-fhir-url",
        )
    except Exception as e:
        assert (
            repr(e)
            == "Exception('HTTP 400 code encountered in $convert-data for a message')"
        )
        assert response is None
