# IOT Device Backbone - Client (Python)

## Getting Started

Install dependencies:

```
pip install -r requirements.txt
```

Then, generate the client by running:

```
ariadne-codegen
```

## Usage

See `example` directoy for examples. You can run them with:

```command
python -m example.main
```

## Development

Install locally:

```command
python -m pip install -e .
```

## Publishing

```command
python -m pip install build twine

python -m build

twine check dist/*

twine upload dist/*
```