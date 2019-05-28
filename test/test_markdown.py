import sys
import warnings
import json

import pytest
from jsonschema import validate
import commonmark


parser = commonmark.Parser()


with open('element-schema.json') as fp:
    SCHEMA = json.load(fp)


def test_markdown(markdown_file):
    if markdown_file.samefile('docs/migration.md'):
        pytest.skip('migration.md intentionally contains invalid API Elements')

    with open(markdown_file) as fp:
        ast = parser.parse(fp.read())

    for node, _ in ast.walker():
        try:
            if node.t == 'code_block' and node.info == 'json':
                element = json.loads(node.literal)

                if isinstance(element, dict) and 'element' in element:
                    validate(instance=element, schema=SCHEMA)
        except:
            warnings.warn('line {}, column: {}'.format(*node.sourcepos[0]))
            raise
