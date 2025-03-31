# OpenRouter Model Selector - Usage Guide

## Overview
The OpenRouter Model Selector is a pipe function for OpenWebUI that integrates OpenRouter's AI models directly into the OpenWebUI interface. It provides a seamless way to access a wide range of AI models through OpenRouter's API, with support for filtering free models and handling reasoning tokens.

## Setup Instructions

### 1. Installation
1. Copy the `openrouter_model_selector.py` file to your OpenWebUI plugins directory:
   ```
   /path/to/openwebui/plugins/
   ```

2. Restart your OpenWebUI server to load the new plugin.

### 2. Configuration
After installation, you'll need to configure the pipe function through the OpenWebUI interface:

1. Navigate to the OpenWebUI settings
2. Go to the "Functions" or "Plugins" section
3. Find "OpenRouter Model Selector" in the list
4. Configure the following valves:
   - **OPENROUTER_API_KEY**: Your OpenRouter API key (required)
   - **FREE_ONLY**: Set to `true` to show only free models, `false` to show all models
   - **MODEL_PREFIX**: Customize the prefix shown before model names (default: "OpenRouter/"). Set to an empty string to remove the prefix completely.
   - **INCLUDE_REASONING**: Enable/disable reasoning token support (default: true)

### 3. Obtaining an OpenRouter API Key
If you don't have an OpenRouter API key:

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Create an account or log in
3. Navigate to your account settings or API section
4. Generate a new API key
5. Copy the key and paste it into the OPENROUTER_API_KEY valve in OpenWebUI

## Using the Model Selector

### Selecting Models
Once configured, OpenRouter models will appear in your model selection dropdown with the prefix specified in the MODEL_PREFIX valve (if any).

1. Open a chat in OpenWebUI
2. Click on the model selection dropdown
3. Look for models with the "OpenRouter/" prefix
4. Select your desired model

### Filtering Free Models
To toggle between showing all models or only free models:

1. Go to the plugin settings
2. Find the FREE_ONLY valve
3. Set it to `true` to show only free models
4. Set it to `false` to show all available models
5. Save your settings
6. The model list will update automatically

### Using Reasoning Tokens
If you're using a model that supports reasoning tokens (like Claude models), and INCLUDE_REASONING is enabled:

1. The model's reasoning will be enclosed in `<think></think>` tags
2. This allows you to see the model's thought process before its final answer
3. The reasoning is separate from the final response content

## Troubleshooting

### Common Issues

#### No Models Appearing
- Verify your OpenRouter API key is correct
- Check your internet connection
- Ensure OpenWebUI has been restarted after installation

#### Authentication Errors
- Your API key may be invalid or expired
- Generate a new key from the OpenRouter website
- Update the OPENROUTER_API_KEY valve with the new key

#### Rate Limiting
- OpenRouter has rate limits based on your account tier
- The plugin includes retry logic for rate limits
- If you consistently hit rate limits, consider upgrading your OpenRouter plan

#### Model Not Working
- Not all models support all features (like reasoning tokens)
- Some models may require additional parameters
- Check the OpenRouter documentation for model-specific requirements

## Advanced Configuration

### Environment Variables
You can also configure the plugin using environment variables:

- `OPENROUTER_API_KEY`: Sets the default API key
- `FREE_ONLY`: Sets the default free model filter state

Example:
```
export OPENROUTER_API_KEY="your-api-key-here"
export FREE_ONLY="true"
```

### Customizing the API Base URL
If you need to use a different API endpoint:

1. Go to the plugin settings
2. Find the OPENROUTER_API_BASE_URL valve
3. Update it with your custom endpoint
4. Save your settings

## Support and Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [OpenWebUI Documentation](https://openwebui.com/docs)
- [OpenRouter API Reference](https://openrouter.ai/docs/api-reference)
