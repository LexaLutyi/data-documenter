from data_documenter.pandera_plugin import pandera_to_markdown
from tests.schemas.example import schema

md = pandera_to_markdown(schema, file_name='test-docs/docs/index')
md.create_md_file()