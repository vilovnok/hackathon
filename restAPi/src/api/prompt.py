from fastapi import APIRouter
from services.prompt import PromptService
from schemas.prompt import Prompt_to

router = APIRouter(
    prefix='/generate',
    tags=['Generate']
)

@router.post('/prompt-prepoccesing', status_code=201)
async def prepoccesing(
    data: Prompt_to,
):
    res = await PromptService().preproccesing(data)
    return res

