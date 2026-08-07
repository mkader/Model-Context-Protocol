# python -m pip install groundx or pip install groundx
from pprint import pprint
from groundx import GroundX

groundx = GroundX(
  api_key="asdadsdasdasd",
)

response = groundx.buckets.create(
    name="deepstack",
)
pprint(response)
