"""
title: OpenRouter Model Selector
author: Cline
version: 0.1.1
license: MIT
description: Integrates OpenRouter model selection into OpenWebUI with a FREE_ONLY filter option
"""

import os
import json
import requests
import time
from typing import List, Dict, Union, Generator, Optional
from pydantic import BaseModel, Field

class Pipe:
    class Valves(BaseModel):
        """Configuration for OpenRouter API."""
        OPENROUTER_API_BASE_URL: str = Field(
            default="https://openrouter.ai/api/v1",
            description="Base URL for the OpenRouter API"
        )
        OPENROUTER_API_KEY: str = Field(
            default="",
            description="Your OpenRouter API key for authentication"
        )
        FREE_ONLY: bool = Field(
            default=False,
            description="When enabled, only free models will be displayed"
        )
        MODEL_PREFIX: str = Field(
            default="OpenRouter/",
            description="Prefix to add to model names in the dropdown"
        )
        INCLUDE_REASONING: bool = Field(
            default=True,
            description="Request reasoning tokens from models that support it"
        )

    def __init__(self):
        self.type = "manifold"  # Indicates this pipe can represent multiple models
        self.id = "openrouter"  # Shorter ID to avoid long prefixes
        self.name = "OpenRouter"  # Shorter name to avoid redundancy
        self.valves = self.Valves(
            **{
                "OPENROUTER_API_KEY": os.getenv("OPENROUTER_API_KEY", ""),
                "FREE_ONLY": os.getenv("FREE_ONLY", "false").lower() == "true",
            }
        )
        self._models_cache = None
        self._last_fetch_time = 0
        self._cache_duration = 300  # Cache models for 5 minutes

    def _get_headers(self) -> Dict[str, str]:
        """Generate headers for OpenRouter API requests."""
        if not self.valves.OPENROUTER_API_KEY:
            raise ValueError("OPENROUTER_API_KEY is not set")
        
        return {
            "Authorization": f"Bearer {self.valves.OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://openwebui.com/",
            "X-Title": "Open WebUI via OpenRouter Pipe"
        }

    def _format_model_id(self, model_id: str) -> str:
        """Format the model ID to be compatible with OpenRouter API."""
        # Remove prefixes if present
        if model_id.startswith(f"{self.id}."):
            model_id = model_id[len(f"{self.id}.") :]
        elif "." in model_id:
            # Handle any other prefixes with dot notation
            model_id = model_id.split(".", 1)[1]
        return model_id

    def _handle_response(self, response: requests.Response) -> dict:
        """Process API response and handle errors."""
        try:
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP Error {response.status_code}"
            try:
                error_data = response.json()
                if "error" in error_data:
                    if isinstance(error_data["error"], dict) and "message" in error_data["error"]:
                        error_message += f": {error_data['error']['message']}"
                    else:
                        error_message += f": {error_data['error']}"
            except:
                error_message += f": {response.text[:500]}"
            raise Exception(error_message)
        except ValueError:
            raise Exception(f"Invalid JSON response: {response.text[:500]}")

    def get_openrouter_models(self) -> List[Dict[str, str]]:
        """Fetch and filter available models from OpenRouter API."""
        current_time = time.time()
        
        # Return cached models if available and not expired
        if (self._models_cache is not None and 
            (current_time - self._last_fetch_time) < self._cache_duration):
            return self._models_cache
        
        url = f"{self.valves.OPENROUTER_API_BASE_URL}/models"
        try:
            response = requests.get(url, headers=self._get_headers(), timeout=10)
            models_data = self._handle_response(response).get("data", [])
            
            # Apply FREE_ONLY filter if enabled
            if self.valves.FREE_ONLY:
                models_data = [
                    model for model in models_data
                    if "free" in model.get("id", "").lower()
                ]
            
            # Format models for display - use MODEL_PREFIX only if it's not empty
            formatted_models = []
            for model in models_data:
                model_name = model.get('name', model.get('id', 'Unknown Model'))
                display_name = f"{self.valves.MODEL_PREFIX}{model_name}" if self.valves.MODEL_PREFIX else model_name
                formatted_models.append({
                    "id": model.get("id", "unknown"),
                    "name": display_name,
                })
            
            # Update cache
            self._models_cache = formatted_models
            self._last_fetch_time = current_time
            
            return formatted_models
        except Exception as e:
            # Return error model if fetching fails
            return [{"id": "error", "name": f"Error: {str(e)}"}]

    def pipes(self) -> List[Dict[str, str]]:
        """Return list of available models for the dropdown."""
        return self.get_openrouter_models()

    def pipe(self, body: dict) -> Union[str, Generator[str, None, None]]:
        """Process the request to the selected model."""
        try:
            # Extract model ID and format it for OpenRouter
            model = self._format_model_id(body["model"])
            messages = body["messages"]
            stream = body.get("stream", False)
            
            # Add reasoning tokens if enabled
            payload = {
                "model": model,
                "messages": messages,
                "stream": stream
            }
            
            if self.valves.INCLUDE_REASONING:
                payload["include_reasoning"] = True
            
            # Add other parameters if present
            for param in ["temperature", "top_p", "max_tokens", "presence_penalty", "frequency_penalty"]:
                if param in body:
                    payload[param] = body[param]
            
            # Process request based on streaming preference
            if stream:
                return self.stream_response(payload)
            return self.get_completion(payload)
        except KeyError as e:
            return f"Error: Missing required key in request: {e}"
        except Exception as e:
            return f"Error: {str(e)}"

    def stream_response(self, payload: dict, retries: int = 3) -> Generator[str, None, None]:
        """Handle streaming responses from OpenRouter API."""
        url = f"{self.valves.OPENROUTER_API_BASE_URL}/chat/completions"
        
        # Track if we're currently in reasoning state
        in_reasoning_state = False
        
        for attempt in range(retries):
            try:
                response = requests.post(
                    url, 
                    json=payload, 
                    headers=self._get_headers(), 
                    stream=True,
                    timeout=60
                )
                response.raise_for_status()
                
                for line in response.iter_lines():
                    if not line:
                        continue
                    
                    line_text = line.decode("utf-8")
                    if not line_text.startswith("data: "):
                        continue
                    elif line_text == "data: [DONE]":
                        # Close reasoning tag if still open
                        if in_reasoning_state:
                            yield "\n</think>\n\n"
                        break
                    
                    try:
                        chunk = json.loads(line_text[6:])
                        
                        if "choices" in chunk and chunk["choices"]:
                            choice = chunk["choices"][0]
                            
                            # Check for reasoning tokens
                            reasoning_text = None
                            if "delta" in choice and "reasoning" in choice["delta"]:
                                reasoning_text = choice["delta"]["reasoning"]
                            elif "message" in choice and "reasoning" in choice["message"]:
                                reasoning_text = choice["message"]["reasoning"]
                            
                            # Check for content tokens
                            content_text = None
                            if "delta" in choice and "content" in choice["delta"]:
                                content_text = choice["delta"]["content"]
                            elif "message" in choice and "content" in choice["message"]:
                                content_text = choice["message"]["content"]
                            
                            # Handle reasoning tokens
                            if reasoning_text:
                                # If first reasoning token, output opening tag
                                if not in_reasoning_state:
                                    yield "<think>\n"
                                    in_reasoning_state = True
                                
                                # Output the reasoning token
                                yield reasoning_text
                            
                            # Handle content tokens
                            if content_text:
                                # If transitioning from reasoning to content, close the thinking tag
                                if in_reasoning_state:
                                    yield "\n</think>\n\n"
                                    in_reasoning_state = False
                                
                                # Output the content
                                yield content_text
                    except json.JSONDecodeError:
                        continue
                
                # If we're still in reasoning state at the end, close the tag
                if in_reasoning_state:
                    yield "\n</think>\n\n"
                
                return  # Success, exit the retry loop
            
            except requests.RequestException as e:
                if response.status_code == 429 and attempt < retries - 1:
                    # Rate limited, exponential backoff
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    yield f"Error: Request failed: {str(e)}"
                    return

    def get_completion(self, payload: dict, retries: int = 3) -> str:
        """Handle non-streaming responses from OpenRouter API."""
        url = f"{self.valves.OPENROUTER_API_BASE_URL}/chat/completions"
        
        for attempt in range(retries):
            try:
                response = requests.post(
                    url, 
                    json=payload, 
                    headers=self._get_headers(),
                    timeout=60
                )
                data = self._handle_response(response)
                
                # Extract content and reasoning if present
                if not data.get("choices") or len(data["choices"]) == 0:
                    return ""
                
                choice = data["choices"][0]
                message = choice.get("message", {})
                
                content = message.get("content", "")
                reasoning = message.get("reasoning", "")
                
                # If we have both reasoning and content
                if reasoning and content:
                    return f"<think>\n{reasoning}\n</think>\n\n{content}"
                elif reasoning:  # Only reasoning, no content (unusual)
                    return f"<think>\n{reasoning}\n</think>\n\n"
                elif content:  # Only content, no reasoning
                    return content
                return ""
                
            except requests.RequestException as e:
                if response.status_code == 429 and attempt < retries - 1:
                    # Rate limited, exponential backoff
                    wait_time = 2 ** attempt
                    time.sleep(wait_time)
                else:
                    return f"Error: Request failed: {str(e)}"
