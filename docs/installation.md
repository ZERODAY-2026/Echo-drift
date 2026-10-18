DataMind Manufacturing — Installation Guide

1. Overview

This guide describes the intended setup process for the DataMind Manufacturing application.

Important: Confirm the actual dependencies, startup command, model configuration, and Snowflake settings with the development team before running the application.

2. Prerequisites

Check that you have access to:

- Python, using the version specified by the project.
- The Echo-drift project repository.
- The required Python packages.
- The configured Gemma model or its approved access method.
- A Snowflake account and the necessary database permissions, if required.

3. Get the Project

Clone the team repository using Git:

git clone https://github.com/ZERODAY-2026/Echo-drift.git
cd Echo-drift

Alternatively, download the repository as a ZIP file from GitHub.

4. Set Up the Python Environment

Create a virtual environment:

python -m venv .venv

Activate it on Windows:

.venv\Scripts\activate

Activate it on macOS or Linux:

source .venv/bin/activate

5. Install Dependencies

If the repository contains a "requirements.txt" file, run:

pip install -r requirements.txt

If the project uses another dependency manager, follow the instructions in the repository README instead.

6. Configure Credentials

Follow the team's approved configuration process for Snowflake and the Gemma model.

- Keep credentials out of source code.
- Do not commit ".env" files or secret keys.
- Use environment variables or the team's approved secrets-management method.
- Request access from the project team if credentials are unavailable.

Do not invent configuration variable names. Confirm the required names and values with the developers.

7. Run the Application

Check the README and project files for the correct entry-point filename.

If the team confirms that the entry point is "app.py", the application may be started with:

streamlit run app.py

Otherwise, use the startup command documented by the team.

8. Verify the Setup

- [ ] Dependencies install successfully.
- [ ] Required configuration is available.
- [ ] The application starts without errors.
- [ ] The interface loads successfully.
- [ ] A supported test question returns a result.
- [ ] Database or model errors are displayed clearly.

9. Troubleshooting

Dependency installation fails: Check the Python version and dependency instructions.

Snowflake connection fails: Verify the account configuration, credentials, network access, and permissions with the team.

Gemma is unavailable: Confirm the configured model location and required access.

Streamlit does not start: Confirm that Streamlit is installed and that the correct entry-point filename is being used.

10. Maintenance

Update this guide whenever the team confirms changes to dependencies, configuration, or startup instructions.
