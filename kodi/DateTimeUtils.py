from datetime import datetime


class DateTimeUtils:

    @staticmethod
    def datetime_to_str(dt: datetime) -> str:
        return dt.strftime("%m/%d/%Y, %H:%M:%S")

    @staticmethod
    def generate_dir_name() -> str:
        return datetime.now().strftime("%m%d%Y%H%M")
