from typing import List
from uuid import UUID
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
import pymongo
from store.db.mongo import db_client
from store.models.product import ProductModel
from store.schemas.product import ProductIn, ProductOut, ProductUpdate, ProductUpdateOut
from store.core.exceptions import NotFoundException
from store.core.exceptions import InsertError
from datetime import datetime
from store.core.exceptions import NotFoundError

class ProductUsecase:
    def __init__(self) -> None:
        self.client: AsyncIOMotorClient = db_client.get()
        self.database: AsyncIOMotorDatabase = self.client.get_database()
        self.collection = self.database.get_collection("products")

    async def create(self, body: ProductIn) -> ProductOut:
        product_model = ProductModel(**body.model_dump())
        await self.collection.insert_one(product_model.model_dump())

        return ProductOut(**product_model.model_dump())

    async def get(self, id: UUID) -> ProductOut:
        result = await self.collection.find_one({"id": id})

        if not result:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        return ProductOut(**result)

    async def query(self) -> List[ProductOut]:
        return [ProductOut(**item) async for item in self.collection.find()]

    async def update(self, id: UUID, body: ProductUpdate) -> ProductUpdateOut:
        result = await self.collection.find_one_and_update(
            filter={"id": id},
            update={"$set": body.model_dump(exclude_none=True)},
            return_document=pymongo.ReturnDocument.AFTER,
        )

        return ProductUpdateOut(**result)

    async def delete(self, id: UUID) -> bool:
        product = await self.collection.find_one({"id": id})
        if not product:
            raise NotFoundException(message=f"Product not found with filter: {id}")

        result = await self.collection.delete_one({"id": id})

        return True if result.deleted_count > 0 else False


product_usecase = ProductUsecase()

def create_product(product_data):
    try:
        if not product_data:  
            raise Exception("Dados inválidos para inserção")
        return {"id": "12345", "message": "Produto criado com sucesso"}
    except Exception as e:
        raise InsertError(detail=f"Erro ao inserir produto: {str(e)}")
    
def update_product(product_id: str, update_data: dict):
    try:
        # Simule a busca pelo produto
        product = {"id": product_id, "name": "Produto Teste"}  # Simulação
        if not product:
            raise NotFoundError(detail="Produto não encontrado")

        # Atualize os dados
        update_data["updated_at"] = datetime.utcnow()  # Atualiza o campo
        # Simule a lógica de atualização no banco, ex.: db.collection.update_one(...)
        return {"id": product_id, "updated_data": update_data}
    except Exception as e:
        raise e
    
    def filter_products_by_price(min_price: float, max_price: float):
    try:
        # Simule uma busca no banco
        products = [
            {"id": "1", "name": "Produto 1", "price": 6000},
            {"id": "2", "name": "Produto 2", "price": 7500},
            {"id": "3", "name": "Produto 3", "price": 8500},
        ]
        # Filtre os produtos pelo intervalo de preço
        filtered_products = [
            p for p in products if min_price < p["price"] < max_price
        ]
        return filtered_products
    except Exception as e:
        raise Exception(f"Erro ao filtrar produtos: {str(e)}")