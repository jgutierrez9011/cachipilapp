from pydantic import BaseModel


class StorePublicOut(BaseModel):
    name: str
    slug: str
    whatsapp_e164: str
