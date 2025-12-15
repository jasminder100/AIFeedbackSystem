# AI Feedback System
This project is a web-based feedback management system that allows users to submit ratings and reviews while enabling administrators to securely review, analyze, and act on that feedback using AI-generated insights.

The application is built with two dashboards:

A User Dashboard for submitting feedback and receiving AI-generated responses. 

An Admin Dashboard for reviewing all feedback and analytics. 

# User Dashboard

The User Dashboard is publicly accessible and designed to be simple and intuitive.

# Functionality

1) Users can select a rating from 1 to 5.

2) Users can write a short review based on their experience.

3) After submission, the system generates an AI-based response in real time.

# Process 

1) The user selects a rating and submits a review.

2) The feedback is processed using an OpenAI API.

3) An AI-generated response is shown to the user. 

4) The feedback and AI output are stored for administrative review.

# Admin Dashboard

The Admin Dashboard is restricted to authorized administrators only.

1) Access Control

2) Admin access is protected by a password

3) The password is stored securely in the .env file

4) Users cannot access admin data without authentication

# Features

View all submitted feedback in a structured, Excel-style format. 

Each record includes:

1) Timestamp

2) User rating

3) User feedback

4) AI-generated response

5) AI-generated summary

6) AI-recommended action

# Priority Feedback Monitoring

1) Reviews with a rating of 2 or lower are clearly highlighted.

2) This allows administrators to quickly identify feedback that requires attention and take corrective action.

# Data Storage

1) All data is stored in a shared CSV file. 

2) Both dashboards read from and write to the same file. 

# Stored Information

1) Timestamp

2) Rating

3) User feedback

4) AI response

5) AI summary

6) AI recommended action

This approach keeps the system lightweight and easy to maintain while meeting the project’s requirements.

# Technologies Used

The project is built using the following tools and libraries:

1) Streamlit – for building the web dashboards.

2) OpenAI API – for AI response generation and analysis.

3) Pandas – for data handling and analytics.

4) python-dotenv – for secure environment variable management.

# Large Language Models(LLMs)

The system integrates a Large Language Model (LLM) to automate key feedback-processing tasks and enhance both user experience and administrative insight. LLMs are used for the following purposes: 

1) User Response Generation: Produces clear, context-aware responses based on the user’s rating and written feedback.

2) Review Summarization: Condenses user reviews into concise summaries, enabling quicker understanding of feedback trends.

3) Recommended Action Generation: Suggests appropriate next steps based on sentiment and review content, supporting informed administrative decisions.

All AI interactions are handled through a secured API, with configuration and credentials managed via environment variables. This ensures safe usage, flexibility across deployment environments, and consistent behavior across both dashboards.

# Conclusion

This project demonstrates a practical and efficient approach to managing user feedback using AI. By combining a simple user interface with secure administrative access and automated language processing, the system enables meaningful interaction with users while providing administrators with clear, actionable insights. The dual-dashboard design ensures a clear separation between public feedback submission and internal analysis, while the use of AI helps reduce manual effort in responding to reviews and identifying areas that require attention. Overall, the solution is lightweight, scalable, and well-suited for real-world feedback management scenarios.
