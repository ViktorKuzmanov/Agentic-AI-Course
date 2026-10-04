from ast import Add
from dataclasses import field
from pydantic import BaseModel, EmailStr, AnyUrl, Field, field_validator, model_validator, computed_field
from typing import List, Dict, Optional, Annotated

class Address(BaseModel):
    city: str
    state: str 
    pin: str

class Pacient(BaseModel):
    ime: str = Field(max_length=6)
    email: EmailStr
    linkedIn: AnyUrl
    tezina: float
    visina: float
    vozrast: int = Field(gt=0, lt=150)
    voBrak: Annotated [ bool, Field(default=False, description="Dali si u brak") ] 
    alergii: Optional[List[str]] = None
    contact_info: Dict[str, str]
    address: Address

    @field_validator("email")
    @classmethod
    def email_validator(classObject, value):
        valid_domains = ["kb.com", "nlb.com"]
        # izvadi go samo domain delot
        domain_name = value.split("@")[-1]
        if domain_name not in valid_domains:
            raise ValueError("Not a valid domain")
        return value
    
    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.tezina/(self.visina**2),2)
        return bmi


    @field_validator("ime")
    @classmethod
    def transform_name(classObject, value):
        return value.upper()

    @model_validator(mode="after")
    def validate_emergency_contact(self):
        if self.vozrast > 60 and 'emergency' not in self.contact_info:
            raise ValueError('ako pacientot e nad 60 godini treba da ima emergency kontakt')
        return self

def dodajPacient(pacient: Pacient):
    print(pacient.ime)
    print(pacient.vozrast)
    print(pacient.bmi)
    print(pacient.address.city)
    print("se dodade pacient")

def updatePacient(pacient: Pacient):
    print(pacient.ime)
    print(pacient.vozrast)
    print("se update pacient")

adresa_dict = {'city':'Kavadarci', 'state': 'Macedonia', 'pin': '1430'}
adresa = Address(**adresa_dict)

pacientPodatoci1 = {"ime": "viktor", 
                    "email": "viktor@kb.com",
                    "linkedIn": "https://www.linkedin.com/in/viktorkuzmanov/",
                    "tezina": '70.5',
                    "visina": '1.75',
                    "vozrast": 62, 
                    "voBrak":True, 
                    "alergii": ["alergija 1.0", "alergija 1.1"], 
                    "contact_info": {"broj":"567", "emergency":"193"},
                    'address': adresa
                    }



pacient1 = Pacient(**pacientPodatoci1)

dodajPacient(pacient1)

# export the object as dictionary
dictPacient = pacient1.model_dump()
print(dictPacient)
print(type(dictPacient))

# export the object as string json
jsonObjectPacient = pacient1.model_dump_json()
print(jsonObjectPacient)
print(type(jsonObjectPacient))

# pacientPodatoci2 = {"ime": "Branko", "vozrast": 52}
# pacient2 = Pacient(**pacientPodatoci2)






