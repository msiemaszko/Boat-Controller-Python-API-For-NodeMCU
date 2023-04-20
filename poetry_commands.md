# Poetry
https://python-poetry.org/docs/

## install:
```sh
curl -sSL https://install.python-poetry.org | python -
lub
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```
To get started you need Poetry's bin directory (C:\Users\mareksiemaszko\AppData\Roaming\Python\Scripts) in your `PATH`
environment variable.

## test
```sh
poetry --version
```

## setup new project:
```sh
cd ~\repos
poetry new boat_controler
```

## init env in existing project
```sh
poetry init

# add dependencies
poetry add customtkinter
poetry add requests

mkdir .\src
echo "print('Hello World!')" > .\src\hello.py

code .
```

# Install dependencies based defined conf
```sh
poetry install
```

## run srcipt
```sh
poetry run python .\src\hello.py
poetry run python .\src\Boat_Controller_UI.py
```
