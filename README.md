# AutomationAgent

AutomationAgent is a lightweight framework for automating short-form content generation, editing and posting. It provides a simple Streamlit dashboard to trigger automation workflows and monitor results. Agents encapsulate individual tasks (such as generating or posting content) while workflows define how those agents run together.

## Project structure

- **dashboard/** – Streamlit user interface for launching workflows.
- **agents/** – Python modules containing reusable automation agents.
- **workflows/** – YAML files describing sequences of agent steps.
- **utils/** – Helper utilities shared across the project.
- **requirements.txt** – Python dependencies.

## Running the dashboard

1. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the Streamlit app:
   ```bash
   streamlit run dashboard/app.py
   ```
   The dashboard will open in your browser where you can select and run workflows.

## Adding workflows or agents

- **Create a new agent** by adding a Python file in `agents/`. Each agent exposes functions that perform an action, e.g. `generate_content` or `post_content`.
- **Define a workflow** by creating a YAML file in `workflows/`. A workflow lists steps by name and optional parameters that map to your agent functions. See `sample_workflow.yaml` for a minimal example.
- After adding new agents or workflows, restart the dashboard to pick up the changes.

AutomationAgent is intentionally simple and can be extended with additional utilities and agents to fit different content automation needs.
