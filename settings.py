class Settings:

    def __init__(self):
        self.screen_width, self.screen_height = 450, 450
        self.bg_color = (0, 0, 0)
        self.board_size = (450, 450)
        self.square_size = int(self.board_size[0]/9)
