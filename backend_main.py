from fastapi import FastAPI
from core.database import engine
from models import models
from routers import students, sync
from services import inferences

# 1. This command tells SQLAlchemy to build any tables that don't exist yet.
# (Since you used DBeaver to build them, this just safely verifies they are there).
models.Base.metadata.create_all(bind=engine)

# 2. Initialize the API
app = FastAPI(
    title="AI-Career Bridge API",
    description="The Central Data Gateway",
    version="1.0.0"
)

# 3. Plug in the Routers
app.include_router(students.router)
app.include_router(sync.router)

# @app.get("/")
# def health_check():
#     return {"status": "online", "system": "HP Compaq Central Gateway"}

# @app.post("/ask")
# async def ask_ai(request: UserRequest):
#     response = await get_ai_response(request.prompt)
#     return {"answer": response}