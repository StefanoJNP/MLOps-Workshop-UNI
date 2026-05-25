from pydantic import BaseModel, Field


class PredictionInput(BaseModel):
    cement: float = Field(..., description="Cantidad de cemento en kg/m³")
    blast_furnace_slag: float = Field(
        ..., description="Cantidad de escoria de horno eléctrico en kg/m³"
    )
    fly_ash: float = Field(..., description="Cantidad de ceniza volante en kg/m³")
    water: float = Field(..., description="Cantidad de agua en kg/m³")
    superplasticizer: float = Field(
        ..., description="Cantidad de plastificante super en kg/m³"
    )
    coarse_aggregate: float = Field(
        ..., description="Cantidad de agregado grueso en kg/m³"
    )
    fine_aggregate: float = Field(..., description="Cantidad de agregado fino en kg/m³")
    age: float = Field(..., description="Edad del concreto en días")
