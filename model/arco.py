from dataclasses import dataclass

from model.actor import Actor


@dataclass
class Arco:
    actor1: Actor
    actor2: Actor
    peso: int