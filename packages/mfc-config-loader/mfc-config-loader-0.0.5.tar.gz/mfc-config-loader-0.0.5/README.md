# MFC Configuration Loader

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

## Introduction
MFC Configuration Loader streamlines YAML-based configuration management with features such as multi-file support, variables, strong typing, and more.


### Features

1. **Multiple Configuration Files**: Configurations can be separated into multiple files to better organize and segregate them based on environment, purpose, and any other criteria.

2. **Variables**: Can define variables referencing other configurations or environment variables.

3. **Strong Typing**: Configurations are loaded into the tuple hierarchy, enabling accessing node properties via dot notation.

## Installation

```shell
pip install mfc-config-loader
```


## Usage

> **Note**  
> Additonal usage examples will be added soon.

```yaml
# .config.yaml
gcp:
  project_id: my-project-id
  sa_key_filepath: /path/to/key.json
  default_dataset: ${project_id}.my_dataset
```

```python
# main.py
configs = ConfigLoader().load("gcp")

project_id = configs.project_id
sa_key_file = configs.sa_key_filepath
default_dataset = configs.default_dataset

```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)