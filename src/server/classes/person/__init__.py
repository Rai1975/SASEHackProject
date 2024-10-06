from typing import List
import numpy as np

class Person:
    def __init__(
        self,
        name: str,
        id: int,
        tags: List[str],
        age: int,
        O_embed: List[float],
        C_embed: List[float],
        E_embed: List[float],
        A_embed: List[float],
        N_embed: List[float],
        disconnects: List[int] = None,
        connects: List[int] = None
    ):
        """
        Initialize a new Person instance.

        :param name: The person's name.
        :param id: A unique identifier for the person.
        :param tags: A list of string tags associated with the person.
        :param age: The person's age.
        :param O_embed: Openness embedding vector.
        :param C_embed: Conscientiousness embedding vector.
        :param E_embed: Extraversion embedding vector.
        :param A_embed: Agreeableness embedding vector.
        :param N_embed: Neuroticism embedding vector.
        :param disconnects: A list of integers representing disconnect events.
        """
        self.name = name
        self.id = id
        self.tags = tags
        self.age = age
        self.O_embed = O_embed
        self.C_embed = C_embed
        self.E_embed = E_embed
        self.A_embed = A_embed
        self.N_embed = N_embed
        self.disconnects = disconnects if disconnects is not None else []
        self.connects = connects if connects is not None else []

    def add_tag(self, tag: str):
        """Add a new tag to the person."""
        self.tags.append(tag)

    def remove_tag(self, tag: str):
        """Remove a tag from the person if it exists."""
        if tag in self.tags:
            self.tags.remove(tag)

    def add_disconnect(self, disconnect_id: int):
        """Add a new disconnect event."""
        self.disconnects.append(disconnect_id)
    
    def add_connect(self, connect_id):
        self.connects.append(connect_id)

    def __repr__(self):
        return (f"Person(name={self.name}, id={self.id}, age={self.age}, "
                f"tags={self.tags}, disconnects={self.disconnects})")

