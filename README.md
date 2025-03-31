# OpenRouter Model Selector for OpenWebUI

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A pipe function for [OpenWebUI](https://github.com/open-webui/open-webui) that integrates [OpenRouter](https://openrouter.ai/) model selection directly into the OpenWebUI interface. This plugin allows users to access a wide range of AI models through OpenRouter's API, with support for filtering free models and handling reasoning tokens.

![OpenRouter Model Selector](docs/images/openrouter-model-selector.png)

## Features

- 🔄 **Dynamic Model List**: Fetches available models directly from OpenRouter API
- 🆓 **Free Model Filter**: Toggle to show only free models or all models
- 🧠 **Reasoning Token Support**: Properly handles `<think></think>` tags for models that support reasoning
- ⚡ **Performance Optimized**: Includes caching to reduce API calls and improve responsiveness
- 🛡️ **Robust Error Handling**: Graceful handling of API errors with retry logic

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/wojons/openwebui-openrouter-pipe.git
   ```

2. Copy the plugin file to your OpenWebUI plugins directory:
   ```bash
   cp openwebui-openrouter-pipe/src/plugins/openrouter_model_selector.py /path/to/openwebui/plugins/
   ```

3. Restart your OpenWebUI server to load the new plugin.

## Configuration

After installation, configure the pipe function through the OpenWebUI interface:

1. Navigate to the OpenWebUI settings
2. Go to the "Functions" or "Plugins" section
3. Find "OpenRouter Model Selector" in the list
4. Configure the following valves:
   - **OPENROUTER_API_KEY**: Your OpenRouter API key (required)
   - **FREE_ONLY**: Set to `true` to show only free models, `false` to show all models
   - **MODEL_PREFIX**: Customize the prefix shown before model names (default: "OpenRouter/"). Set to an empty string to remove the prefix completely.
   - **INCLUDE_REASONING**: Enable/disable reasoning token support (default: true)

## Usage

Once configured, OpenRouter models will appear in your model selection dropdown with the prefix specified in the MODEL_PREFIX valve (if any).

1. Open a chat in OpenWebUI
2. Click on the model selection dropdown
3. Look for models with the "OpenRouter/" prefix
4. Select your desired model

For more detailed usage instructions, see the [Usage Guide](docs/usage-guide.md).

## Requirements

- OpenWebUI (latest version recommended)
- Python 3.8+
- An OpenRouter API key

## Dependencies

- requests
- pydantic

## Development

### Setup Development Environment

1. Clone the repository:
   ```bash
   git clone https://github.com/wojons/openwebui-openrouter-pipe.git
   cd openwebui-openrouter-pipe
   ```

2. Install development dependencies:
   ```bash
   pip install -r requirements-dev.txt
   ```

3. Make your changes to the code

4. Test your changes with OpenWebUI

### Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [OpenWebUI](https://github.com/open-webui/open-webui) for the amazing web interface
- [OpenRouter](https://openrouter.ai/) for providing access to a wide range of AI models
