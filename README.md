# pyci-lint

Python GitHub Actions

## Create requirements.txt

```bash
$ pip freeze | grep -e black -e isort -e flake8 -e mypy > requirements.txt
```
