from dataclasses import dataclass
from algobench.models.algorithm import Algorithm

@dataclass
class AlgorithmRepository:
    algorithms: dict[int, Algorithm]

    def get_all(self) -> list[Algorithm]:
        return list(self.algorithms.values())

    def get_by_id(self, alg_id: int) -> Algorithm | None:
        return self.algorithms.get(alg_id)

