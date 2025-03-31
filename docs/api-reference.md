# API Reference

## OpenRouter Model Selector API

### Class: `Pipe`

The main class that implements the OpenWebUI pipe function interface.

#### Attributes

- `type` (str): Set to "manifold" to indicate this pipe represents multiple models.
- `id` (str): Unique identifier for the pipe, set to "openrouter_model_selector".
- `name` (str): Display name for the pipe, set to "OpenRouter Model Selector".
- `valves` (Valves): Configuration options for the pipe.
- `_models_cache` (List[Dict[str, str]] | None): Cache for storing fetched models.
- `_last_fetch_time` (float): Timestamp of the last model fetch.
- `_cache_duration` (int): Duration in seconds for which the cache is valid (default: 300).

#### Methods

##### `__init__(self)`

Initializes the pipe with default values and environment variables.

##### `_get_headers(self) -> Dict[str, str]`

Generates headers for OpenRouter API requests.

**Returns:**
- Dictionary of HTTP headers including Authorization and Content-Type.

**Raises:**
- ValueError: If OPENROUTER_API_KEY is not set.

##### `_format_model_id(self, model_id: str) -> str`

Formats the model ID to be compatible with OpenRouter API by removing prefixes.

**Parameters:**
- `model_id` (str): The model ID to format.

**Returns:**
- Formatted model ID string.

##### `_handle_response(self, response: requests.Response) -> dict`

Processes API response and handles errors.

**Parameters:**
- `response` (requests.Response): The HTTP response object.

**Returns:**
- Parsed JSON response as a dictionary.

**Raises:**
- Exception: If HTTP error occurs or response contains invalid JSON.

##### `get_openrouter_models(self) -> List[Dict[str, str]]`

Fetches and filters available models from OpenRouter API.

**Returns:**
- List of dictionaries containing model information (id and name).

##### `pipes(self) -> List[Dict[str, str]]`

Returns list of available models for the dropdown.

**Returns:**
- List of dictionaries containing model information (id and name).

##### `pipe(self, body: dict) -> Union[str, Generator[str, None, None]]`

Processes the request to the selected model.

**Parameters:**
- `body` (dict): Request body containing model, messages, and other parameters.

**Returns:**
- String response for non-streaming requests or Generator for streaming requests.

**Raises:**
- KeyError: If required keys are missing from the request body.
- Exception: For other errors during processing.

##### `stream_response(self, payload: dict, retries: int = 3) -> Generator[str, None, None]`

Handles streaming responses from OpenRouter API.

**Parameters:**
- `payload` (dict): Request payload for the API.
- `retries` (int, optional): Number of retry attempts for failed requests. Defaults to 3.

**Returns:**
- Generator yielding response content chunks.

##### `get_completion(self, payload: dict, retries: int = 3) -> str`

Handles non-streaming responses from OpenRouter API.

**Parameters:**
- `payload` (dict): Request payload for the API.
- `retries` (int, optional): Number of retry attempts for failed requests. Defaults to 3.

**Returns:**
- String containing the complete response.

### Class: `Pipe.Valves`

Configuration options for the OpenRouter Model Selector pipe.

#### Attributes

- `OPENROUTER_API_BASE_URL` (str): Base URL for the OpenRouter API. Default: "https://openrouter.ai/api/v1".
- `OPENROUTER_API_KEY` (str): API key for authenticating with OpenRouter. Default: "".
- `FREE_ONLY` (bool): When enabled, only free models will be displayed. Default: False.
- `MODEL_PREFIX` (str): Prefix to add to model names in the dropdown. Default: "OpenRouter/".
- `INCLUDE_REASONING` (bool): Request reasoning tokens from models that support it. Default: True.

## OpenRouter API Endpoints

### GET /models

Fetches available models from OpenRouter.

**Headers:**
- Authorization: Bearer {OPENROUTER_API_KEY}
- Content-Type: application/json

**Response:**
```json
{
  "data": [
    {
      "id": "model-id",
      "name": "Model Name",
      "description": "Model description",
      "context_length": 8192,
      "pricing": {
        "prompt": 0.0001,
        "completion": 0.0002
      }
    }
  ]
}
```

### POST /chat/completions

Sends a chat completion request to OpenRouter.

**Headers:**
- Authorization: Bearer {OPENROUTER_API_KEY}
- Content-Type: application/json

**Request Body:**
```json
{
  "model": "model-id",
  "messages": [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Hello, how are you?"}
  ],
  "stream": false,
  "include_reasoning": true
}
```

**Response (non-streaming):**
```json
{
  "id": "response-id",
  "object": "chat.completion",
  "created": 1679351337,
  "model": "model-id",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "I'm doing well, thank you for asking!",
        "reasoning": "The user is asking about my state, so I should respond politely."
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 23,
    "completion_tokens": 13,
    "total_tokens": 36
  }
}
```

**Response (streaming):**
A stream of server-sent events, each containing a chunk of the response.
