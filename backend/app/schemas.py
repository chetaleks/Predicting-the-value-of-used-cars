from typing import Optional, Union, List
from pydantic import BaseModel, Field
from fastapi import Query


class CarFeatures(BaseModel):
    production_year: Optional[Union[int, float]] = Field(None)
    mileage: Optional[Union[int, float]] = Field(None)
    condition: Optional[str] = Field(None)
    owners_number: Optional[Union[int, float]] = Field(None)
    pts_original: Optional[Union[bool, str]] = Field(None)
    accidents_resolution: Optional[str] = Field(None)
    region: Optional[str] = Field(None)
    seller_type: Optional[str] = Field(None)
    brand: Optional[str] = Field(None)
    model: Optional[str] = Field(None)
    body_type: Optional[str] = Field(None)
    doors_count: Optional[Union[int, float]] = Field(None)
    seats: Optional[Union[int, str, float]] = Field(None)
    engine_displacement: Optional[Union[float, int]] = Field(None)
    engine_power: Optional[Union[float, int]] = Field(None)
    fuel_rate: Optional[Union[float, int]] = Field(None)
    steering_wheel: Optional[str] = Field(None)
    price: Optional[Union[int, float]] = Field(None)
    price_segment: Optional[str] = Field(None)
    auto_class: Optional[str] = Field(None)
    horse_power: Optional[Union[float, int]] = Field(None)
    tags: Optional[str] = Field(None)
    equipment: Optional[str] = Field(None)
    complectation_available_options: Optional[str] = Field(None)


class ModelInfo(BaseModel):
    id: str
    name: str
    params: dict
    metrics: Optional[dict] = None


class HyperParams(BaseModel):
    alpha: float = Field(1, description="Коэффициент регуляризации")
    max_iter: int = Field(100, description="Максимальное количество итераций")
    solver: str = Field("auto", description="алгоритмы оптимизации")


class FitRequestJson(BaseModel):
    data: List[CarFeatures]
    params: HyperParams
    xml_params: Optional[str] = Field(default=None, example="")


class FitRequestQueryParams(BaseModel):
    alpha: Optional[float] = Query(None)
    max_iter: Optional[int] = Query(None)
    solver: Optional[str] = Query(None)
