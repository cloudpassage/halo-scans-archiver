import datetime
import re


class Utility(object):
    @classmethod
    def date_to_iso8601(cls, date_obj):
        """Returns an ISO8601-formatted string for datetime arg"""
        retval = date_obj.isoformat()
        return retval

    @classmethod
    def iso8601_arbitrary_days_ago(cls, days_ago):
        return Utility.date_to_iso8601(datetime.date.today() -
                                       datetime.timedelta(days=days_ago))

    @classmethod
    def target_date_is_valid(cls, start_date):
        """ Tests date stamp for validity """
        canary = re.compile(r'^\d{4}-\d{2}-\d{2}$')
        if canary.match(start_date):
            return True
        else:
            return False
