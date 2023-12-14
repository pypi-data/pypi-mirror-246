import base64
from web3 import Web3
from eth_account.messages import encode_defunct
from datetime import datetime, timedelta, timezone

class AGInet:
    async def validate(self, request, validation=None, timeout=None, exception_class=None, response_model=None):
        print(f"1. GOT REQUEST: {request}")
        # Check for "agent-upload-test" header
        if "agent-upload-test" in request.headers:
            return response_model(response="pong")
        print(f"2. COMPLETED TEST, NOT A REGISTRATION TEST")

        # Check for required headers
        validation_headers = ['AGIWallet', 'AGISignedMessage', 'AGIRawMessage', 'AGISignedAt']
        if not all(header in request.headers for header in validation_headers):
            if exception_class is not None:
                raise exception_class(status_code=400, detail="Missing some validation headers")
            else:
                # TODO: this needs work because we should make it possible to return the exception they want
                return response_model(response="pong")
        print(f"3. VALIDATION HEADERS ARE PRESENT")

        # Verify signature
        wallet_address = request.headers["AGIWallet"]
        signed_message = request.headers["AGISignedMessage"]
        raw_message = None
        try:
            raw_message = base64.b64decode(request.headers["AGIRawMessage"]).decode()
        except (base64.binascii.Error, UnicodeDecodeError):
            if exception_class is not None:
                raise exception_class(status_code=400, detail="Invalid base64 encoding in AGIRawMessage header")
            else:
                # TODO: this needs work because we should make it possible to return the exception they want

                return response_model(response="Invalid base64 encoding in AGIRawMessage header")
        signed_at = request.headers["AGISignedAt"]

        print(f"4. GOT DECODED MESSAGE: {raw_message}")

        # Check for timeout
        if timeout is not None:
            signed_at_datetime = datetime.strptime(signed_at, "%Y-%m-%dT%H:%M:%S.%fZ").replace(tzinfo=timezone.utc)            
            if datetime.now(timezone.utc) - signed_at_datetime > timedelta(seconds=timeout):                
                print(f"ERROR: SIGNATURE OUTDATED")
                if exception_class is not None:
                    raise exception_class(status_code=400, detail="Signature has expired")
                else:
                    # TODO: this needs work because we should make it possible to return the exception they want

                    return response_model(response="Signature has expired")
        print(f"5. SIGNATURE IS WITHIN ACCEPTABLE TIME WINDOW")

        w3 = Web3()
        hex_message = encode_defunct(text=raw_message)
        recovered_address = w3.eth.account.recover_message(hex_message, signature=signed_message)

        if recovered_address.lower() != wallet_address.lower():
            if exception_class is not None:
                raise exception_class(status_code=400, detail="Invalid signature")
            else:
                # TODO: this needs work because we should make it possible to return the exception they want
                return response_model(response="Invalid signature")

        return True