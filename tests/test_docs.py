from pathlib import Path


DOCS_DIR = Path(__file__).parents[1] / "docs"


def test_api_reference_pages_are_registered_in_documentation_tree():
    index = (DOCS_DIR / "index.rst").read_text(encoding="utf-8")

    assert "cloud_admin" in index
    assert "rest_client" in index


def test_extended_client_guides_include_autodoc_api_references():
    expected_references = {
        "bamboo.rst": "atlassian.bamboo.Bamboo",
        "bitbucket.rst": "atlassian.bitbucket.Bitbucket",
        "cloud_admin.rst": "atlassian.cloud_admin.CloudAdmin",
        "confluence.rst": "atlassian.confluence.server.Server",
        "crowd.rst": "atlassian.crowd.Crowd",
        "rest_client.rst": "atlassian.rest_client",
    }

    for filename, reference in expected_references.items():
        contents = (DOCS_DIR / filename).read_text(encoding="utf-8")
        assert reference in contents
        assert "API reference" in contents


def test_confluence_reference_covers_server_legacy_cloud_and_v2_clients():
    contents = (DOCS_DIR / "confluence.rst").read_text(encoding="utf-8")

    assert "atlassian.confluence.server.Server" in contents
    assert "atlassian.confluence.cloud.Cloud" in contents
    assert "atlassian.confluence.cloud.cloud.ConfluenceCloud" in contents


def test_bitbucket_reference_covers_compatible_cloud_and_server_clients():
    contents = (DOCS_DIR / "bitbucket.rst").read_text(encoding="utf-8")

    assert "atlassian.bitbucket.Bitbucket" in contents
    assert "atlassian.bitbucket.cloud.Cloud" in contents
    assert "atlassian.bitbucket.server.Server" in contents


def test_sphinx_configuration_can_import_repository_and_mock_optional_auth_dependencies():
    config = (DOCS_DIR / "conf.py").read_text(encoding="utf-8")

    assert 'os.path.abspath("..")' in config
    assert "autodoc_mock_imports" in config
    assert '"oauthlib"' in config
