# -*- coding: utf-8 -*-
class AuraException(Exception):
    pass

class AuraAuthError(AuraException):
    pass

class AuraAPIError(AuraException):
    pass
