# GPT Plugins 4All

GPT Plugins 4All is a Python library designed to facilitate the integration of GPT and other large language models with various APIs, leveraging OpenAPI specifications. This library simplifies the process of parsing OpenAPI specs, managing different authentication methods, and dynamically interacting with APIs based on model responses.

![Demo using the AlphaVantage API with OpenAI](https://github.com/tcmartin/GPTPlugins4All/blob/master/demo/demo.gif)

## Features

- Parse and validate OpenAPI 3.1.0 specifications.
- Handle diverse authentication methods, including OAuth 2.0, Basic Auth, Header Auth, and Query Parameter Auth.
- Generate structured API representations for AI interactions.
- Dynamically construct API calls based on OpenAPI specs.
- Support OAuth2.0 flow for token acquisition and usage.

## Installation

Install GPT Plugins 4All using pip:

```bash
pip install GPTPlugins4All
```

## Quick Start

### Initializing with an OpenAPI Specification

```python
from GPTPlugins4All.config import Config

# Initialize the Config object with your OpenAPI spec
spec_string = """..."""  # Your OpenAPI spec as a string
config = Config(spec_string)
```

### Adding Authentication Methods

#### Add Basic Authentication

```python
config.add_auth_method("BASIC", {"key": "your_api_key"})
```

#### Add OAuth Configuration

```python
config.add_auth_method("OAUTH", {
    "client_id": "your_client_id",
    "client_secret": "your_client_secret",
    "auth_url": "https://example.com/auth",
    "token_url": "https://example.com/token",
    "redirect_uri": "https://yourapp.com/oauth-callback",
    "scope": "read write"
})
```

### Generating Simplified API Representations

```python
simplified_api = config.generate_simplified_api_representation()
print(simplified_api)
```
### Generate Object for use with OpenAI functions
```python
tools = config.generate_tools_representation()
```

### OAuth Flow

```python
auth_url = config.start_oauth_flow()
# Redirect the user to auth_url...

tokens = config.handle_oauth_callback(code_from_redirect)
```

### Making API Calls

```python
response = config.make_api_call("/endpoint", "GET", {"param": "value"})
```

#### Oauth
```python
url = config5.start_oauth_flow() #use this url to get code first
callback = config5.handle_oauth_callback(code)
#example
response = config5.make_api_call_by_path(path, "POST", params=your_params, user_token=callback, is_json=True)
```

## Contributing

Contributions are welcome! Please check out the [contributing guidelines](CONTRIBUTING.md).

## License

GPT Plugins 4All is released under the [MIT License](LICENSE).
