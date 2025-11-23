from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    description: str | None = None
    address: str
    logo_url: str
    latitude: float
    longitude: float


class CompanyCreate(CompanyBase):
    pass


class Company(CompanyBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
