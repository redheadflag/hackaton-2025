from db.models import Channel
from db.repositories.crud import CRUDRepository


channel_repository = CRUDRepository(Channel)
