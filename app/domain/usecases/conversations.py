from datetime import datetime
from typing import List
from uuid import uuid4

from app.core import Context, Log, ReservedAdmin
from app.domain import entity
from app.domain.errors import ErrInvalidData, ErrNotFound, ErrUnauthorized, ErrUnexpected
from app.domain.interfaces import store
from shortuuid import uuid


class Conversation:
    def __init__(self, store: store.Conversations, playerStore: store.Players, log: Log):
        self.__log = log.named("usecases.conversation")
        self.__store = store
        self.__players = playerStore

    def new(self, player_ids: List[str]) -> entity.Conversation:
        log = self.__log.method("new").parameter("players", player_ids)

        try:
            players = [self.__players.select(player) for player in player_ids]
        except ErrNotFound as e:
            log.exception(e).info("A player does not exists")
            raise e
        except Exception as e:
            log.error("Could not check players", e)
            raise ErrUnexpected().to_precise("CannotCheckPlayers")

        conversation = entity.Conversation(id=str(uuid4()), players=players)
        creation_message = self.__system_message(conversation.id, "created")

        log.parameter("conversation", conversation)

        try:
            self.__store.insert(conversation)
            self.__store.add_message(creation_message)
        except ErrInvalidData as e:
            log.exception(e).info("Invalid conversation")
            raise e
        except Exception as e:
            log.error("Could not insert", e)
            raise ErrUnexpected().to_precise("CannotCreateConversation") from e
        else:
            log.success()
            return conversation

    def get(self, conversation_id: str) -> entity.Conversation:
        log = self.__log.method("get").parameter("conversation", conversation_id)

        try:
            conversation = self.__store.select(conversation_id)
        except ErrNotFound as e:
            log.info("Not found")
            raise e
        except Exception as e:
            log.error("Could not read", e)
            raise ErrUnexpected().to_precise("CannotRetrieveConversation") from e
        else:
            log.success()
            return conversation

    def list_for_player(self, player_id: str) -> List[entity.Conversation]:
        log = self.__log.method("list_for_player").parameter("player_id", player_id)

        try:
            conversations = self.__store.list_for_players(player_id)
        except Exception as e:
            log.error("Could not read", e)
            raise ErrUnexpected().to_precise("CannotRetrieveConversations") from e
        else:
            log.success()
            return conversations

    def read(self, ctx: Context, read_by: str, conversation_id: str) -> entity.Conversation:
        log = (
            self.__log.method("read")
            .parameter("conversation_id", conversation_id)
            .parameter("read_by", read_by)
            .context(ctx)
        )

        try:
            conversation = self.__store.select(conversation_id)
        except ErrNotFound as e:
            log.exception(e).info("Conversation does not exists")
            raise e
        except Exception as e:
            log.error("Cannot retrieve conversation", e)
            raise ErrUnexpected().to_precise("CannotRetrieveConversation") from e

        player = self.__assert_player_in_conversation(conversation, log, read_by)

        try:
            last_received_message = self.__store.get_latest_recieved_message(
                conversation_id, player.id
            )
        except ErrNotFound:
            log.success("No message from others")
            return conversation
        except Exception as e:
            log.error("Could not retrieve latest message", e)
            raise ErrUnexpected().to_precise("CannotRetrieveLatestMessage") from e

        if conversation.latest_read_message.get(player.id, "") == last_received_message.id:
            log.success("Already latest read")
            return conversation

        conversation.latest_read_message[player.id] = last_received_message.id

        try:
            self.__store.update(conversation)
        except Exception as e:
            log.error("Cannot update conversation", e)
            raise ErrUnexpected().to_precise("CannotUpdateConversation") from e
        else:
            log.success()
            return conversation

    def toggle_mask(
        self, ctx: Context, conversation_id: str, masked_by: str
    ) -> entity.Conversation:
        log = (
            self.__log.method("toggle_mask")
            .parameter("conversation_id", conversation_id)
            .parameter("masked_by", masked_by)
            .context(ctx)
        )

        try:
            conversation = self.__store.select(conversation_id)
        except ErrNotFound as e:
            log.exception(e).info("Conversation does not exists")
            raise e
        except Exception as e:
            log.error("Cannot retrieve conversation", e)
            raise ErrUnexpected().to_precise("CannotRetrieveConversation") from e

        self.__assert_player_in_conversation(conversation, log, masked_by)

        if masked_by in conversation.masked_by:
            conversation.masked_by.remove(masked_by)
        else:
            conversation.masked_by.append(masked_by)

        try:
            self.__store.update(conversation)
        except Exception as e:
            log.error("Cannot update conversation", e)
            raise ErrUnexpected().to_precise("CannotUpdateConversation") from e
        else:
            log.success()
            return conversation

    def send_message(
        self, ctx: Context, message: entity.Conversation.Message
    ) -> entity.Conversation.Message:
        log = self.__log.method("list_mesages").parameter("message", message).context(ctx)

        try:
            conversation = self.__store.select(message.conversation_id)
        except ErrNotFound as e:
            log.exception(e).info("Conversation does not exists")
            raise e
        except Exception as e:
            log.error("Cannot retrieve conversation", e)
            raise ErrUnexpected().to_precise("CannotRetrieveConversation") from e

        self.__assert_player_in_conversation(conversation, log, message.send_by)

        if message.send_by in conversation.masked_by:
            log.info("Masked conversation")
            raise ErrInvalidData("conversation", "masked")

        message.id = str(uuid())

        try:
            self.__store.add_message(message)
        except Exception as e:
            log.error("Cannot create message", e)
            raise ErrUnexpected().to_precise("CannotCreateMessage") from e
        else:
            log.success()
            return message

    def list_mesages(
        self, ctx: Context, conversation_id: str, player_id: str
    ) -> List[entity.Conversation.Message]:
        log = (
            self.__log.method("list_mesages")
            .parameter("conversation_id", conversation_id)
            .context(ctx)
        )

        try:
            conversation = self.__store.select(conversation_id)
        except ErrNotFound as e:
            log.exception(e).info("Conversation does not exists")
            raise e
        except Exception as e:
            log.error("Cannot retrieve conversation", e)
            raise ErrUnexpected().to_precise("CannotRetrieveConversation") from e

        self.__assert_player_in_conversation(conversation, log, player_id)

        if player_id in conversation.masked_by:
            log.info("Masked conversation")
            raise ErrInvalidData("conversation", "masked")

        player = None
        for candidate in conversation.players:
            if candidate.id == player_id:
                player = candidate
                break

        if not player:
            raise ErrUnauthorized()

        try:
            messages = self.__store.list_messages(conversation.id)
        except Exception as e:
            log.error("Cannot retrieve messages", e)
            raise ErrUnexpected().to_precise("CannotRetrieveMessages") from e
        else:
            log.success()
            return messages

    @staticmethod
    def __assert_player_in_conversation(
        conversation: entity.Conversation, log: Log, player_id: str
    ) -> entity.Player:
        player = None
        for candidate in conversation.players:
            if candidate.id == player_id:
                player = candidate
                break

        if not player:
            log.parameter("not_in_conv", player_id).info("Player not in conversation")
            raise ErrUnauthorized()

        return player

    @staticmethod
    def __system_message(conversation: str, message: str, **meta) -> entity.Conversation.Message:
        return entity.Conversation.Message(
            id=str(uuid4()),
            conversation_id=conversation,
            send_by=ReservedAdmin.BOY,
            content=message,
            metadata=meta,
            send_at=datetime.utcnow(),
        )
