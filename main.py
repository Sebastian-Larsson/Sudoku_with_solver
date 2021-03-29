import pygame
import numpy as np
from settings import Settings

# Sudoku puzzle
puzzle = [[4, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 9, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 7, 8, 5],
              [0, 0, 7, 0, 4, 8, 0, 5, 0],
              [0, 0, 1, 3, 0, 0, 0, 0, 0],
              [0, 0, 6, 0, 7, 0, 0, 0, 0],
              [8, 6, 0, 0, 0, 0, 9, 0, 3],
              [7, 0, 0, 0, 0, 5, 0, 6, 2],
              [0, 0, 3, 7, 0, 0, 0, 0, 0]]

# User input numbers along with original numbers
digits = np.array(puzzle).T

# Save original, will not be altered
original_numbers = np.array(puzzle).T


class SudokuGame:
    def __init__(self):
        pygame.init()
        self.running = True
        self.settings = Settings()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.board, self.squares = self.draw_board()
        self.selected = (10, 10)
        self.update_board()

    def update_board(self, change_color=False):
        font_1 = pygame.font.SysFont('couriernew', 24)

        # Find which square has been clicked
        x_cord, y_cord = pygame.mouse.get_pos()
        x_cord = x_cord // self.settings.square_size
        y_cord = y_cord // self.settings.square_size
        for x in range(9):
            for y in range(9):
                square = pygame.Surface((self.settings.square_size, self.settings.square_size))
                if x_cord == x and y_cord == y:

                    # Set selected square and mark it red
                    self.selected = (x_cord, y_cord)
                    if change_color:
                        square.fill((255, 0, 0))
                    else:
                        square.fill((255, 255, 255))
                else:
                    square.fill((255, 255, 255))

                # If square has a number
                if digits[x, y] != 0:

                    # Original numbers have black color and user input ones have a blue color
                    if original_numbers[x, y] != 0:
                        numbers = font_1.render(str(int(digits[x, y])), True, (0, 0, 0))
                    else:
                        numbers = font_1.render(str(int(digits[x, y])), True, (97, 83, 230))
                    square.blit(numbers, (25 - numbers.get_width() / 2, 25 - numbers.get_width() / 2))
                self.squares.append(self.board.blit(square, ((x * self.settings.square_size),
                                                             (y * self.settings.square_size))))

        # Draw sudoku board
        for line in range(10):
            if line % 3 == 0:
                pygame.draw.line(self.board, (0, 0, 0), (line * self.settings.square_size, 0),
                                 (line * self.settings.square_size, self.settings.board_size[1]), 3)
                pygame.draw.line(self.board, (0, 0, 0), (0, line * self.settings.square_size),
                                 (self.settings.board_size[0], line * self.settings.square_size), 3)
            else:
                pygame.draw.line(self.board, (0, 0, 0), (line * self.settings.square_size, 0),
                                 (line * self.settings.square_size, self.settings.board_size[1]))
                pygame.draw.line(self.board, (0, 0, 0), (0, line * self.settings.square_size),
                                 (self.settings.board_size[0], line * self.settings.square_size))

    # Game loop
    def run_game(self):
        while self.running:
            self.check_events()
            self.update_screen()

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONUP:
                for square in self.squares:
                    if square.collidepoint(pygame.mouse.get_pos()):
                        self.update_board(change_color=True)  # Square was clicked and should be highlighted
                        break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.backtracking(0, 0)
                else:
                    if self.selected != (10, 10):
                        x, y = self.selected
                    else:
                        x, y = pygame.mouse.get_pos()
                        x = x // self.settings.square_size
                        y = y // self.settings.square_size
                    if original_numbers[x, y] == 0:
                        digits[x, y] = chr(event.key)
                    self.update_board()
                    self.selected = (10, 10)

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.screen.blit(self.board, (0, 0))
        pygame.display.flip()

    # Init squares and the board itself
    def draw_board(self):
        squares = []
        board = pygame.Surface(self.settings.board_size)
        board.fill((255, 255, 255))
        for x in range(9):
            for y in range(9):
                square = pygame.Surface((self.settings.square_size, self.settings.square_size))
                square.fill((255, 255, 255))
                squares.append(board.blit(square, ((x * self.settings.square_size), (y * self.settings.square_size))))
        return board, squares

    """Solving algorithm, activate by pressing the Enter key. 
    
    The user can fill in squares which will decrease the time it takes to complete the sudoku. Providing numbers that
    are incorrect will cause the algorithm to not find a solution.
    """
    def backtracking(self, row, col):
        self.update_board()
        self.update_screen()
        if row == 8 and col == 9:
            return True

        if col == 9:
            row += 1
            col = 0

        if digits[row, col] != 0:
            return self.backtracking(row, col + 1)

        for number in range(1, 10, 1):
            if number_possible(row, col, number):
                digits[row, col] = number
                if self.backtracking(row, col + 1):
                    return True
            digits[row, col] = 0
        return False


def number_possible(row, col, number):
    if number in digits[row, :]:
        return False
    if number in digits[:, col]:
        return False

    square_row = row - row % 3
    square_col = col - col % 3
    for x in range(3):
        for y in range(3):
            if digits[square_row + x, square_col + y] == number:
                return False
    return True


if __name__ == "__main__":
    sudoku_game = SudokuGame()
    sudoku_game.run_game()
