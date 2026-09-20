# AI Support Ticket Decision Assistant

An AI-powered support ticket decision assistant built using Python, FastAPI, Streamlit, SQLite, JWT authentication, RAG, and Google Gemini.

## Features

- User registration and login
- JWT authentication
- Secure password hashing
- Submit support tickets
- AI-generated decisions
- RAG-based policy retrieval
- Gemini LLM integration
- Confidence score and reasoning
- Policy source display
- Ticket history
- User-specific ticket access
- SQLite database
- Evaluation using sample test cases

## Tech Stack

- Python
- FastAPI
- Streamlit
- SQLite
- SQLAlchemy
- JWT
- Google Gemini API
- NumPy
- Pydantic


## Project Structure

```text
ai_support_decision_assistant/
├── data/
│   ├── tickets.csv
│   └── knowledge_base_embeddings.json
├── knowledge_base/
│   ├── cancellations.md
│   ├── damaged_goods.md
│   ├── defective_products.md
│   ├── returns.md
│   ├── shipping.md
│   └── wrong_item.md
├── src/
│   ├── api.py
│   ├── auth.py
│   ├── database.py
│   ├── decision.py
│   ├── ingest.py
│   └── retrieval.py
├── tests/
├── evaluate.py
├── streamlit_app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── DEVELOPMENT.md
└── README.md

## Setup

### 1. Create virtual environment

```cmd
python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

JWT_SECRET=your_secret
GEMINI_API_KEY=your_gemini_api_key

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/register` | Register a new user |
| POST | `/login` | Login and receive JWT |
| GET | `/me` | Get current user |
| POST | `/tickets` | Create and analyze a support ticket |
| GET | `/tickets` | Get the current user's tickets |
| GET | `/tickets/{id}` | Get a specific ticket |

Protected endpoints use JWT authentication with:

`Authorization: Bearer <JWT>`


## AI Decision Flow

1. The user submits a support ticket through Streamlit.
2. FastAPI receives the ticket.
3. The ticket is converted into an embedding.
4. Relevant policy chunks are retrieved from the knowledge base.
5. The ticket and retrieved policy context are sent to Gemini.
6. Gemini returns a structured decision.
7. The decision is validated using Pydantic.
8. The ticket and decision are stored in SQLite.
9. Streamlit displays the action, confidence, reasoning, and policy sources.

## Evaluation

The project includes sample support-ticket test cases.

Run the evaluation script with:

```cmd
python evaluate.py

## Security

- Passwords are stored using bcrypt hashing.
- JWT tokens are used for authentication.
- Protected endpoints validate the JWT token.
- Users can access only their own tickets.
- The Gemini API key is stored in `.env` and is excluded from GitHub.

## Running the Application

### Backend

```cmd
uvicorn src.api:app --reload


### Frontend

```cmd
streamlit run streamlit_app.py


## RAG Knowledge Base

The assistant uses policy documents stored in the `knowledge_base` folder.

The documents are split into smaller chunks and converted into embeddings.

The relevant policy chunks are retrieved using similarity search before sending the context to the Gemini model.

The generated decision is based on the support ticket and the retrieved policy information.

## Database

The application uses SQLite to store:

- User accounts
- Support tickets
- AI decisions
- Decision confidence
- Decision reasoning
- Policy sources


## Future Improvements

- Improve the accuracy of AI decisions with more test cases.
- Add more support policy documents to the knowledge base.
- Add automated API and authentication tests.

## Conclusion

This project demonstrates an end-to-end AI-powered support ticket decision system using FastAPI, Streamlit, SQLite, JWT authentication, RAG, and Google Gemini.