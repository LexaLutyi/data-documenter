from data_documenter.pandera_plugin import create_documentation
from tests.schemas.example import schema
import time

md = create_documentation(schema, docs_path='test-docs', title='Test', author='tester')
md.run()

time.sleep(5)