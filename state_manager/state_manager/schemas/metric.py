from schemas.retrieve import RetrieveRQ, RetrieveRS


class RetrieveMetricRQ(RetrieveRQ):
    name: str


class RetrieveMetricRS(RetrieveRS):
    name: str
    query: str
