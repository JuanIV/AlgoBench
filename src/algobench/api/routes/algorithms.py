from fastapi import APIRouter, Depends
from algobench.schemas.algorithm import AlgorithmResponse
from algobench.services.algorithm_service import AlgorithmService
import algobench.api.dependencies

router = APIRouter()

def get_algorithm_service():
    return algobench.api.dependencies.get_algorithm_service()

@router.get("/algorithms", response_model=list[AlgorithmResponse])
def get_all_algorithms(service = Depends(get_algorithm_service)):
    return service.get_all_algorithms()

@router.get("/algorithms/{alg_id}", response_model=AlgorithmResponse)
def get_algorithm_by_id(alg_id: int, service = Depends(get_algorithm_service)):
    return service.get_algorithm_by_id(alg_id)
