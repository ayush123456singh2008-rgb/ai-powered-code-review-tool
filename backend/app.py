# app.py
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from bcrypt import hashpw, gensalt, checkpw
from jose import jwt, JWTError
from datetime import datetime, timedelta
from logging.config import dictConfig
from fastapi.middleware.cors import CORSMiddleware

# Logging Configuration
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'default'
        }
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console']
    }
})

# Database Configuration
SQLALCHEMY_DATABASE_URL = "sqlite:///ai-powered-code-review-tool.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    url = Column(String)
    user_id = Column(Integer)

class CodeAnalysisResult(Base):
    __tablename__ = "code_analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    repository_id = Column(Integer)
    file_name = Column(String)
    issues = Column(String)

Base.metadata.create_all(bind=engine)

# FastAPI App
app = FastAPI()

# OAuth2 Configuration
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# CORS Configuration
origins = [
    "https://ai-powered-code-review-tool.com",
    "https://api.ai-powered-code-review-tool.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Configuration
SECRET_KEY = "secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

# Pydantic Models
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class RepositoryCreate(BaseModel):
    name: str
    url: str

class CodeAnalysisResultCreate(BaseModel):
    repository_id: int
    file_name: str
    issues: str

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Authentication
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    db = SessionLocal()
    user = db.query(User).filter(User.username == token_data.username).first()
    if user is None:
        raise credentials_exception
    return user

# Routes
@app.post("/users", response_model=UserCreate)
def create_user(user: UserCreate, db: SessionLocal = Depends(get_db)):
    hashed_password = hashpw(user.password.encode("utf-8"), gensalt())
    db_user = User(username=user.username, email=user.email, password=hashed_password.decode("utf-8"))
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")

@app.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    db = SessionLocal()
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not checkpw(form_data.password.encode("utf-8"), user.password.encode("utf-8")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = jwt.encode(
        {"sub": user.username, "exp": datetime.utcnow() + access_token_expires},
        SECRET_KEY,
        algorithm=ALGORITHM,
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/repositories", response_model=List[RepositoryCreate])
def get_repositories(current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    repositories = db.query(Repository).filter(Repository.user_id == current_user.id).all()
    return repositories

@app.post("/repositories", response_model=RepositoryCreate)
def create_repository(repository: RepositoryCreate, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    db_repository = Repository(name=repository.name, url=repository.url, user_id=current_user.id)
    db.add(db_repository)
    db.commit()
    db.refresh(db_repository)
    return db_repository

@app.get("/repositories/{repository_id}/code-analysis", response_model=CodeAnalysisResultCreate)
def get_code_analysis(repository_id: int, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    code_analysis_result = db.query(CodeAnalysisResult).filter(CodeAnalysisResult.repository_id == repository_id).first()
    if not code_analysis_result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Code analysis result not found")
    return code_analysis_result

@app.post("/repositories/{repository_id}/code-analysis")
def run_code_analysis(repository_id: int, current_user: User = Depends(get_current_user), db: SessionLocal = Depends(get_db)):
    # Run code analysis here
    return {"message": "Code analysis running"}

# Error Handling
@app.exception_handler(HTTPException)
def http_exception_handler(request, exc):
    return {"error": {"code": exc.status_code, "message": exc.detail}}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)