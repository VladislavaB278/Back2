from fastapi import HTTPException
from fastapi.responses import JSONResponse

from src.schemas.users import UserAdmin, UserCreate
from src.security import get_password_hash
from src.utils.unitofwork import IUnitOfWork


async def create_user(uow: IUnitOfWork, data: UserCreate | UserAdmin):
    async with uow:
        user = await uow.users.find_one(username=data.username, raw=True, no_error=True)

        if user:
            raise HTTPException(status_code=422, detail="Username is already registered with us.")

        data = data.model_dump()
        data["password"] = get_password_hash(data["password"])
        await uow.users.add_one(data)
        payload = {"message": "User account has been succesfully created."}

        return JSONResponse(content=payload)


async def update_user_query(uow: IUnitOfWork, user, data: UserAdmin | UserCreate):
    named_user = await uow.users.find_one(username=data.username, no_error=True)
    if named_user and named_user[0].username != user.username:
        raise HTTPException(status_code=422, detail="A user with the same name already exists.")
    res = await uow.users.edit_one(id=user.id, data=data.model_dump(exclude_none=True))
    return res


async def update_user(uow: IUnitOfWork, user, data: UserAdmin | UserCreate):
    data.password = get_password_hash(data.password)
    async with uow:
        await update_user_query(uow, user, data)
