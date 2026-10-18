DataMind Manufacturing

Conversational AI for Manufacturing Analytics

Overview

DataMind Manufacturing is a project that aims to let users ask natural-language questions about manufacturing operations and receive answers based on database results.

The intended system combines an AI model, a Snowflake database, and a Streamlit interface.

Project Goals

- Make manufacturing data easier to explore.
- Translate supported natural-language questions into database queries.
- Present useful insights from query results.
- Handle ambiguous questions and missing data clearly.
- Test the accuracy and reliability of generated answers.

Intended Architecture

- User interface: Streamlit
- AI model: Google Gemma
- Database: Snowflake
- Testing and integration: Test cases, verification, and integration checks

Confirm these technologies against the actual implementation before treating them as completed features.

Example Questions

The application is intended to support questions such as:

- What is the total production?
- Which machine has the highest downtime?
- Which raw material has the lowest stock?
- Which product has the highest defect rate?
- Which customer orders are delayed?

The actual answers depend on the data available in the configured database.

Repository Structure

Echo-drift/
├── README.md
├── tests/
│   ├── test_cases.md
│   ├── ground_truth.md
│   └── integration_checklist.md
├── docs/
│   ├── architecture.md
│   ├── installation.md
│   └── test_results.md
└── demo/
    └── demo_script.md

This is the intended documentation structure. Update it if the actual repository differs.

Setup

Refer to "the installation guide" (docs/installation.md) for setup instructions.

Check the actual project files and required configuration before running the application.

Testing

- "Test cases" (tests/test_cases.md)
- "Ground truth template" (tests/ground_truth.md)
- "Integration checklist" (tests/integration_checklist.md)
- "Test results" (docs/test_results.md)

Run tests against the actual application and database. Record verified results; do not mark unexecuted tests as passed.

Demo

Refer to "the demo script" (demo/demo_script.md) for the proposed presentation flow.

Security

- Never commit passwords, API keys, or database credentials.
- Use the team's approved secrets-management method.
- Validate SQL queries before executing them.
- Use appropriate database permissions.

Team Contributions

Update this section with the actual team members and their responsibilities.

Project Status

Status: In development. Update this section as components are implemented and tested.
