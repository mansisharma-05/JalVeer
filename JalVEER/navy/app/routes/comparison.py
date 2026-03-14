from fastapi import APIRouter
from schemas.comparison_schema import ComparisonRequest
from services.ml_service import compare_by_id

router = APIRouter(prefix="/compare", tags=["Comparison"])

@router.post("/by-id")
def compare_weapons(request: ComparisonRequest):

    result = compare_by_id(request.weapon1_id, request.weapon2_id)

    return result

