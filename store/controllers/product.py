from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pydantic import UUID4
from store.core.exceptions import NotFoundException

from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.usecases.product import ProductUsecase

from fastapi import APIRouter, HTTPException
from store.usecases.product import create_product
from store.core.exceptions import InsertError
from fastapi import APIRouter, HTTPException
from store.usecases.product import update_product
from store.core.exceptions import NotFoundError

router = APIRouter(tags=["products"])


@router.post(path="/", status_code=status.HTTP_201_CREATED)
async def post(
    body: ProductIn = Body(...), usecase: ProductUsecase = Depends()
) -> ProductOut:
    return await usecase.create(body=body)


@router.get(path="/{id}", status_code=status.HTTP_200_OK)
async def get(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> ProductOut:
    try:
        return await usecase.get(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)


@router.get(path="/", status_code=status.HTTP_200_OK)
async def query(usecase: ProductUsecase = Depends()) -> List[ProductOut]:
    return await usecase.query()


@router.patch(path="/{id}", status_code=status.HTTP_200_OK)
async def patch(
    id: UUID4 = Path(alias="id"),
    body: ProductUpdate = Body(...),
    usecase: ProductUsecase = Depends(),
) -> ProductUpdateOut:
    return await usecase.update(id=id, body=body)


@router.delete(path="/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(
    id: UUID4 = Path(alias="id"), usecase: ProductUsecase = Depends()
) -> None:
    try:
        await usecase.delete(id=id)
    except NotFoundException as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message)
    
router = APIRouter()

@router.post("/products")
def create_product_controller(product_data: dict):
    try:
        return create_product(product_data)
    except InsertError as e:
        raise HTTPException(status_code=400, detail=e.detail)
    
router = APIRouter()

@router.patch("/products/{product_id}")
def update_product_controller(product_id: str, update_data: dict):
    try:
        return update_product(product_id, update_data)
    except NotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)

@router.get("/products/filter")
def filter_products_controller(min_price: float, max_price: float):
    try:
        return filter_products_by_price(min_price, max_price)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))