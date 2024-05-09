# coding:utf-8
class VikingKnowledgeBaseServerException(Exception):
    def __init__(self, code, request_id, message=None):
        self.code = code
        self.request_id = request_id
        self.message = "{}, code:{}，request_id:{}".format(message, self.code, self.request_id)

    def __str__(self):
        return self.message


class UnauthorizedException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class NoPermissionException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidRequestException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class CollectionExistException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class CollectionNotExistException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class OperationNotAllowedException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexExistException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexNotExistException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class QueryOpFailedException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class DataNotFoundException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class DelOpFailedException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class UpsertOpFailedException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class TokenMismatchException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidQueryVecException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidPrimaryKeyException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidPartitionException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidScalarCondException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidProxyServiceException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexRecallException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexFetchDataException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexNotReadyException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class APINotImplementedException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class CalcEmbeddingFailedException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class ListEmbeddingModelsException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class VikingKnowledgeBaseException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        self.code = code
        self.request_id = request_id
        if message is not None:
            self.message = message
        else:
            self.message = "unknown error, please contact customer service, request_id:{}".format(self.request_id)

    def __str__(self):
        return self.message

class QuotaLimiterException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)

class RerankException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)

class DocNotExistException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)

class DocIsFullException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)

class PointNotExistException(VikingKnowledgeBaseServerException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)

ERRCODE_EXCEPTION = {
    1000001: UnauthorizedException,
    1000002: NoPermissionException,
    1000003: InvalidRequestException,
    1000004: CollectionExistException,
    1000005: CollectionNotExistException,
    1000006: OperationNotAllowedException,
    1000007: IndexExistException,
    1000008: IndexNotExistException,
    1000010: QueryOpFailedException,
    1000011: DataNotFoundException,
    1000013: DelOpFailedException,
    1000014: UpsertOpFailedException,
    1000015: TokenMismatchException,
    1000016: InvalidQueryVecException,
    1000017: InvalidPrimaryKeyException,
    1000018: InvalidPartitionException,
    1000019: InvalidScalarCondException,
    1000020: InvalidProxyServiceException,
    1000021: IndexRecallException,
    1000022: IndexFetchDataException,
    1000023: IndexNotReadyException,
    1000024: APINotImplementedException,
    1000025: CalcEmbeddingFailedException,
    1000026: ListEmbeddingModelsException,
    1000028: VikingKnowledgeBaseException,
    1000029: QuotaLimiterException,
    1000030: RerankException,

    1001001: DocNotExistException,
    1001010: DocIsFullException,	
    1002001: PointNotExistException,
}