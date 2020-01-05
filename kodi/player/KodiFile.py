class KodiFile:
    def __init__(self, file: str, file_type: str, label: str, mime_type: str, thumbnail: str, title: str, type: str):
        self.file = file
        self.file_type = file_type
        self.label = label
        self.mime_type = mime_type
        self.thumbnail = thumbnail
        self.title = title
        self.type = type
