from fastapi import APIRouter

from app.schemas.code import (
    CodeRunRequest,
    CodeRunResponse,
)
from app.services.execution_service import (
    CodeExecutionService,
)

router = APIRouter(
    prefix="/code",
    tags=["Code Execution"],
)

execution_service = CodeExecutionService()


@router.post(
    "/run",
    response_model=CodeRunResponse,
)
async def run_code(
    request: CodeRunRequest,
):

    return await execution_service.run_code(
        request
    )