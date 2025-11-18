from pydantic import BaseModel

class InterfaceState(BaseModel):
    radius: float
    internal_hspace: float
    internal_vspace: float
    external_hspace: float
    external_vspace: float
    margin: float
    paper_type: str
    text: str
