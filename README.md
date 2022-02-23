# Command Line Interface for Lucidtech AI Services

## Installation

```bash
$ pip install lucidtech-las-cli
```

## Documentation

[Link to docs](https://docs.lucidtech.ai/getting-started/dev/cli)

## Usage
All methods support the `--help` flag which will provide information on the purpose of the method, 
and what arguments could be added.

```bash
$ las documents create --help
$ las models list --help
$ las workflows update --help
```

## Contributing

### Prerequisites

```bash
$ pip install -r requirements.txt
$ pip install -r requirements.ci.txt 
```

### Run tests

```bash
$ make prism-start
$ python -m pytest
