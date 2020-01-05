class PlayerState:
    def __init__(self, player_id: int, playlist_id: int, speed: int, shuffled: bool, repeat: str):
        self.player_id = player_id
        self.playlist_id = playlist_id
        self.speed = speed
        self.shuffled = shuffled
        self.repeat = repeat
