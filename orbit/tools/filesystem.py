import os
import glob
from pathlib import Path

def file_search(pattern: str, path: str = ".") -> str:
    """Searches for files matching a pattern."""
    try:
        search_path = os.path.join(path, f"**/{pattern}")
        files = glob.glob(search_path, recursive=True)
        if not files:
            return "No files found."
        return "\n".join(files[:20]) # Limit to 20 to avoid crashing the LLM context
    except Exception as e:
        return f"Search failed: {e}"

def file_read(path: str) -> str:
    """Reads the contents of a file."""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            # Truncate if it's too massive
            if len(content) > 10000:
                return content[:10000] + "\n...[CONTENT TRUNCATED]..."
            return content
    except Exception as e:
        return f"Read failed: {e}"

def file_create(path: str, content: str = "") -> str:
    """Creates a new file with optional content."""
    try:
        # Create directories if they don't exist
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return f"Successfully created {path}"
    except Exception as e:
        return f"Creation failed: {e}"

def file_write(path: str, content: str) -> str:
    """Overwrites an existing file with new content."""
    # For MVP, write and create act similarly, but we separate them for security rules
    return file_create(path, content)