# tlylt

## Development

### Lint
    
```bash
ruff check .
```

### Local install

```bash
pip install -e .
```

### Test

### Release

```bash
rm -rf dist & rm -rf tlylt.egg-info
python setup.py sdist
twine upload dist/*
```