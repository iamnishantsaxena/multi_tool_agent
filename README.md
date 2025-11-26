# Multi Agent Project

Modular Python project for building and running AI-powered agents tailored towards doing specific tasks powered by Google Agent Development Kit.

## Features

- Modular multi AI agent architecture
- Google Agent Development Kit integration
- Document parsing (PDF, DOCX, etc.)
- Customizable prompts and utilities
- Environment variable configuration

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd multi_tool_agent
```

### 2. Create and Activate a Virtual Environment
python -m venv env
# On Windows:
env\Scripts\activate
# On macOS/Linux:
source env/bin/activate

### 3. Install Dependencies
pip install -r [requirements.txt](http://_vscodecontentref_/2)

### 4. Configure Environment Variables
Create a .env file in the project root:

Ensure .env is listed in .gitignore to keep credentials secure.

### 5. Run the Agent
Refer to instructions.md for detailed usage and configuration steps.

Exporting Dependencies
To update requirements.txt after installing new packages:

pip freeze > [requirements.txt](http://_vscodecontentref_/3)

License
This project is for educational and research purposes.
