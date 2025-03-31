# Development Guide

This guide provides information for developers who want to contribute to or modify the OpenRouter Model Selector pipe function.

## Project Structure

```
openwebui-openrouter-pipe/
├── docs/                     # Documentation
│   ├── images/               # Documentation images
│   ├── api-reference.md      # API reference documentation
│   ├── development.md        # Development guide (this file)
│   └── usage-guide.md        # User guide
├── src/                      # Source code
│   └── plugins/              # OpenWebUI plugins
│       └── openrouter_model_selector.py  # Main pipe function implementation
├── .gitignore                # Git ignore file
├── LICENSE                   # MIT license
├── README.md                 # Project overview
├── requirements-dev.txt      # Development dependencies
├── requirements.txt          # Runtime dependencies
└── setup.py                  # Package setup script
```

## Development Environment Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/openwebui-openrouter-pipe.git
   cd openwebui-openrouter-pipe
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

4. Install the package in development mode:
   ```bash
   pip install -e .
   ```

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

## Adding Features

### Adding a New Valve

To add a new configuration option to the pipe function:

1. Add the new valve to the `Pipe.Valves` class in `src/plugins/openrouter_model_selector.py`:

```python
class Valves(BaseModel):
    # Existing valves...
    NEW_VALVE: str = Field(
        default="default_value",
        description="Description of the new valve"
    )
```

2. Use the new valve in your code:

```python
def some_method(self):
    new_value = self.valves.NEW_VALVE
    # Use the value...
```

### Modifying the Model Filtering Logic

The model filtering logic is in the `get_openrouter_models` method. To modify it:

1. Locate the method in `src/plugins/openrouter_model_selector.py`
2. Update the filtering logic as needed:

```python
# Example: Add a new filter for context length
if self.valves.MIN_CONTEXT_LENGTH:
    models_data = [
        model for model in models_data
        if model.get("context_length", 0) >= self.valves.MIN_CONTEXT_LENGTH
    ]
```

### Adding Support for New API Endpoints

To add support for new OpenRouter API endpoints:

1. Add a new method to the `Pipe` class:

```python
def call_new_endpoint(self, param1, param2):
    url = f"{self.valves.OPENROUTER_API_BASE_URL}/new-endpoint"
    payload = {"param1": param1, "param2": param2}
    
    response = requests.post(
        url, 
        json=payload, 
        headers=self._get_headers(),
        timeout=30
    )
    return self._handle_response(response)
```

2. Use the new method in your code as needed.

## Debugging

For debugging, you can enable debug output by setting the `DEBUG` constant to `True` at the top of the file:

```python
DEBUG = True
```

This will print detailed information about API requests and responses.

## Building and Distribution

To build the package for distribution:

```bash
python setup.py sdist bdist_wheel
```

This will create distribution packages in the `dist/` directory.

## Documentation

We use Markdown for documentation. When adding new features, please update the relevant documentation files:

- `README.md` for high-level overview
- `docs/usage-guide.md` for user-facing documentation
- `docs/api-reference.md` for API details
- `docs/development.md` for development information

## Pull Request Process

1. Ensure your code follows the project's style guidelines
2. Update documentation as necessary
3. Add or update tests as appropriate
4. Make sure all tests pass
5. Submit a pull request with a clear description of the changes

## Versioning

We use [Semantic Versioning](https://semver.org/) for version numbers:

- MAJOR version for incompatible API changes
- MINOR version for backwards-compatible functionality additions
- PATCH version for backwards-compatible bug fixes
