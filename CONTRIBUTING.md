# Contributing to Kakhoot

Thank you for your interest in contributing to Kakhoot! We welcome contributions from everyone. This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and inclusive in all interactions. We are committed to providing a welcoming and inspiring community for all.

## How to Contribute

### Reporting Bugs

Before creating a bug report, please check the issue list as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

- **Use a clear and descriptive title**
- **Describe the exact steps which reproduce the problem**
- **Provide specific examples to demonstrate the steps**
- **Describe the behavior you observed after following the steps**
- **Explain which behavior you expected to see instead and why**
- **Include screenshots if possible**
- **Include your Python version and OS information**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

- **Use a clear and descriptive title**
- **Provide a step-by-step description of the suggested enhancement**
- **Provide specific examples to demonstrate the steps**
- **Describe the current behavior and expected behavior**
- **Explain why this enhancement would be useful**

### Pull Requests

- Fill in the required template
- Follow the Python styleguide (PEP 8)
- Include appropriate test cases
- Update documentation as needed
- End all files with a newline

## Development Setup

1. **Fork** the repository
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/kakhoot.git
   cd kakhoot
   ```
3. **Create** a new branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make** your changes
5. **Install** in editable mode:
   ```bash
   pip install -e .
   ```
6. **Test** your changes (see "Testing" section below)
7. **Commit** your changes:
   ```bash
   git commit -m "Add your commit message"
   ```
8. **Push** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```
9. **Open** a Pull Request

## Styleguides

### Python Style Guide

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use meaningful variable and function names
- Add comments for complex logic
- Use type hints for all function arguments and return values
- Use `async` and `await` for asynchronous operations

Example:
```python
# Good
async def fetch_data(url: str) -> dict:
    """Fetches data from a given URL asynchronously."""
    # ... implementation ...
    return {"status": "success"}

# Avoid
def get_data(u):
    # ... implementation ...
    return {}
```

## Commit Message Guidelines

- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
feat: Add OpenAI model integration

- Implement OpenAIModel class in kakhoot/models.py
- Update Agent to support OpenAI tool calling format
- Add example usage in CLI

Fixes #1, #2
```

## Testing (Coming Soon)

We aim for comprehensive test coverage. Please include tests for your changes.

- Use `pytest` for unit and integration tests.
- Run tests with `pytest` from the project root.

## Documentation

- Update `README.md` if you add new features or change core functionality.
- Add docstrings to all new modules, classes, and functions.
- Update `CONTRIBUTING.md` if you change the contribution process.
- Keep documentation clear and concise.

## Feature Ideas

Here are some features we'd love to see contributed:

- **New Model Integrations**: Add support for more LLM providers (e.g., Google Gemini, Cohere).
- **Advanced Tooling**: Implement more sophisticated tool parameter parsing (e.g., Pydantic validation).
- **Agent Orchestration**: Add support for multi-agent systems and complex workflows.
- **CLI Enhancements**: Improve the CLI with more features and a richer user experience.
- **Examples & Tutorials**: Provide more diverse examples and detailed tutorials.
- **Performance Optimizations**: Further enhance the speed and efficiency of the framework.
- **Web UI**: A simple web interface for monitoring agents.

## Questions?

Feel free to open an issue with the label `question` if you have any questions about contributing.

## License

By contributing to Kakhoot, you agree that your contributions will be licensed under its MIT License.

---

Thank you for contributing! 🎉
