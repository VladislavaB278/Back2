from fastapi import APIRouter, Depends, status

from src.models.users import Users
from src.schemas.users import UserCreate, UserRead
from src.security import get_current_user
from src.services import user_service
from src.utils.dependencies import UOWDep

router = APIRouter(prefix="/api/users", tags=["Users"], responses={404: {"description": "Not found"}})


@router.post("/sign_up", status_code=status.HTTP_201_CREATED)
async def create_user_router(uow: UOWDep, data: UserCreate):
    res = await user_service.create_user(uow, data)
    return res


@router.get("/me", status_code=status.HTTP_200_OK, response_model=UserRead)
def get_user_detail_router(user: Users = Depends(get_current_user)):
    return user


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
async def edit_user_router(uow: UOWDep, data: UserCreate, user: Users = Depends(get_current_user)):
    await user_service.update_user(uow, user, data)
