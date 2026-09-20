# Development Notes

## Development Approach

This project was developed as a small end-to-end AI support ticket decision assistant.

The implementation focused on keeping the code simple and understandable while meeting the assignment requirements.

## Main Components

- FastAPI backend for REST API endpoints
- Streamlit frontend for the user interface
- SQLite database for persistent storage
- JWT authentication for protected API endpoints
- bcrypt password hashing
- Local knowledge base for support policies
- Embeddings and similarity search for RAG retrieval
- Google Gemini for AI decision generation
- Pydantic for structured decision validation

## AI-Assisted Development

AI coding assistance was used during development for:

- Understanding implementation requirements
- Debugging errors
- Reviewing code structure
- Improving API and frontend integration
- Troubleshooting authentication and API issues

All generated code was reviewed, tested, and adapted to the project requirements.

## Testing

The application was tested for:

- User registration
- User login
- JWT authentication
- Protected API endpoints
- Ticket creation
- Ticket history
- User-specific ticket authorization
- RAG retrieval
- Structured AI decision output

A sample evaluation script is included in `evaluate.py`.

## Security Testing

Authorization was tested by creating tickets for different users and verifying that one user's JWT could not access another user's ticket.

## Notes

The Gemini API key is stored in the local `.env` file and is not included in the repository.

The SQLite database and virtual environment are excluded from Git using `.gitignore`.