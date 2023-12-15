# detect_llm_api_keys

scan python files for llm api keys (designed for pre-commit)


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![python](https://img.shields.io/badge/Python-3.9+-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)

[![Publish to PyPI](https://github.com/joshuasundance-swca/detect_llm_api_keys/actions/workflows/publish_on_pypi.yml/badge.svg)](https://github.com/joshuasundance-swca/detect_llm_api_keys/actions/workflows/publish_on_pypi.yml)
![GitHub tag (with filter)](https://img.shields.io/github/v/tag/joshuasundance-swca/detect_llm_api_keys)
[![Read the Docs](https://img.shields.io/readthedocs/detect_llm_api_keys)](https://detect-llm-api-keys.readthedocs.io/en/latest/)

![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/joshuasundance-swca/detect_llm_api_keys)
![Code Climate issues](https://img.shields.io/codeclimate/issues/joshuasundance-swca/detect_llm_api_keys)
![Code Climate technical debt](https://img.shields.io/codeclimate/tech-debt/joshuasundance-swca/detect_llm_api_keys)
[![coverage](coverage.svg)](./COVERAGE.md)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json)](https://github.com/charliermarsh/ruff)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[![security: bandit](https://img.shields.io/badge/security-bandit-yellow.svg)](https://github.com/PyCQA/bandit)
![Known Vulnerabilities](https://snyk.io/test/github/joshuasundance-swca/detect_llm_api_keys/badge.svg)


🤖 This README was written by GPT-4. 🤖


## Introduction
`detect_llm_api_keys` is a vital tool for Python developers, especially those working with large language models (LLMs). It's a pre-commit hook that efficiently scans your Python files to detect and prevent the accidental committing of LLM API keys, enhancing the security of your projects.

## Features
- **Efficient API Key Detection**: Scans for keys from major providers like `Anthropic`, `Anyscale`, `Microsoft Azure`, `LangChain`, `OpenAI`, and `Mistral AI`.
- **Easy Integration**: Seamlessly integrates with your existing Python projects.
- **Support for Various API Key Patterns**: Recognizes a range of patterns, ensuring comprehensive protection.
- **Compatibility with nosec and noqa Comments**: Respects your code's existing security annotations.

## Getting Started
1. **Installation**: Add `detect_llm_api_keys` to your `.pre-commit-config.yaml` file.
2. **Configuration**: Customize the settings as per your project requirements.
3. **Usage**: Automatically scans files upon each commit, flagging potential API key exposures.

## Usage
To use `detect_llm_api_keys` in your project, update your `.pre-commit-config.yaml` as follows:

```.pre-commit-config.yaml
repos:
-   repo: https://github.com/joshuasundance-swca/detect_llm_api_keys
    rev: "0.0.3"
    hooks:
    -   id: detect-llm-api-keys
```

## Collaboration and Contributions
Feedback, suggestions, and contributions are highly welcomed to enhance `detect_llm_api_keys`. Please feel free to open issues or submit pull requests on GitHub.

## License
Distributed under the MIT License. See `LICENSE` for more information.

## Acknowledgements
Special thanks to the Python and Open Source communities for their invaluable support and contributions.
