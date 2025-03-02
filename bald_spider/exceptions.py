

class TransformTypeError(TypeError):
    pass


class OutputError(Exception):
    pass


class SpiderTypeError(TypeError):
    pass


class ItemInitError(Exception):
    pass


class ItemAttributeError(Exception):
    pass


class DecodeError(Exception):
    pass


class MiddlewareInitError(Exception):
    pass


class InvalidOutput(Exception):
    pass


class RequestMethodError(Exception):
    pass


class IgnoreRequest(Exception):

    def __init__(self, msg):
        self.msg = msg
        super(IgnoreRequest, self).__init__(msg)


class NotConfigured(Exception):
    pass


class ExtensionInitError(Exception):
    pass


class ReceiverTypeError(Exception):
    pass


class PipelineInitError(Exception):
    pass


class ItemDiscard(Exception):

    def __init__(self, msg):
        self.msg = msg
        super(ItemDiscard, self).__init__(msg)