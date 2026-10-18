DataMind Manufacturing — Hackathon Demo Script

1. Introduction (30 seconds)

"Hello everyone. We are presenting DataMind Manufacturing, a conversational analytics application designed to help users explore manufacturing data using natural-language questions.

Our goal is to make manufacturing insights easier to access without requiring every user to write SQL manually."

2. Explain the Architecture (30 seconds)

"Our application is designed around three main components:

- Streamlit provides the user interface.
- Google Gemma interprets questions and helps generate database queries.
- Snowflake provides the manufacturing data.

The integration workflow connects the user's question to the database and presents the resulting insights."

Confirm these components are implemented and working before presenting them as completed features.

3. Demonstrate a Manufacturing Question (60 seconds)

Open the running application and enter a supported question, such as:

"What is the total production?"

Explain the workflow:

1. The application receives the question.
2. The AI layer interprets the request.
3. The application queries Snowflake.
4. The result is displayed to the user.

Use the actual result returned by the application. Do not invent a production figure for the demonstration.

4. Demonstrate Another Query (45 seconds)

If the relevant data is available, ask:

"Which machine has the highest downtime?"

Show the returned answer and, if supported by the application, the SQL query or records used to produce it.

Verify the result against Snowflake before the demo.

5. Explain Testing and Reliability (30 seconds)

"Our integration work includes test cases for manufacturing questions, ambiguous requests, unsupported questions, and missing data.

We compare application responses with actual database results so that we can identify incorrect queries and unsupported answers."

Only report completed tests and verified results.

6. Conclusion (15 seconds)

"DataMind Manufacturing aims to make manufacturing analytics more accessible through natural-language interaction.

Thank you. We are happy to answer your questions."

Demo Preparation Checklist

- [ ] Confirm the application starts successfully.
- [ ] Confirm the Gemma integration works.
- [ ] Confirm the Snowflake connection works.
- [ ] Prepare two verified questions and their actual results.
- [ ] Confirm the displayed answers match database records.
- [ ] Keep a screenshot or backup of verified results in case the live demo fails.
- [ ] Ensure no credentials or secrets appear on screen.
- [ ] Rehearse the presentation and keep it within the allotted time.

Known Limitations

Record any incomplete features, unavailable data, or known issues here before the presentation.
