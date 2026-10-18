DataMind Manufacturing — System Architecture

1. Project Overview

DataMind Manufacturing is a conversational analytics application designed to help users ask questions about manufacturing data using natural language.

The application is intended to connect an AI model with a Snowflake database and present results through a user interface.

2. Main Components

User Interface — Streamlit

- Accepts questions from users.
- Displays answers and query results.
- Shows understandable error messages when something goes wrong.

AI Layer — Google Gemma

- Interprets questions about manufacturing operations.
- Helps generate SQL queries for supported questions.
- Uses database results to help formulate answers.
- Should request clarification when a question is ambiguous.

Database Layer — Snowflake

- Stores or provides access to manufacturing data.
- Executes SQL queries generated for supported requests.
- Returns records for the application to process.

Testing and Integration

- Verifies that components communicate correctly.
- Checks answers against actual database results.
- Records failures, limitations, and test outcomes.

3. Expected Request Flow

1. The user enters a manufacturing question in Streamlit.
2. The AI layer interprets the question and prepares a SQL query.
3. The application validates the query before execution.
4. Snowflake executes the query and returns results.
5. The application uses the returned results to prepare an answer.
6. Streamlit displays the answer and supporting information to the user.

4. Reliability and Safety Checks

- Validate generated SQL before executing it.
- Use read-only database permissions for analytics where possible.
- Never expose database credentials in source code.
- Handle database errors and empty results clearly.
- Do not present unverified or invented values as facts.
- Ask for clarification when required information is missing.
- Restrict requests to the application's supported manufacturing-data scope.

5. Component Status

This document describes the intended architecture. Update it after confirming the actual implementation with the team.

Component| Technology| Status
User interface| Streamlit| To be verified
AI model| Google Gemma| To be verified
Database| Snowflake| To be verified
Testing and integration| Test cases and checklists| In progress

6. Open Questions

- Which Snowflake tables and columns are used?
- How is the Gemma model hosted and accessed?
- Where are database credentials configured?
- How is generated SQL validated?
- Which files start the application?

Update this document when these details have been confirmed.
