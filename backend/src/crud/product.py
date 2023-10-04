import sqlalchemy

from src.data.models import Product
from src.data.schemas.product import (
    ProductInCreate,
    ProductInUpdate,
    ProductInResponse,
)
from src.crud.base import BaseCRUD
from src.securities.hashing.password import password_generator

from src.securities.verification.credentials import credential_verifier

from src.utilities.exceptions.database import (
    EntityAlreadyExists,
    EntityDoesNotExist,
)

from src.utilities.exceptions.password import PasswordDoesNotMatch


class ProductCRUD(BaseCRUD):
    async def create_product(
        self, product_create: ProductInCreate
    ) -> ProductInResponse:
        new_product = Product(**product_create.dict(exclude_none=True))
        self.async_session.add(instance=new_product)
        await self.async_session.commit()
        await self.async_session.refresh(instance=new_product)
        return new_product

    async def read_product_by_productname(self, productname: str) -> Product:
        stmt = sqlalchemy.select(Product).where(Product.name == productname)
        query = await self.async_session.execute(statement=stmt)

        if not query:
            raise EntityDoesNotExist(
                "Product with productname `{productname}` does not exist!"
            )

        return query.scalar()  # type: ignore

    async def update_product(
        self, id: int, product_update: ProductInUpdate
    ) -> Product:
        new_product_data = product_update.dict(exclude_none=True)

        select_stmt = sqlalchemy.select(Product).where(Product.id == id)
        query = await self.async_session.execute(statement=select_stmt)
        update_product = query.scalar()

        if not update_product:
            raise EntityDoesNotExist(f"Product with id `{id}` does not exist!")  # type: ignore

        update_stmt = sqlalchemy.update(table=Product).where(Product.id == update_product.id)  # type: ignore

        for key in new_product_data:
            update_stmt = update_stmt.values({key: new_product_data[key]})

        await self.async_session.execute(statement=update_stmt)
        await self.async_session.commit()
        await self.async_session.refresh(instance=update_product)

        return update_product  # type: ignore
