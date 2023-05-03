"""Modulo describes each of the value objects used within the Duel aggregate"""
import uuid
from typing import Tuple

from domain import IEntityID


class EntityID(IEntityID, uuid.UUID):
    """Represents a value object specialized in working with entity IDs.

    It is capable of generating unique IDs, whether or not based on the namespace.
    : fonte_unica = None
        Utiliza o algoritmo uuid4 para gerar um ID pseudoaleatorio
    : fonte_unica = <str>
        Utiliza o algoritmo uuid5 (SHA-1) para gerar um ID pseudoaleatorio recuperavel.
        Nesse caso o ID pode ser recuperado utilizando sua fonte (fonte_unica)
    : uuid_string = <str>
        Utiliza o uuid string como base para criacao deste ID

    Quando instanciar esta classe com um parametro de namespace, certifique-se de
    utilizar uma fonte_unica, ou seja, apenas em casos os quais estiver trabalhando
    com entidades que tenham atributos unicos, como numero de celular, ou cpf, dessa forma,
    o algoritmo SHA-1 sempre entregara hashs com uma probabilidade infema de colisao!
    """

    def __init__(self, fonte_unica: str | None = None, uuid_string: str | None = None):
        if fonte_unica is not None:
            super().__init__(str(uuid.uuid5(uuid.NAMESPACE_DNS, fonte_unica)), version=5)
        elif uuid_string is not None:
            super().__init__(uuid_string)
        else:
            super().__init__(str(uuid.uuid4()), version=4)

    def __eq__(self, entity_id: object) -> bool:
        if not isinstance(entity_id, EntityID):
            return False
        return super().__eq__(entity_id)

    def __mul__(self, quantidade_de_instancias: int) -> Tuple["EntityID", ...]:
        return tuple(EntityID() for _ in range(quantidade_de_instancias))

    def __rmul__(self, quantidade_de_instancias: int) -> Tuple["EntityID", ...]:
        return tuple(EntityID() for _ in range(quantidade_de_instancias))

    def __hash__(self) -> int:
        return super().__hash__()
