import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from typing import List, Dict
import numpy as np
from API.generate_embeds import get_ocean_embeds

class Person:
    def __init__(
        self,
        name: str,
        tags: List[str],
        age: int,
        id: int = 0,
        prompt_responses: Dict[str, str] = [],
        O_embed: List[float] = [],
        C_embed: List[float] = [],
        E_embed: List[float] = [],
        A_embed: List[float] = [],
        N_embed: List[float] = [],
        disconnects: List[int] = [],
        connects: List[int] = []
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
        self.prompt_responses = prompt_responses
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

    def add_prompt_response(self, prompt_resonse):
        self.prompt_responses.append(prompt_resonse)

    def __repr__(self):
        return (f"Person(name={self.name}, id={self.id}, age={self.age}, "
                f"tags={self.tags}, disconnects={self.disconnects})")
    

def generate_embeds(p1: Person):
    prompt_list = p1.prompt_responses
    ocean_embeds = get_ocean_embeds(Ocean=prompt_list)

    p1.O_embed = ocean_embeds['O']
    p1.C_embed = ocean_embeds['C']
    p1.E_embed = ocean_embeds['E']
    p1.A_embed = ocean_embeds['A']
    p1.N_embed = ocean_embeds['N']

