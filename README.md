# BatchCreator Module

A Python module for creating OpenAI Batch API `.jsonl` files with customizable parameters.

## Features

- Create structured batch requests for OpenAI's Batch API
- Configurable model, reasoning effort, and JSON schema
- Support for both structured (JSON schema) and freeform responses
- Easy entry management with add, clear, and preview functions
- Automatic file creation with proper formatting

## Installation

The module is self-contained and only requires Python's standard library. Simply import the `BatchCreator` class:

```python
from scripts.batch_creator import BatchCreator
```

## Usage

### Basic Usage

```python
from scripts.batch_creator import BatchCreator

# Create a simple batch creator
batch_creator = BatchCreator(
    model="o4-mini",                    # Default: "o4-mini"
    reasoning_effort="medium",          # Default: "medium"
    json_schema=None,                   # Default: None (no structured response)
    system_prompt="Your system prompt"  # Required
)

# Add entries
batch_creator.add_entry("request-1", "Your user prompt here")
batch_creator.add_entry("request-2", "Another user prompt")

# Save to file
batch_creator.save_to_file("data/my_batch.jsonl")
```

### With JSON Schema (Structured Responses)

```python
# Define your JSON schema
schema = {
    "name": "my_schema",
    "schema": {
        "type": "object",
        "properties": {
            "answer": {"type": "string"},
            "confidence": {"type": "number"}
        },
        "required": ["answer", "confidence"]
    },
    "strict": True
}

# Create batch creator with schema
batch_creator = BatchCreator(
    model="o4-mini",
    reasoning_effort="medium",
    json_schema=schema,
    system_prompt="Provide structured responses"
)
```

### Batch Management

```python
# Check entry count
print(f"Current entries: {batch_creator.get_entry_count()}")

# Preview an entry
entry = batch_creator.preview_entry(0)  # Preview first entry
print(f"Custom ID: {entry['custom_id']}")

# Clear all entries
batch_creator.clear_entries()
```

## Constructor Parameters

- `model` (str): OpenAI model to use (default: "o4-mini")
- `reasoning_effort` (str): Reasoning effort level (default: "medium")
- `json_schema` (Optional[Dict]): JSON schema for structured responses. If None, `response_format` is omitted
- `system_prompt` (str): System prompt for all requests

## Methods

### `add_entry(index: str, user_prompt: str)`

Add a single entry to the batch.

**Parameters:**

- `index`: Custom ID for the request
- `user_prompt`: User prompt content

### `save_to_file(file_path: str)`

Save all entries to a `.jsonl` file. Creates directories if they don't exist.

### `clear_entries()`

Remove all entries from the batch.

### `get_entry_count() -> int`

Get the number of entries currently in the batch.

### `preview_entry(index: int = 0) -> Dict`

Preview a specific entry by index.

## Output Format

The generated `.jsonl` file follows OpenAI's Batch API format:

### With JSON Schema

```json
{
  "custom_id": "request-1",
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "o4-mini",
    "seed": 334,
    "reasoning_effort": "medium",
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        /* your schema */
      }
    },
    "messages": [
      { "role": "system", "content": "System prompt" },
      { "role": "user", "content": "User prompt" }
    ]
  }
}
```

### Without JSON Schema

```json
{
  "custom_id": "request-1",
  "method": "POST",
  "url": "/v1/chat/completions",
  "body": {
    "model": "o4-mini",
    "seed": 334,
    "reasoning_effort": "medium",
    "messages": [
      { "role": "system", "content": "System prompt" },
      { "role": "user", "content": "User prompt" }
    ]
  }
}
```

## Examples

See `example_usage.py` for comprehensive examples including:

- Creating batches with JSON schema
- Creating batches without JSON schema
- Batch management operations

## Integration with main.py

The `BatchCreator` is imported and available in `main.py`:

```python
from scripts.batch_creator import BatchCreator

def main():
    # Use BatchCreator here
    batch_creator = BatchCreator(system_prompt="Your prompt")
    # ... rest of your code
```
