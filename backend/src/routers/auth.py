from fastapi import APIRouter, Depends, Header, status
from fastapi.security import OAuth2PasswordRequestForm

from src.services import auth_service
from src.utils.dependencies import UOWDep

router = APIRouter(prefix="/api/users", tags=["Users"], responses={404: {"description": "Not found"}})


@router.post("/sign_in", status_code=status.HTTP_200_OK)
async def authenticate_user(uow: UOWDep, data: OAuth2PasswordRequestForm = Depends()):
    res = await auth_service.get_token(uow, data)
    return res


@router.post("/refresh", status_code=status.HTTP_200_OK)
async def refresh_access_token(uow: UOWDep, refresh_token: str = Header()):
    res = await auth_service.get_refresh_token(uow, refresh_token)
    return res

