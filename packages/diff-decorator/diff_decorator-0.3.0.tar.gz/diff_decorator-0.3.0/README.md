# Diff Decorator

[![Unit Test Diff Decorator](https://github.com/weshouman/py-diff-decorator/actions/workflows/python-test.yml/badge.svg)](https://github.com/weshouman/py-diff-decorator/actions/workflows/python-test.yml)

## Overview
`diff_decorator` is a Python package that provides a decorator for unittests, enhancing the visualization of differences when assertions fail. It allows easy comparison of expected and actual results using a diff tool of your choice.

## Installation

```
pip install diff_decorator
```

## Usage

To use `diff_decorator`, import the `diff_with` decorator in your test files and apply it to your test methods.

### Basic Usage

```python
from diff_decorator import diff_with
import unittest

class MyTestCase(unittest.TestCase):

    @diff_with
    def test_example(self):
        expected = "expected string"
        actual = "actual string"
        self.assertEqual(expected, actual)
```

### Customizing the Diff Tool

By default, `diff_with` uses `diff` as the diff tool. That could be customized by setting the `DIFF_DECORATOR_TOOL` environment variable or by specifying a tool in the decorator (which has higher precedence).

#### Using an Environment Variable

To modify the default diff tool set the `DIFF_DECORATOR_TOOL` environment variable to the preferred diff tool:

```bash
export DIFF_DECORATOR_TOOL=meld
```

#### Specifying the Tool in the Decorator

```python
@diff_with(tool='meld')
def test_example_with_custom_tool(self):
    # ...
```

### Notes

- The decorator only runs when the test shows differences (e.g., if it fails).

## Requirements

- Python 3.x
- External diff tool (e.g., vimdiff, meld, diff)

## Development

For development, clone the repository and install the package using pip:

```bash
git clone https://github.com/weshouman/diff_decorator.git
cd diff_decorator
pip install .
```

To publish the project

```
pip install setuptools
python setup.py sdist bdist_wheel
pip install twine
twine upload dist/*
```

## License

This project is licensed under the [MIT License](LICENSE) while being prohibited for use in anything that is Haram.

