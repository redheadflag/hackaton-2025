from db.models import Message
from db.repositories.crud import CRUDRepository


message_repository = CRUDRepository(Message)
