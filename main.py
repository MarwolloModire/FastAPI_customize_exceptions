from fastapi import FastAPI, HTTPException, Request
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from typing import Optional
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

app = FastAPI()


users_data: dict = {}


class UserModel(BaseModel):
    username: str
    age: int = Field(gt=18)
    email: EmailStr
    password: str = Field(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'


class ErrorResponseModel(BaseModel):
    status_code: int
    detail: str
    error_code: int


class UserNotFoundException(HTTPException):
    def __init__(self, status_code=404, detail="User not found"):
        super().__init__(status_code=status_code, detail=detail)


class InvalidUserDataException(HTTPException):
    def __init__(self, detail="Incorrect data", status_code=400):
        super().__init__(status_code=status_code, detail=detail)


@app.exception_handler(UserNotFoundException)
async def user_not_found_handler(request: Request, exc: UserNotFoundException):
    start = datetime.now()
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    response.headers['X-ErrorHandleTime'] = str(datetime.now() - start)
    return response


@app.exception_handler(InvalidUserDataException)
async def invalid_user_data_handler(request: Request, exc: InvalidUserDataException):
    start = datetime.now()
    response = JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )
    response.headers['X-ErrorHandleTime'] = str(datetime.now() - start)
    return response


# Регистрация пользователя
@app.post('/users/')
async def post_user(user: UserModel):
    if user.username == 'Jiuda':
        raise InvalidUserDataException(
            detail='No, no, nooo, god, please noo!!!', status_code=406)

    users_data[user.username] = [
        user.age, user.email, user.password, user.phone]
    return {'message': 'User created successfully!', 'status_code': '200_OK'}


# Получение данных о Юзере по его имени
@app.get('/user_data/{username}')
async def read_data(username: str):
    if username == 'Ivan':
        raise HTTPException(
            status_code=406, detail='Vaniya idi domoy! Ti ustal!')
    if username not in users_data:
        raise UserNotFoundException()
    return users_data[username]


# # Обработка ошибки при выводе данных о пользователе
# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request, exc):
#     print(f'OMG! An HTTP error!: {repr(exc)}')
#     return await http_exception_handler(request, exc)


# # Обработка ошибки при попытке зарегистрировать пользователя
# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     print(f'OMG! The client sent invalid data!: {exc}')
#     return await request_validation_exception_handler(request, exc)
