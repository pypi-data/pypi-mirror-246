from typing import Callable

class LayoutCNABException(Exception):
    pass

def raiseLayoutCNABException(msg) -> Callable:
    def __raise():
        raise LayoutCNABException(msg)
    return __raise