from datetime import datetime
from cerberus import Validator
from cerberus.errors import ErrorDefinition
from common.utils.aws_utils import get_constant

END_DATE: any = ErrorDefinition(0x106, None)


class CustomValidator(Validator):
    def _validate_greater_date(self, constraint, field, value):
        """
        {'type': 'string'}
        """
        try:
            beginning_date = datetime.strptime(self.document[constraint], '%Y-%m-%dT%H:%M:%S.%fZ')
            end_date = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%fZ')
            if beginning_date > end_date:
                self._error(field, END_DATE, get_constant('FIELD_NAME', 'begin', '期間設定開始日'))
        except TypeError:
            pass
        except ValueError:
            pass
