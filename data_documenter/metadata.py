import pandera as pa
import os
import shutil
import subprocess
from .metadocs import MetaDocs

def wrap_lines(long_text, start, end):
    long_text = long_text.replace('*', '\\*')
    return start + (start + end).join(long_text.splitlines()) + end

def title(obj):
    return obj.title if obj.title else obj.name

def description(obj, indent=0):
    if obj.description:
        return wrap_lines(obj.description, '\t' * indent, "  \n")
    else:
        return ""

def data_type(column, indent=0):
    return wrap_lines(f"**data type**: {column.dtype}", '\t' * indent, "  \n")

def user_data(name, value):
    if value:
        return wrap_lines(f"**{name}**: {value.strip()}", '', '  \n')
    else:
        return ""

class Metadata:
    def __init__(self, schema: pa.DataFrameSchema):
        self.schema: pa.DataFrameSchema = schema

    def markdown(self):
        schema = self.schema
        md = f"# {title(schema)}\n"
        md += description(schema)
        md += "## Columns\n"
        md += "\n"
        for name, column in schema.columns.items():
            md += f"### {title(column)}\n"
            md += description(column, 0)
            md += data_type(column, 0)
            for name, value in column.metadata.items():
                md += user_data(name, value)
            md += "\n"
            md += "---\n"
            md += "\n"
        return md

    def make_docs(self, path):
        # Path to the mkdocs_template.yml within your package
        template_path = os.path.join(os.path.dirname(__file__), 'templates', 'mkdocs.yml')
        yml_path = os.path.join(path, "mkdocs.yml")

        # Ensure docs directory exists
        docs_path = os.path.join(path, "docs")
        os.makedirs(docs_path, exist_ok=True)

        # Save markdown content to index.md
        markdown_content = self.markdown()
        with open(os.path.join(docs_path, "index.md"), "w") as f:
            f.write(markdown_content)

        shutil.copyfile(template_path, yml_path)

        subprocess.run([
            "mkdocs",
            "build",
            "-f", yml_path,
            "--no-directory-urls"
            ],
            check=True
        )
        return MetaDocs(path)