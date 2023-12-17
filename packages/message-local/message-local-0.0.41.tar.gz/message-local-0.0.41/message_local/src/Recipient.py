import json
from enum import Enum, auto

# from user_context_remote.user_context import UserContext
from variable_local.variable import VariablesLocal

# user = UserContext()


class ReferenceType(Enum):
    PERSON_ID = auto()
    CONTACT_ID = auto()
    USER_ID = auto()
    PROFILE_ID = auto()


class RecipientType(Enum):
    TELEPHONE_NUMBER = auto()
    EMAIL_ADDRESS = auto()

    UNKNOWN = auto()


class Recipient:
    __main_recipient_type: RecipientType = None

    def __init__(self, contact_id: int = None, person_id: int = None, user_id: int = None, profile_id: int = None,
                 telephone_number: str = None, email_address: str = None):
        self.__person_id = person_id
        self.__email_address = email_address
        self.__contact_id = contact_id
        self.__user_id = user_id
        self.__profile_id = profile_id
        self.__telephone_number = telephone_number

        for key, value in self.to_json().items():
            if not key.endswith("id"):
                self._recipient_type = RecipientType[key.upper()]  # remove the first underscore

        self.variable_local = VariablesLocal()
        # TODO: make sure those are stored on the effective_profile_id (using global user_context or sending the user_context).
        self.variable_local.add(self.__contact_id, "contact_id")
        self.variable_local.add(self.__person_id, "person_id")
        self.variable_local.add(self.__user_id, "user_id")
        self.variable_local.add(self.__profile_id, "profile_id")
        self.variable_local.add(self.__telephone_number, "telephone_number")
        self.variable_local.add(self.__email_address, "email_address")

    def get_person_id(self) -> int:
        return self.__person_id

    def get_profile_id(self) -> int:
        return self.__profile_id

    def is_email_address(self):
        return self.__telephone_number is not None

    def is_telephone_number(self):
        return self.__telephone_number is not None

    def get_email_address(self):
        return self.__email_address is not None

    def get_telephone_address(self):
        return self.__telephone_number is not None

    def get_canonical_telephone(self):
        # TODO I think this function is do not cover all cases - I believe we can find one in the internet
        if self.__telephone_number is None:
            return None
        if self.__telephone_number.startswith("+"):
            country_code = ""
        else:
            country_code = 972  # TODO country_code = user.get_country_id()

        # Remove non-numeric characters from the telephone number and leading zeroes
        cleaned_number = int(''.join(char for char in self.__telephone_number if char.isdigit()))

        cleaned_number = f"{country_code}{cleaned_number}"

        return cleaned_number

    def to_json(self):
        return {k.replace("_Recipient__", ""): v for k, v in self.__dict__.items()
                if v is not None and k.startswith("_Recipient__")}  # i.e. starts with __. We can also check init args

    def __str__(self):
        return json.dumps(self.to_json())


if __name__ == '__main__':
    recipient = Recipient(person_id=1, email_address="test@test")
    assert recipient.to_json() == {'person_id': 1, 'email_address': 'test@test'}
