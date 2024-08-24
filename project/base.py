# -*- coding: UTF-8 -*-
from abc import (
    ABCMeta,
    abstractmethod
)
from typing import Any


class BaseBroker(object, metaclass=ABCMeta):

    @abstractmethod
    def transact(self, order: Any, **kwargs):
        """
        Transact: deal with each order sequentially.

        Args:
            order (Any): Required.
        """
        raise NotImplementedError

    @abstractmethod
    def order_book(self, level: int = 5, **kwargs):
        """
        Order book: N level.

        Args:
            level (int): Optional, N-level, default is 5.
        """
        raise NotImplementedError


__all__ = [
    'BaseBroker'
]
