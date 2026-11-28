from dataclasses import dataclass
from algobench.models.algorithm import Algorithm
from algobench.repositories.algorithm_repository import AlgorithmRepository
from algobench.core.exceptions import AlgorithmNotFoundError

@dataclass
class AlgorithmService:
    repo: AlgorithmRepository

    def get_all_algorithms(self) -> list[Algorithm]:
        return self.repo.get_all()

    def get_algorithm_by_id(self, alg_id: int) -> Algorithm:
        found = self.repo.get_by_id(alg_id)
        if(found is None):
            raise AlgorithmNotFoundError(alg_id)
        return found
