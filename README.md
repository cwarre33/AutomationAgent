# AutomationAgent

AutomationAgent is a modular Python project that automates short-form content generation,
editing, and posting across multiple platforms. It is organized into several components:

- **dashboard**: Streamlit dashboard for monitoring and controlling workflows.
- **agents**: Modular automation scripts for generating, editing, and posting content.
- **workflows**: YAML files defining reusable automation workflows.
- **utils**: Shared utilities used across the project.

## Installation

```bash
# clone the repository
git clone <repo-url>
cd AutomationAgent

# install dependencies
pip install -r requirements.txt
```

## Usage

Run the Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

Create or modify workflows in the `workflows` directory and extend agents in `agents`.
