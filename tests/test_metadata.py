import pandas as pd
import pytest
import subprocess
import shutil
import os
from time import sleep

TEST_DOCS_PATH = 'test-docs'

from data_documenter.metadata import (
    Metadata,
    DataEntry
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

def test_metadata_instance():
    meta = Metadata()
    assert isinstance(meta, Metadata)

def test_dataentry_instance():
    entry = DataEntry(
        name = 'count(1)',
        eltype = 'number',
        updated = 546
    )
    assert isinstance(entry, DataEntry)

def test_metadata_fit(sample_dataframe):
    # Create a Metadata instance
    metadata = Metadata()

    # Fit the Metadata instance with the sample DataFrame
    metadata.fit(sample_dataframe)

    # Check if metadata.items[0] is a DataEntry instance
    assert isinstance(metadata.items[0], DataEntry)
    assert isinstance(metadata.items[1], DataEntry)

    # Check the attributes of the DataEntry instance
    data_entry = metadata.items[0]
    assert data_entry.name == 'a'
    assert data_entry.eltype == sample_dataframe['a'].dtype.name
    assert data_entry.updated == sample_dataframe['a'].count()

    # Check the attributes of the DataEntry instance
    data_entry = metadata.items[1]
    assert data_entry.name == 'b'
    assert data_entry.eltype == sample_dataframe['b'].dtype.name
    assert data_entry.updated == sample_dataframe['b'].count()

def test_markdown(sample_dataframe):
    metadata = Metadata(
        name = 'Test data',
        description = 'Just some dummy dataset',
    )
    metadata.fit(sample_dataframe)
    expected_md = """# Test data
Just some dummy dataset

???+ note "a"
\telement type: float64  
\tNot nulls: 5  

???+ note "b"
\telement type: object  
\tNot nulls: 6  
"""
    md = metadata.markdown()
    print(md)
    assert md.strip() == expected_md.strip()

def test_makedocs(sample_dataframe):
    metadata = Metadata(
        name='Test data',
        description='Just some dummy dataset',
    )
    metadata.fit(sample_dataframe)
    markdown_content = metadata.markdown()  # Assuming this returns the markdown content
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
