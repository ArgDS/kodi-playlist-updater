from datetime import datetime


class DateTimeUtils:

    @staticmethod
    def datetime_to_str(dt: datetime) -> str:
        return dt.strftime("%m/%d/%Y, %H:%M:%S")
