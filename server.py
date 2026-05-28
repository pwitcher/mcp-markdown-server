import os
from fastmcp import FastMCP

# Initialize the FastMCP server with a descriptive name for the LLM client
mcp = FastMCP("Markdown Knowledge Base")

# Establish the path to our local target folder from Step 2
KB_PATH = os.path.join(os.path.dirname(__file__), "knowledge_base")

@mcp.tool()
def list_documents() -> list[str]:
    """
    Retrieves a list of all available Markdown documentation filenames (.md) 
    stored in the local knowledge base. Use this tool first to discover what 
    files are available to read.
    """
    if not os.path.exists(KB_PATH):
        return []
    return [f for f in os.listdir(KB_PATH) if f.endswith('.md')]


@mcp.tool()
def search_knowledge_base(keyword: str) -> list[dict]:
    """
    Searches the internal text of all local Markdown documents for a specific keyword.
    Use this tool when a user asks about a general concept or feature, but you do 
    not yet know the specific filename containing that information.
    
    Arguments:
    keyword: A single search term or phrase (e.g., 'API', 'architecture', 'CI/CD'). 
             Do NOT pass full conversational sentences.
    """
    results = []
    if not os.path.exists(KB_PATH):
        return results

    # Standardize keyword for case-insensitive search
    search_term = keyword.lower()

    for filename in os.listdir(KB_PATH):
        if filename.endswith('.md'):
            file_path = os.path.join(KB_PATH, filename)
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if search_term in content.lower():
                        # Extract a small snippet around the match for preview
                        idx = content.lower().find(search_term)
                        start = max(0, idx - 40)
                        end = min(len(content), idx + len(search_term) + 60)
                        snippet = f"...{content[start:end]}..."
                        
                        results.append({
                            "filename": filename,
                            "preview_snippet": snippet.replace('\n', ' ')
                        })
            except Exception as e:
                # Silently catch file read errors so the JSON-RPC stream doesn't break
                continue
                
    return results


@mcp.tool()
def read_document(filename: str) -> str:
    """
    Reads and returns the complete, raw Markdown text content of a specific file.
    Use this tool ONLY after identifying the exact filename via list_documents 
    or search_knowledge_base.
    
    Arguments:
    filename: The exact name of the target file, including the '.md' extension 
              (e.g., 'architecture.md'). Do NOT guess or pass raw paths.
    """
    # Prevent directory traversal vulnerability attempts
    safe_filename = os.path.basename(filename)
    file_path = os.path.join(KB_PATH, safe_filename)

    if not os.path.exists(file_path):
        return f"Error: The requested file '{filename}' does not exist in the knowledge base."

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error: Failed to read file content due to system permissions. Details: {str(e)}"


if __name__ == "__main__":
    mcp.run()