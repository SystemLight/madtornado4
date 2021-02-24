from abc import ABC
from typing import Dict


class IModel(ABC):

    @property
    def data(self) -> Dict:
        obj = dict()
        for key in self.__dict__.keys():
            k = key.split("__")[1]
            v = getattr(self, k)
            if isinstance(v, IModel):
                obj[k] = v.__dict__
            elif isinstance(v, list):
                obj[k] = list(map(lambda _: _.__dict__, v))
            else:
                obj[k] = v
        return obj
