# Developer Onboarding

## Prerequisites

You will need Python 3.11 or newer and the `uv` package manager installed locally. On Windows, install `uv` through the official installer or via `winget install astral-sh.uv`. On macOS and Linux, the recommended path is the standalone installer script published by Astral. Verify the installation by running `uv --version` from a fresh terminal session before continuing.

You will also need an MCP-aware client to talk to the server. Claude Desktop is the reference client used throughout this guide, but any client that speaks MCP over stdio will work. If you plan to extend the server, a working editor with Python language support (VS Code, PyCharm, or Neovim with pyright) will make the experience considerably better.

## Initial Setup

Clone the repository, change into the project directory, and run `uv sync` to create a virtual environment and install the locked dependencies. This step reads `pyproject.toml` and `uv.lock` and produces a `.venv` folder at the repository root. Activate the environment with `.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on macOS and Linux.

After the environment is active, run `python main.py --help` to confirm that the server starts and prints its command-line options. The most important option is `--root`, which points the server at the directory of Markdown files it should index. If no root is provided, the server defaults to the `knowledge_base/` directory next to `main.py`.

## Wiring Up Claude Desktop

Open your `claude_desktop_config.json` file. On Windows this lives under `%APPDATA%\Claude\`, and on macOS it lives under `~/Library/Application Support/Claude/`. Add an entry under `mcpServers` that names the server, points at the Python interpreter from your virtual environment, and passes the absolute path to `main.py` along with the desired `--root` argument. Restart Claude Desktop after saving the file so that the new server is discovered.

Once Claude Desktop reconnects, the two tools should appear in the tool picker. Ask the model to search the knowledge base for a keyword you know exists in one of the Markdown files, and confirm that the matching filename and excerpt come back in the response. If the tool call fails, the most common cause is an incorrect path in the config file or a Python interpreter that does not match the one used to install the project dependencies.
