import base64
from loguru import logger

class CommonEncryptionHelper():

    def __init__(self):
        pass

    def encodeString(self, message):
        message_bytes = message.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_message = base64_bytes.decode('ascii')
        return base64_message

    def decodeString(self, base64_message):
        base64_bytes = base64_message.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        message = message_bytes.decode('ascii')
        return message

    def getSecret(self, secret, encryption=False):
        output=""
        if encryption == True \
        or encryption == "True":
            logger.info("Your secret is encrypted")
            output=self.decodeString(secret)
        else:
            logger.warning("!!! Your secret is shown as plain text !!!")
            logger.warning("your secret         : "+ secret)
            logger.warning("your secret encoded : "+ self.encodeString(secret))
            output=secret
        return output

if __name__ == "__main__":
    logger.disable("common.CommonMetaLogger")
    coder = CommonEncryptionHelper()
    base64_message = coder.encodeString("test")
    logger.info(base64_message)
    message = coder.decodeString(base64_message)

    logger.info(coder.getSecret("MyTestString"))
    logger.info(coder.getSecret("TXlUZXN0U3RyaW5n",True))
