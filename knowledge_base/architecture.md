# System Architecture

## Overview

The Local Markdown Knowledge Base MCP Server is a Python-based implementation of the Model Context Protocol. It runs as a local process on the developer's machine and communicates with MCP clients (such as Claude Desktop) over standard input/output streams using JSON-RPC 2.0 framing.

The server is intentionally narrow in scope. It indexes a single configured directory of Markdown files and exposes that directory to an LLM client through two tools: `search_knowledge_base` and `read_doc_file`. There is no network listener, no authentication layer, and no persistent database. State is rebuilt on each invocation from the filesystem.

## Components

The codebase is organized into three primary modules. The transport layer handles MCP message framing and lifecycle events (initialize, list_tools, call_tool, shutdown). The indexer module walks the configured directory, reads each `.md` file into memory, and builds a simple inverted index keyed on lowercased word tokens. The tools module implements the two exposed capabilities and is the only place that touches user-provided arguments after they have been validated against the declared JSON Schemas.

## Request Flow

When a client invokes `search_knowledge_base`, the request arrives at the transport layer, is dispatched to the tools module, and the query string is tokenized using the same rules applied during indexing. Matching documents are scored by term frequency, ranked, and the top results are returned as a list of filenames with short text excerpts. A `read_doc_file` call is simpler: the requested filename is resolved against the configured root directory, the resolved path is verified to still sit inside that root, and the raw file contents are returned to the caller.

## Security Boundaries

Path traversal is the most realistic threat against a server of this shape. Every filename supplied by the client is joined to the configured root and then canonicalized; if the canonical path escapes the root, the request is rejected before any file I/O occurs. The server never executes shell commands, never evaluates Markdown content, and never follows symbolic links that point outside the configured root.
