
## Create Virtual Environment

1. Open terminal and navigate to your project directory
2. Create virtual environment:
```bash
python -m venv env
```
3. Activate virtual environment:
- On Windows:
```bash
env\Scripts\activate
```
- On macOS/Linux:
```bash
source env/bin/activate
```

## Install Google Agent Development Kit

1. Install the Google Agent Development Kit:
```bash
pip install google-agent-development-kit
```

2. Verify installation:
```bash
python -c "import google_agent_development_kit"
```

3. Update pip if needed:
```bash
pip install --upgrade pip
```

## Additional Dependencies

Install any additional required packages:
```bash
pip install -r requirements.txt
```

## Configuration

1. Set up your Google Cloud credentials
2. Initialize the development kit
3. Configure your agent settings

*Note: Keep virtual environment active while working on the project*

## Environment Variables

1. Create a .env file in your project root:
```bash
touch .env
```

2. Add the following configuration to your .env file:
```
GOOGLE_GENAI_USE_VERTEXAI=FALSE
GOOGLE_API_KEY=PASTE_YOUR_ACTUAL_API_KEY_HERE
```

3. Ensure .env is in your .gitignore file to keep credentials secure

## Export Dependencies

To create or update requirements.txt:
```bash
pip freeze > requirements.txt
```

This command exports all installed packages and their versions to requirements.txt.