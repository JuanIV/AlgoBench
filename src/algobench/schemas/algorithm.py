from pydantic import BaseModel, ConfigDict

class AlgorithmResponse(BaseModel):
    alg_id: int
    name: str
    desc: str
    time_cplx: str
    space_cplx: str

    model_config = ConfigDict(from_attributes=True)
