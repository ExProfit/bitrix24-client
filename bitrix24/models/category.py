from typing import List
from .base import BaseBitrixModel
from pydantic import Field


class Category(BaseBitrixModel):
    id: int
    name: str
    sort: int
    entity_type_id: int = Field(alias="entityTypeId")
    is_default: str = Field(alias="isDefault")

class CategoryResponse(BaseBitrixModel):
    result: Category

class CategoriesListResult(BaseBitrixModel):
    categories: List[Category]

class CategoriesListResponse(BaseBitrixModel):
    result: CategoriesListResult
    total: int