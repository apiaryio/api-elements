from pathlib import Path


def pytest_generate_tests(metafunc):
    if 'markdown_file' in metafunc.fixturenames:
        paths = Path('docs').glob('*.md')
        metafunc.parametrize('markdown_file', paths)
