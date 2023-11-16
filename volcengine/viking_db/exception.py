# coding:utf-8
class OtherException(Exception):
    def __init__(self, code, request_id, message=None):
        self.code = code
        self.request_id = request_id
        self.message = "{}, code:{}，request_id:{}".format(message, self.code, self.request_id)

    def __str__(self):
        return self.message


class UnauthorizedException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class NoPermissionException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidRequestException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class CollectionExistException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class CollectionNotExistException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class OperationNotAllowedException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexExistException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexNotExistException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class QueryOpFailedException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class DataNotFoundException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class DelOpFailedException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class UpsertOpFailedException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class TokenMismatchException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidQueryVecException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidPrimaryKeyException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidPartitionException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidScalarCondException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class InvalidProxyServiceException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexRecallException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexFetchDataException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class IndexNotReadyException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class APINotImplementedException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class CalcEmbeddingFailedException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class ListEmbeddingModelsException(OtherException):
    def __init__(self, code, request_id, message=None):
        super().__init__(code, request_id, message)


class VikingDBException(OtherException):
    def __init__(self, code, request_id, message=None):
        self.code = code
        self.request_id = request_id
        if message is not None:
            self.message = message
        else:
            self.message = "unknown error, please contact customer service, request_id:{}".format(self.request_id)

    def __str__(self):
        return self.message


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
    1000028: VikingDBException,

}

# volcanoOK             errCode = 0
# volcanoErrUnauthorized             errCode = 1000001
# volcanoErrNoPermission             errCode = 1000002
# volcanoErrInvalidRequest             errCode = 1000003
# volcanoErrCollectionExist             errCode = 1000004
# volcanoErrCollectionNotExist             errCode = 1000005
# volcanoErrOperationNotAllowed             errCode = 1000006
# volcanoErrIndexExist             errCode = 1000007
# volcanoErrIndexNotExist            errCode = 1000008
# volcanoErrQueryOpFailed            errCode = 1000010
# volcanoErrDataNotFound            errCode = 1000011
# volcanoErrDelOpFailed            errCode = 1000013
# volcanoErrUpsertOpFailed            errCode = 1000014
# volcanoErrTokenMismatch            errCode = 1000015
# volcanoErrInvalidQueryVec		   errCode = 1000016
# volcanoErrInvalidPrimaryKey		   errCode = 1000017
# volcanoErrInvalidPartition		   errCode = 1000018
# volcanoErrInvalidScalarCond        errCode = 1000019
# volcanoErrInvalidProxyService      errCode = 1000020
# volcanoErrIndexRecall              errCode = 1000021
# volcanoErrIndexFetchData              errCode = 1000022
# volcanoErrIndexNotReady              errCode = 1000023
# volcanoErrAPINotImplemented             errCode = 1000024
# volcanoErrCalcEmbeddingFailed            errCode = 1000025
# volcanoErrListEmbeddingModels            errCode = 1000026
# volcanoErrInternal                errCode = 1000028
