from fastapi import APIRouter


router = APIRouter(prefix='/api/v1/despesa', tags=['despesa'])

@router.get('/')
def home():
    return {'message': 'Olá Mundo!'}