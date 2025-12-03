# JD-Match AI – An Agentic Resume–JD Analysis Framework

An intelligent multi-agent system that extracts, analyzes, and matches resumes with job descriptions using Google's Agent Development Kit and advanced AI models.

## Overview

JD-Match AI is a sophisticated Python application that leverages AI-powered agents to automate the recruitment workflow. It intelligently processes resumes and job descriptions, extracting key information and performing intelligent matching to identify qualified candidates.

## Features

- **Multi-Agent Architecture**: Modular design with specialized agents for different tasks
  - Resume Extraction Agent: Parses and structures resume data
  - Job Description Extraction Agent: Extracts and structures job requirements
  - Resume-JD Matcher Agent: Analyzes compatibility between resumes and job descriptions
- **Multi-Format Document Support**: Handles PDF, DOCX, and text documents
- **Advanced NLP**: Powered by Google Gemini AI models for intelligent text analysis
- **Structured Data Output**: Uses Pydantic models for consistent, validated data structures
- **Customizable Prompts**: Flexible instruction sets for each agent
- **Secure Configuration**: Environment variable management for API keys and credentials

## Technology Stack

- **Python 3.x**: Core language
- **Google Agent Development Kit**: Multi-agent orchestration
- **Google Generative AI**: Gemini models for NLP tasks
- **Pydantic**: Data validation and structured outputs
- **FastAPI & Uvicorn**: Web framework (if applicable)
- **PyPDF2 & python-docx**: Document parsing

## Project Structure

```
JD-Match-AI/
├── ResumeAgent/
│   ├── agent.py                 # Root agent coordinator
│   ├── dtypes_common.py         # Pydantic models for data structures
│   ├── sub/
│   │   ├── agent.py             # Sub-agent definitions
│   │   ├── prompt.py            # Agent instructions and prompts
│   │   ├── root_prompt.py       # Root agent instructions
│   │   └── util_resumeExtractor.py  # Resume extraction utilities
│   └── .env                     # Environment variables (not in repo)
├── requirements.txt             # Python dependencies
├── instructions.md              # Detailed setup guide
└── README.md                    # This file
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Google Cloud account with Generative AI API access
- pip and venv

### Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/iamnishantsaxena/JD-Match-AI.git
   cd JD-Match-AI
   ```

2. **Create and Activate Virtual Environment**
   ```bash
   python -m venv env
   
   # On macOS/Linux:
   source env/bin/activate
   
   # On Windows:
   env\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   ```bash
   touch .env
   ```
   
   Add the following to `.env`:
   ```
   GOOGLE_GENAI_USE_VERTEXAI=FALSE
   GOOGLE_API_KEY=your_actual_api_key_here
   ```
   
   ⚠️ **Important**: Never commit `.env` to version control. Ensure it's in `.gitignore`.

### Quick Start

```python
from ResumeAgent.agent import agent

# Run the agent with your documents
result = agent.run(input="Please extract and match the provided resume with the job description")
print(result)
```

For detailed usage examples, refer to `instructions.md`.

## Configuration

### Google API Setup

1. Create a Google Cloud project
2. Enable the Generative AI API
3. Create an API key
4. Add the key to your `.env` file

### Agent Models

The project uses multiple Gemini models:
- **Root Agent**: `gemini-1.5-pro-latest` (for coordination)
- **Sub-Agents**: `gemini-2.0-flash-exp` (for specialized tasks)

You can modify model selections in `ResumeAgent/sub/agent.py` and `ResumeAgent/agent.py`.

## Usage Examples

See `instructions.md` for comprehensive usage documentation and examples.

## Development

### Adding Dependencies

```bash
pip install <package-name>
pip freeze > requirements.txt
```

### Project Architecture

- **Root Agent**: Coordinates between sub-agents and manages the overall workflow
- **Sub-Agents**: Specialize in specific extraction and matching tasks
- **Data Models**: Pydantic models ensure type safety and validation
- **Utilities**: Helper functions for document processing and extraction

## Contributing

Contributions are welcome! Please ensure code follows the project's structure and includes appropriate documentation.

## License

This project is for educational and research purposes.

## Support

For issues, questions, or suggestions, please refer to the project documentation or open an issue on GitHub.
