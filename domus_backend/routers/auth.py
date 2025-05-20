from fastapi import APIRouter

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/token')
def login_for_access_token():
    return {'access': 'fake_token', 'token_type': 'bearer'}
