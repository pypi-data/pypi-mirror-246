import base64
import binascii

from web3 import Web3
from eth_account.messages import encode_defunct
from datetime import datetime, timedelta, timezone
from typing import List, Set, Optional

from pydantic import BaseModel, validator, root_validator, Field

class Validation(BaseModel):
    valid: bool = Field(..., description="Whether the signature is valid or not")
    address: str = Field(default=None, description="Verified address that created the signature, if valid.")
    response: str = Field(default=None, description="Additional details, such as errors, that happened during validation.")
class AGInet:
    """
    Function to handle a variety of basic validation tasks, including:

    - Check if the request coming in is real or is a test from uploading an agent
    - Check if the request coming in has necessary secrets in headers
    - Check whether the raw and signed messages are valid via decoding them
    - Check if the signature was issued within the timeout criteria

    timeout is measured in seconds
    """
    async def validate(self, 
        request, 
        validation: Optional[str] = None, 
        timeout: Optional[int] = None, 
        secrets: Optional[List[str]] = None, 
        exception_class=None
    ) -> Validation:
        
        if not validation:
            return Validation(valid=True, response="No validation was performed.")
        elif validation != "signature":
            return Validation(valid=False, response="This validation method is not currently supported. Try setting validation to `signature`")

        # This is to check if this is a request coming in from a client during registration
        # The goal of this is to check if the URL is actually reachable
        if "agent-upload-test" in request.headers:
            return Validation(valid=True, response="pong")
        
        # Check if the list of secrets is present in the header, case-sensitive
        if secrets:
            if not all(secret in request.headers for secret in secrets):
                if exception_class is not None:
                    raise exception_class(status_code=400, detail="Missing some secrets in the headers")
                else:
                    return Validation(valid=False, address="Missing some secrets in the headers")
            
        validation_headers = ['AGIWallet', 'AGISignedMessage', 'AGIRawMessage', 'AGISignedAt']
        if not all(header in request.headers for header in validation_headers):
            if exception_class is not None:
                raise exception_class(status_code=400, detail="Missing some validation headers")
            else:
                return Validation(valid=False, address="Missing some validation headers")

        # Verify signature
        wallet_address = request.headers["AGIWallet"]
        signed_message = request.headers["AGISignedMessage"]
        raw_message = None
        try:
            raw_message = base64.b64decode(request.headers["AGIRawMessage"]).decode()
        except (binascii.Error, UnicodeDecodeError):
            if exception_class is not None:
                raise exception_class(status_code=400, detail="Invalid base64 encoding in AGIRawMessage header")
            else:
                return Validation(valid=False, response="Invalid base64 encoding in AGIRawMessage header")
        signed_at = request.headers["AGISignedAt"]

        # Check for timeout
        if timeout is not None:
            signed_at_datetime = datetime.strptime(signed_at, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)            
            if datetime.now(timezone.utc) - signed_at_datetime > timedelta(seconds=timeout):                
                if exception_class is not None:
                    raise exception_class(status_code=400, detail="Signature has expired")
                else:
                    return Validation(valid=False, response="Signature has expired")

        w3 = Web3()
        hex_message = encode_defunct(text=raw_message)
        recovered_address = w3.eth.account.recover_message(hex_message, signature=signed_message)

        if recovered_address.lower() != wallet_address.lower():
            if exception_class is not None:
                raise exception_class(status_code=400, detail="Signature does not match wallet")
            else:
                return Validation(valid=False, response="Signature does not match wallet")

        return Validation(valid=True, address=recovered_address.lower(), response="Signature is valid")
    
    """
    Function to handle checking whether the verified address is in a given allowlist.

    Depending on the source type, performs different functions:

    Files: line delimited .txt, jsonl, json, csv, maybe others
    URL: api call, hosted file
    Variable: just passed in
    """
    async def allowlist(self,
        address: str,
        variable: Optional[Set] = None, 
        api_url: Optional[str] = None, 
        file_url: Optional[str] = None, 
        file_path: Optional[str] = None, 
        exception_class = None
    ) -> Validation:
        
        parameters = [variable, api_url, file_url, file_path]
        non_none_parameters = [parameter for parameter in parameters if parameter is not None]

        if len(non_none_parameters) != 1:
            if exception_class:
                raise exception_class(status_code=400, detail="Exactly one parameter must be not None")
            else:
                return Validation(valid=False, response="Exactly one parameter must be not None")
        
        if not variable:
            if exception_class:
                raise exception_class(status_code=400, detail="Currently this library only accepts a variable as a allowlist source")
            else:
                return Validation(valid=False, response="Currently this library only accepts a variable as a allowlist source")
        
        # variable is required to be a Set, should test this
        address = address.lower()
        allowlist = {item.lower() for item in variable}

        if address in allowlist:
            return Validation(valid=True, address=address, response="Address is in provided allowlist.")
        else:
            return Validation(valid=False, address=address, response="Address is not found in provided allowlist.")
        
        