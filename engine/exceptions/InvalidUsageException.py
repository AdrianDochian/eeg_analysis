class InvalidUsageException(Exception):
    def __init__(self, reason, parameter):
        message_format = "You can't use parameter `{}` for `{}`"
        message = message_format.format(parameter, reason)
        super().__init__(self, message)
