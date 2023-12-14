# pptg
python package template for publish to pypi

```bash

mkdir pptg
cd pptg
pdm init






```

## init project

```bash
pip install pdm --upgrade
pipx install pdm --upgrade

pdm init
pdm run python -m ensurepip
pdm run python.exe -m pip install --upgrade pip

pdm add -dG test pytest pytest-cov pytest-mock coverage
pdm add -dG lint ruff mypy
pdm add -dG fmt ruff
pdm add -dG docs mkdocs
pdm add -dG all pytest pytest-cov pytest-mock coverage ruff mypy mkdocs
pdm plugin add pdm-publish

pdm list
pdm list --graph
pdm list pytest --graph

# 更新所有的 dev 依赖
pdm update -d

# 更新 dev 依赖下某个分组的某个包
pdm update -dG test pytest

如果你的依赖包有设置分组，还可以指定分组进行更新

pdm update -G format -G docs
也可以指定分组更新分组里的某个包

pdm update -G format yapf

```

## init existed project
```bash
pdm install
pdm run python -m ensurepip
pdm run python.exe -m pip install --upgrade pip

```


## publish package
```bash
config_path: "C:\Users\lgf\AppData\Local\pdm\pdm\config.toml"

pdm config repository.pypi.username "__token__"
pdm config repository.pypi.password "my-pypi-token"

pdm config repository.testpypi.username "__token__"
pdm config repository.testpypi.url "https://test.pypi.org/legacy/"
pdm config repository.testpypi.password "my-testpypi-token"

pdm config repository.company.url "https://pypi.company.org/legacy/"
pdm config repository.company.ca_certs "/path/to/custom-cacerts.pem"

pdm config -d repository.testpypi.username
pdm config -d repository.testpypi.username
pdm config -d repository.testpypi.username


```
