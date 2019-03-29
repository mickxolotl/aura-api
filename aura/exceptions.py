# -*- coding: utf-8 -*-
class AuraException(Exception):
    pass


class AuraAuthError(AuraException):
    pass


class AuraAPIError(AuraException):
    def __init__(self, error):
        self.error = error

    def __str__(self):
        if 'code' in self.error and 'errors' in self.error:
            return 'Aura API Error [%s]: %s' % (self.error['code'], self.error['errors'])
        else:
            return super(AuraAPIError, self).__str__()
