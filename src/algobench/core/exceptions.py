class AlgoBenchError(Exception):
    pass

class AlgorithmNotFoundError(AlgoBenchError):
    """Se lanza cuando no se encuentra un algoritmo por su ID."""

    def __init__(self, algorithm_id: int | str, message: str | None = None):
        self.algorithm_id = algorithm_id
        self.message = message or f"No se encontró el algoritmo con ID '{algorithm_id}'."
        super().__init__(self.message)
