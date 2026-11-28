from dataclasses import dataclass

@dataclass
class Algorithm:
    alg_id: int
    name: str
    desc: str
    time_cplx: str
    space_cplx: str

