import pandas as pd
import pandera as pa
import pytest
import subprocess
import shutil
import os
from time import sleep
from tests.schemas.annotation import schema

TEST_DOCS_PATH = 'test-docs'

from data_documenter.metadata import (
    Metadata
)
from data_documenter.metadocs import MetaDocs

# @pytest.fixture(scope="session", autouse=True)
# def cleanup_after_tests(request):
#     # Request.addfinalizer is called after all tests in the session
#     request.addfinalizer(lambda: shutil.rmtree(TEST_DOCS_PATH, ignore_errors=True))

@pytest.fixture
def sample_dataframe():
    # Create a sample DataFrame
    data = {'a': [1, 2, 3, None, 5, 6], 'b': ['x', 'x', 'x', 'y', 'x', 'y']}
    df = pd.DataFrame(data)
    return df

@pytest.fixture
def sample_schema():
    return pa.DataFrameSchema(
        columns = {
            'Column 1': pa.Column(
                str, 
                description="Description with\nmany lines"
            ),
            'Column_2': pa.Column(
                str, 
                title='Column 2',
            ),
        },
        description='Test pandera schema',
        name = 'Test'
    )

def test_metadata_instance(sample_dataframe):
    schema = pa.infer_schema(sample_dataframe)
    meta = Metadata(schema)
    assert isinstance(meta, Metadata)

def test_markdown(sample_schema):
    expected_md = """# Test
*Test pandera schema*

## Column 1
*Description with*  
*many lines*  
data type: str  

## Column 2
data type: str  
"""
    metadata = Metadata(sample_schema)
    md = metadata.markdown()
    print(md)
    print("----------")
    print(expected_md)
    for (a, b) in zip(md.splitlines(), expected_md.splitlines()):
        assert a == b

def test_makedocs():
    metadata = Metadata(schema)
    markdown_content = metadata.markdown()
    meta_docs = metadata.make_docs(path=TEST_DOCS_PATH)

    assert isinstance(meta_docs, MetaDocs)

    # Verify existence of index.md and mkdocs.yml
    assert os.path.exists(os.path.join(TEST_DOCS_PATH, "docs/index.md"))
    assert os.path.exists(os.path.join(TEST_DOCS_PATH, "mkdocs.yml"))
    assert os.path.exists(os.path.join(TEST_DOCS_PATH, "site"))

    # Verify content of index.md
    with open(os.path.join(TEST_DOCS_PATH, "docs/index.md"), 'r') as f:
        index_md_content = f.read()
    assert index_md_content == markdown_content

    # Verify content of mkdocs.yml supports theme material and includes admonitions
    with open(os.path.join(TEST_DOCS_PATH, "mkdocs.yml"), 'r') as f:
        mkdocs_yml_content = f.read()

    assert 'theme:' in mkdocs_yml_content
    assert 'name: material' in mkdocs_yml_content
    assert 'markdown_extensions:' in mkdocs_yml_content
    assert 'admonition' in mkdocs_yml_content

    meta_docs.run()
    sleep(1)
