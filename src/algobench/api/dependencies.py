from algobench.repositories.algorithm_repository import AlgorithmRepository
from algobench.services.algorithm_service import AlgorithmService
from algobench.models.algorithm import Algorithm

def get_algorithm_repository() -> AlgorithmRepository:
    hardcoded_algorithms = {
        1: Algorithm(
            alg_id=1,
            name="QuickSort",
            desc="Algoritmo de ordenamiento divide y vencerás",
            time_cplx="O(n log n)",
            space_cplx="O(log n)"
        ),
        2: Algorithm(
            alg_id=2,
            name="BubbleSort",
            desc="Algoritmo de ordenamiento por intercambio simple",
            time_cplx="O(n^2)",
            space_cplx="O(1)"
        ),
        3: Algorithm(
            alg_id=3,
            name="Binary Search",
            desc="Búsqueda eficiente en listas ordenadas",
            time_cplx="O(log n)",
            space_cplx="O(1)"
        )
    }
    
    return AlgorithmRepository(algorithms=hardcoded_algorithms)

def get_algorithm_service() -> AlgorithmService:
    return AlgorithmService(get_algorithm_repository())