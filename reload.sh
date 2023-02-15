pip uninstall -y chatter
rm -rf dist/*
poetry build
pip install dist/chatter-`poetry version -s`-py3-none-any.whl
