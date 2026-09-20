import json
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from sqlalchemy.orm import Session

from .auth import (
    create_access_token,
    get_user_id_from_token,
    hash_password,
    verify_password,
)
from .database import Decision, Ticket, User, create_tables, get_db
from .decision import make_decision
from .retrieval import load_saved_knowledge_base, retrieve_relevant_chunks


app = FastAPI(
    title="AI Support Ticket Decision Assistant",
    version="1.0.0",
)

security = HTTPBearer()


def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    try:
        return get_user_id_from_token(credentials.credentials)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
        )


@app.on_event("startup")
def startup_event():
    create_tables()
    app.state.knowledge_base = load_saved_knowledge_base()

class RegisterRequest(BaseModel):
    email: str
    password: str


@app.get("/")
def root():
    return {
        "message": "AI Support Ticket Decision Assistant API is running"
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/register")
def register(
    request: RegisterRequest,
    db: Session = Depends(get_db),
):
    existing_user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered",
        )

    user = User(
        email=request.email,
        password_hash=hash_password(request.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "User registered successfully",
        "user_id": user.id,
        "email": user.email,
    }


class LoginRequest(BaseModel):
    email: str
    password: str


class TicketCreateRequest(BaseModel):
    message: str


@app.post("/login")
def login(
    request: LoginRequest,
    db: Session = Depends(get_db),
):
    user = (
        db.query(User)
        .filter(User.email == request.email)
        .first()
    )

    if not user or not verify_password(
        request.password,
        user.password_hash,
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )

    access_token = create_access_token(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@app.get("/me")
def get_me(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found",
        )

    return {
        "id": user.id,
        "email": user.email,
    }


@app.post("/tickets")
def create_ticket(
    request: TicketCreateRequest,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    retrieved_chunks = retrieve_relevant_chunks(
        request.message,
        app.state.knowledge_base,
    )

    decision = make_decision(
        request.message,
        retrieved_chunks,
    )

    ticket = Ticket(
        user_id=user_id,
        message=request.message,
    )

    db.add(ticket)
    db.commit()
    db.refresh(ticket)

    saved_decision = Decision(
        ticket_id=ticket.id,
        action=decision.action,
        reason=decision.reason,
        confidence=decision.confidence,
        sources=json.dumps(decision.sources),
    )

    db.add(saved_decision)
    db.commit()

    return {
        "id": ticket.id,
        "message": ticket.message,
        "user_id": ticket.user_id,
        "decision": {
            "action": decision.action,
            "confidence": decision.confidence,
            "reason": decision.reason,
            "sources": decision.sources,
        },
    }


@app.get("/tickets")
def get_tickets(
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    tickets = (
        db.query(Ticket)
        .filter(Ticket.user_id == user_id)
        .order_by(Ticket.created_at.desc())
        .all()
    )

    return [
        {
            "id": ticket.id,
            "message": ticket.message,
            "user_id": ticket.user_id,
            "created_at": ticket.created_at,
           "decision": {
                "action": ticket.decision.action,
                "confidence": ticket.decision.confidence,
                "reason": ticket.decision.reason,
                "sources": json.loads(ticket.decision.sources),
            } if ticket.decision else None,
        }
        for ticket in tickets
    ]


@app.get("/tickets/{ticket_id}")
def get_ticket(
    ticket_id: int,
    user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    ticket = (
        db.query(Ticket)
        .filter(
            Ticket.id == ticket_id,
            Ticket.user_id == user_id,
        )
        .first()
    )

    if not ticket:
        raise HTTPException(
            status_code=404,
            detail="Ticket not found",
        )

    decision = ticket.decision

    return {
        "id": ticket.id,
        "message": ticket.message,
        "user_id": ticket.user_id,
        "created_at": ticket.created_at,
        "decision": {
            "action": decision.action,
            "confidence": decision.confidence,
            "reason": decision.reason,
            "sources": json.loads(decision.sources),
        },
    }