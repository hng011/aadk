# AADK - AI Agent Development Kit Demo

A comprehensive showcase of AI agents built with Google ADK (Agent Development Kit), demonstrating various agent architectures and integrations including MCP tools, A2A protocol, BigQuery, and multi-agent workflows.

## Overview

This project demonstrates 5 different AI agent implementations, each showcasing different capabilities of the Google ADK framework:

- **MCP Agent** - Multi-tool integration using Model Context Protocol
- **ArXiv Agent** - Sequential multi-agent workflow for research paper analysis
- **BigQuery Agent** - Database querying with vision capabilities
- **A2A Agent** - Agent-to-Agent communication across different languages
- **Sustainability Research Agent** - Parallel research execution and synthesis

## Agents

### 🔧 MCP Agent
An Agent Navigator that integrates with multiple open-source tools via Model Context Protocol (MCP).

**Connected Tools:**
- GitHub Copilot MCP
- Hugging Face MCP
- Context7 MCP

**Capabilities:** Repository search, model exploration, and contextual information retrieval with multilingual support.

### 📄 ArXiv Agent
A sequential agent workflow that searches and reviews academic papers from arXiv.

**Architecture:**
- `scraper_agent` - Fetches latest papers (max 7) based on domain
- `reviewer_agent` - Analyzes and reviews paper content

**Output:** Structured paper summaries with PDF links and analysis.

### 💾 BigQuery Agent
A dual-mode intelligent assistant combining data analytics with device assessment.

**Modes:**
1. **Senior Data Architect** - Writes optimized GoogleSQL queries
2. **Device Assessment Specialist** - Grades and values physical devices (iPhone trade-ins)

**Features:**
- BigQuery integration with write protection
- Custom phone grading tool with vision capabilities
- Context-aware routing logic

### 🎲 A2A Agent
Demonstrates Agent-to-Agent (A2A) protocol communication between Python and Go agents.

**Components:**
- Python agent orchestrator
- Remote Go agent (`check_prime_agent`) for prime number verification
- Dice rolling sub-agent

**Use Case:** Cross-language agent collaboration and remote agent integration.

### 🌱 Sustainability Research Agent
Parallel research agent that investigates multiple sustainability topics simultaneously.

**Research Topics:**
- Renewable Energy
- Electric Vehicle Technology
- Carbon Capture Methods

**Architecture:** Uses `ParallelAgent` to run research tasks concurrently, then merges results.

## Project Structure

```
aadk/
├── agents/
│   ├── a2a_agent/           # Agent-to-Agent communication
│   │   └── remote_a2a/
│   │       └── check_prime_agent/  # Go-based remote agent
│   ├── arxiv_agent/         # Sequential paper research
│   │   └── sub_agents/
│   ├── bq_agent/            # BigQuery database agent
│   │   ├── prompts/
│   │   └── tools/
│   ├── mcp_agent/           # MCP tool integrations
│   └── sustainability_research_agent/  # Parallel research
├── shared/
│   └── config.py           # Shared configuration
├── pyproject.toml
├── Makefile
└── README.md
```

## Requirements

- Python >= 3.12
- Go (for A2A remote agent)
- Google Cloud Project with BigQuery access

## Installation

### Option 1: Using uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver.

1. **Install uv**
```bash
# On Linux/Mac
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

2. **Clone and setup**
```bash
git clone <repository-url>
cd aadk
```

3. **Create virtual environment and install dependencies**
```bash
uv venv
source .venv/bin/activate  # On Linux/Mac
uv pip install -e .
```

### Option 2: Using pip

1. **Clone the repository**
```bash
git clone <repository-url>
cd aadk
```

2. **Create virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Linux/Mac
```

3. **Install dependencies**
```bash
pip install -e .
```

### Configuration

4. **Configure environment variables**
Create a `.env` file with required credentials:
```bash
# API Tokens
GITHUB_TOKEN=your_github_token
HUGGING_FACE_TOKEN=your_hf_token
NOTION_TOKEN=your_notion_token
CONTEXT7_TOKEN=your_context7_token

# Google Cloud
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_CLOUD_PROJECT=your_project_id
GOOGLE_CLOUD_LOCATION=your_location

# BigQuery
BQ_DATASET_NAME=your_dataset
BQ_DATASET_LOCATION=your_location
BQ_TABLE=your_table
BQ_TUKERINAJA_TABLE=your_table

# GCS (if needed)
GCS_BUCKET_NAME=your_bucket
GCS_BLOB_NAME=your_blob

# Model
MODEL_ID=gemini-2.0-flash-001
```

## Usage

### Start All Agents

```bash
make start
```

This will:
1. Start the Go-based remote A2A agent
2. Launch the ADK web interface for all agents

### Run Individual Agents

Using the ADK CLI:
```bash
# Run specific agent
adk agent run agents/mcp_agent

# Run with web interface
adk web agents/mcp_agent
```

## Dependencies

**Core:**
- `google-adk[a2a]` - Google Agent Development Kit
- `a2a-sdk[all]` - Agent-to-Agent SDK
- `langchain` - LLM framework
- `langchain-google-genai` - Google Gemini integration

**Data & Processing:**
- `pandas` - Data manipulation
- `google-cloud-bigquery` - BigQuery client
- `db-dtypes` - Database type handling

**Utilities:**
- `bs4` - Web scraping
- `pypdf` - PDF processing

## Key Features

✅ **Multi-Agent Architectures** - Sequential, Parallel, and Remote agent patterns  
✅ **MCP Integration** - Model Context Protocol for tool interoperability  
✅ **Cross-Language A2A** - Python-Go agent communication  
✅ **Vision Capabilities** - Multimodal phone grading  
✅ **BigQuery Integration** - Secure database querying  
✅ **Research Automation** - Parallel web research and synthesis  

## License

Apache License 2.0 (see agent files for full license text)

## Architecture Patterns

| Agent | Pattern | Communication |
|-------|---------|---------------|
| MCP Agent | Single Agent | HTTP/MCP |
| ArXiv Agent | Sequential | Internal |
| BQ Agent | Single Agent | BigQuery API |
| A2A Agent | Remote/Hybrid | A2A Protocol |
| Sustainability Agent | Parallel + Sequential | Internal |

## Development

**Adding a new agent:**
1. Create agent directory under `agents/`
2. Implement `agent.py` with `root_agent` export
3. Add `__init__.py` with settings import
4. Configure in shared settings if needed

**Agent Template:**
```python
from google.adk.agents import Agent

root_agent = Agent(
    name="my_agent",
    model="gemini-2.0-flash-001",
    instruction="Your system instruction",
    tools=[],
)
```

---

Built with [Google ADK](https://google.github.io/adk-docs/) 🚀
