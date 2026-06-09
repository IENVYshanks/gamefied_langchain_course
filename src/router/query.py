from fastapi import APIRouter, Depends
from src.helper.llm_call import user_query, agent_call
from src.models.chat import UserQuery

router = APIRouter(
    prefix="/query",
    tags=["query"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.post("/")
async def get_query(query : UserQuery):
    return user_query(query.query)

@router.post("/agent")
async def get_agent_query(query: UserQuery):
    response = agent_call(query.query)
    return response