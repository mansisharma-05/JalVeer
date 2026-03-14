from pydantic import BaseModel

class ComparisonRequest(BaseModel):
    weapon1_id: str
    weapon2_id: str


