import os


def test_version_file_exists_and_has_content():
    """Ensure VERSION file exists and contains a valid version string."""
    version_path = "VERSION"
    assert os.path.exists(version_path), "VERSION file is missing"

    with open(version_path, "r") as f:
        version = f.read().strip()

    assert len(version) > 0, "VERSION file is empty"
    assert all(
        c.isdigit() or c in ".-" for c in version
    ), f"Invalid version format: {version}"


def test_placeholder_pass():
    """Basic placeholder to ensure CI runs even before releases exist."""
    assert True
