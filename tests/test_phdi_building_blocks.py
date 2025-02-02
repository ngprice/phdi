from importlib import metadata
import toml
from pathlib import Path


def test_version():
    with open(Path(__file__).parent.parent / "pyproject.toml") as project_config_file:
        project_config = toml.load(project_config_file)
        assert (
            "v" + metadata.version("phdi")
            == project_config["tool"]["poetry"]["version"]
        )
