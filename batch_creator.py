import json
from typing import Optional, Dict, Any, List
from pathlib import Path


class BatchCreator:
    """
    A class for creating OpenAI Batch API .jsonl files with customizable parameters.
    
    This class allows you to create batch requests for the OpenAI API with the following structure:
    {
        "custom_id": "INDEX", 
        "method": "POST", 
        "url": "/v1/chat/completions", 
        "body": {
            "model": "MODEL", 
            "seed": 334, 
            "reasoning_effort": "EFFORT", 
            "response_format": {"type": "json_schema", "json_schema": {JSON_SCHEMA}}, 
            "messages": [
                {"role": "system", "content": "SYSTEM PROMPT"}, 
                {"role": "user", "content": "USER PROMPT"}
            ]
        }
    }
    """
    
    def __init__(
        self,
        model: str = "o4-mini",
        reasoning_effort: str = "medium",
        json_schema: Optional[Dict[str, Any]] = None,
        system_prompt: str = ""
    ):
        """
        Initialize the BatchCreator with configurable parameters.
        
        Args:
            model (str): The OpenAI model to use (default: "o4-mini")
            reasoning_effort (str): The reasoning effort level (default: "medium")
            json_schema (Optional[Dict[str, Any]]): JSON schema for response format.
                                                   If None, response_format will be omitted.
            system_prompt (str): The system prompt to use for all requests
        """
        self.model = model
        self.reasoning_effort = reasoning_effort
        self.json_schema = json_schema
        self.system_prompt = system_prompt
        self.entries: List[Dict[str, Any]] = []
    
    def add_entry(self, index: str, user_prompt: str) -> None:
        """
        Add a single entry to the batch.
        
        Args:
            index (str): The custom_id for this request
            user_prompt (str): The user prompt content
        """
        # Build the basic body structure
        body = {
            "model": self.model,
            "seed": 334,
            "reasoning_effort": self.reasoning_effort,
            "messages": [
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        }
        
        # Add response_format only if json_schema is provided
        if self.json_schema is not None:
            body["response_format"] = {
                "type": "json_schema",
                "json_schema": self.json_schema
            }
        
        # Create the complete entry
        entry = {
            "custom_id": index,
            "method": "POST",
            "url": "/v1/chat/completions",
            "body": body
        }
        
        self.entries.append(entry)
    
    def save_to_file(self, id: str) -> None:
        """
        Save all entries to a .jsonl file.
        
        Args:
            id (str): Identifier for the batch, used to name the output file
        """
        file_path = Path(__file__).parent.parent / f"data/batches/batch_{id}.jsonl"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            for entry in self.entries:
                f.write(json.dumps(entry, ensure_ascii=False) + '\n')
    
    def clear_entries(self) -> None:
        """Clear all entries from the batch."""
        self.entries.clear()
    
    def get_entry_count(self) -> int:
        """Get the number of entries currently in the batch."""
        return len(self.entries)
    
    def preview_entry(self, index: int = 0) -> Dict[str, Any]:
        """
        Preview a specific entry by index.
        
        Args:
            index (int): Index of the entry to preview (default: 0)
            
        Returns:
            Dict[str, Any]: The entry at the specified index
            
        Raises:
            IndexError: If the index is out of range
        """
        if index >= len(self.entries):
            raise IndexError(f"Index {index} is out of range. Only {len(self.entries)} entries exist.")
        return self.entries[index]
