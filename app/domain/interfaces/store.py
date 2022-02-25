"""
Store define different storage interraction used in the project.
It is an abstract definition that can be implemented in different form
or for various adapters.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, List

from app.domain import entity


class Players(ABC):
    """Manage player storages"""

    @abstractmethod
    def insert(self, player: entity.Player):
        """Add player to storage"""

    @abstractmethod
    def select(self, player_id: str) -> entity.Player:
        """Recover a specific player from storage"""

    @abstractmethod
    def list(self) -> List[entity.Player]:
        """List all known players"""


class Conversations(ABC):
    """Manage conversation storage"""

    @abstractmethod
    def insert(self, conversation: entity.Conversation):
        """Add conversation to storage"""

    @abstractmethod
    def update(self, conversation: entity.Conversation):
        """Update conversation from storage"""

    @abstractmethod
    def select(self, conversation_id: str) -> entity.Conversation:
        """Recover a specific conversation from storage"""

    @abstractmethod
    def list_for_players(self, player_id: str) -> List[entity.Conversation]:
        """List provided player conversations"""

    @abstractmethod
    def list_messages(self, conversation_id: str) -> List[entity.Conversation.Message]:
        """List all messages in conversations"""

    @abstractmethod
    def add_message(self, message: entity.Conversation.Message):
        """Add message to conversation"""

    @abstractmethod
    def get_latest_recieved_message(
        self, conversation_id: str, player_id: str
    ) -> entity.Conversation.Message:
        """Get latest message recieved by player in conversation"""


class Transactions(ABC):
    """
    Transaction interface abstract transaction management
    to uniformise calls for different requirements
    """

    @abstractmethod
    def start(self) -> Transactions:
        """Init a write only transaction"""

    @abstractmethod
    def commit(self) -> None:
        """Commit transaction to storage"""

    @abstractmethod
    def rollback(self) -> None:
        """Rollback cancel transaction"""

    @abstractmethod
    def instance(self) -> Any:
        """Provide concrete transaction instance to user"""

    @abstractmethod
    def clear(self) -> None:
        """Fully reset transaction instance"""
