# from numlookupapi import PhoneNumberValidator
from numlookupapi import PhoneNumberValidator

class PhoneNumberValidatorWrapper:
    def __init__(self, api_key):
        """
        Initializes an instance of the class.

        Args:
            api_key (str): The API key to use for authentication.

        Returns:
            None
        """
        self.validator = PhoneNumberValidator(api_key)

    def validate(self, phone_number):
        """
        Validates a phone number.

        Args:
            phone_number (str): The phone number to be validated.

        Returns:
            bool: True if the phone number is valid, False otherwise.
        """
        return self.validator.validate(phone_number)
