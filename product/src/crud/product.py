import sqlalchemy

from src.data.models import Product
from src.data.schemas.product import (
    ProductInCreate,
    ProductInUpdate,
    ProductInResponse,
    ProductToSubstract,
)
from src.crud.base import BaseCRUD

from src.utilities.exceptions.database import (
    EntityDoesNotExist,
)

from typing import Optional, Sequence


class ProductCRUD(BaseCRUD):
    async def get_multiple(
        self,
        categories: str | None,
        order_by: str | None,
        order_type: str,
        min_cost: float | None,
        max_cost: float | None,
    ) -> Optional[Sequence[Product]]:
        stmt = sqlalchemy.select(Product)
        if categories:
            categories_list = [int(cat) for cat in categories.split(",")]
            stmt = stmt.filter(Product.category_id.in_(categories_list))
        if min_cost:
            stmt = stmt.filter(Product.price >= min_cost)
        if max_cost:
            stmt = stmt.filter(Product.price <= max_cost)
        if order_by:
            stmt = stmt.order_by(
                getattr(getattr(Product, order_by), order_type)()
            )

        query = await self.async_session.execute(statement=stmt)
        return query.scalars().all()

    async def create_product(
        self, product_create: ProductInCreate
    ) -> ProductInResponse:
        new_product = Product(**product_create.model_dump(exclude_none=True))
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
        new_product_data = product_update.model_dump(exclude_none=True)

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

    async def subtract_from_inventory(
        self, products_substract: Sequence[ProductToSubstract]
    ) -> Sequence[Product]:
        product_response = []
        for product in products_substract:
            select_stmt = sqlalchemy.select(Product).where(
                Product.id == product.id
            )
            query = await self.async_session.execute(statement=select_stmt)
            update_product = query.scalar()

            if not update_product:
                raise EntityDoesNotExist(f"Product with id `{id}` does not exist!")  # type: ignore

            try:
                update_product.stock -= product.quantity
                self.async_session.add(instance=update_product)
                await self.async_session.flush()
                product_response.append(update_product)
            except ValueError:
                raise ValueError("Cannot subtract more than available stock!")
        await self.async_session.commit()
        return product_response  # type: ignore
