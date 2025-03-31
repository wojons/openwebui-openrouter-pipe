# Contributing to OpenRouter Model Selector

Thank you for your interest in contributing to the OpenRouter Model Selector for OpenWebUI! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

Please be respectful and considerate of others when contributing to this project. We aim to foster an inclusive and welcoming community.

## How to Contribute

There are many ways to contribute to this project:

1. **Reporting Bugs**: If you find a bug, please create an issue with a detailed description of the problem, steps to reproduce, and your environment.

2. **Suggesting Enhancements**: Have an idea for a new feature or improvement? Open an issue with the "enhancement" label.

3. **Code Contributions**: Want to fix a bug or add a feature? Follow the steps below.

4. **Documentation**: Help improve or translate the documentation.

5. **Testing**: Help test the plugin with different OpenWebUI versions and configurations.

## Development Workflow

### Setting Up Your Development Environment

1. Fork the repository on GitHub.

2. Clone your fork locally:
   ```bash
   git clone https://github.com/wojons/openwebui-openrouter-pipe.git
   cd openwebui-openrouter-pipe
   ```

3. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements-dev.txt
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

### Making Changes

1. Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes to the code.

3. Follow the code style guidelines (see the [Development Guide](docs/development.md)).

4. Add or update tests as appropriate.

5. Run the tests to make sure everything passes:
   ```bash
   pytest
   ```

6. Update documentation as necessary.

### Submitting a Pull Request

1. Commit your changes with a clear and descriptive commit message:
   ```bash
   git commit -m "Add feature: your feature description"
   ```

2. Push your branch to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

3. Go to the original repository on GitHub and create a pull request from your branch.

4. In your pull request description, explain the changes you've made and why they should be included.

5. Wait for a maintainer to review your pull request. They may ask for changes or clarification.

## Pull Request Guidelines

- Keep pull requests focused on a single feature or bug fix.
- Make sure your code passes all tests.
- Follow the code style guidelines.
- Update documentation as necessary.
- Add tests for new features or bug fixes.
- Ensure your branch is up to date with the main branch before submitting.

## Code Style

This project follows the [Black](https://black.readthedocs.io/) code style. We also use isort for import sorting and flake8 for linting.

To format your code:

```bash
# Format Python code
black src/

# Sort imports
isort src/

# Run linter
flake8 src/
```

## Testing

We use pytest for testing. To run the tests:

```bash
pytest
```

## Documentation

When adding new features or making significant changes, please update the relevant documentation:

- `README.md` for high-level overview
- `docs/usage-guide.md` for user-facing documentation
- `docs/api-reference.md` for API details
- `docs/development.md` for development information

## Issue and Pull Request Labels

We use labels to categorize issues and pull requests:

- `bug`: Something isn't working as expected
- `enhancement`: New feature or improvement
- `documentation`: Documentation-related changes
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `question`: Further information is requested

## Getting Help

If you need help with contributing, feel free to:

- Open an issue with your question
- Reach out to the maintainers

## Thank You!

Your contributions are greatly appreciated. Every contribution, no matter how small, helps make this project better!
