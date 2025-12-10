from pydantic import BaseModel
import json

class PaperDimension(BaseModel):
    height: float
    width: float
    name: str

paperDimensions=[]
with open("paperDimensions.json") as fp:
    payload = json.load(fp)
    paperDimensions = [
        PaperDimension.model_validate(item)
        for item in payload
    ]

def getPaperDimensionOptions():
    return paperDimensions


