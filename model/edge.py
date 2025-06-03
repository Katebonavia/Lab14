from dataclasses import dataclass

from model.order import Order


@dataclass

class Edge:
    v1: Order
    v2: Order
    peso: int
