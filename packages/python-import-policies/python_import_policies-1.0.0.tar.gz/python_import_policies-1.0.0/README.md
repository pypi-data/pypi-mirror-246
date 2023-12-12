# python-import-policies

**python-import-policies** is a Python package designed to enhance the management of import policies within your Python projects. It provides a set of contract types for the incredible [import-linter](https://github.com/seddonym/import-linter). This package allows you to enforce consistent import practices, improve code readability, and maintain a clean and organized codebase.

## Installation

Install the package using pip:

```bash
pip install python-import-policies
```

## Usage

An example configuration for `import-linter` configuration

```ini
[importlinter]
root_package = your_package
contract_types =
    import_policy: import_policies.contracts.ImportPolicy

[importlinter:contract:import-policy]
name = Define import policy
type = import_policy
allow_modules =
    your_package.** -> another_package.**
    ** -> your_package.api

```

Then execute the linter

```bash
lint-imports

```

For more information visit [import-linter](https://import-linter.readthedocs.io/) website.


## Contributing
We welcome contributions from the community! If you find a bug, have a feature request, or want to contribute code, please open an issue or submit a pull request on our [Gitlab repository](https://gitlab.com/sombrahq/python-libs/python-import-policies).

## License
MIT License
