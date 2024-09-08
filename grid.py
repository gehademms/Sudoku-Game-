import pygame
from random import sample
from copy import deepcopy
from selection import Select

def create_line_coordinates(cell_size):
    coordinates = []
    for y in range(1, 9):
        horizontal_line = [(0, y * cell_size), (cell_size * 9, y * cell_size)]
        coordinates.append(horizontal_line)
    for x in range(1, 9):
        vertical_line = [(x * cell_size, 0), (x * cell_size, cell_size * 9)]
        coordinates.append(vertical_line)
    return coordinates

SUB_GRID_SIZE = 3
GRID_SIZE = SUB_GRID_SIZE * SUB_GRID_SIZE

def pattern(row_num, col_num):
    return (SUB_GRID_SIZE * (row_num % SUB_GRID_SIZE) + row_num // SUB_GRID_SIZE + col_num) % GRID_SIZE

def shuffle(samp: range):
    return sample(samp, len(samp))

def create_grid(sub_grid):
    """Creates the 9x9 grid filled with random numbers."""
    row_base = range(sub_grid)
    rows = [g * sub_grid + r for g in shuffle(row_base) for r in shuffle(row_base)]
    cols = [g * sub_grid + c for g in shuffle(row_base) for c in shuffle(row_base)]
    nums = shuffle(range(1, sub_grid * sub_grid + 1))
    return [[nums[pattern(r, c)] for c in cols] for r in rows]

class Grid:
    def __init__(self, font, pygame):
        self.cell_size = 67
        self.coordinates = create_line_coordinates(self.cell_size)
        self.font = font
        self.x_offset = 25
        self.y_offset = 10
        self.selection = Select(pygame, self.font)
        self.win = False
        self.start_time = pygame.time.get_ticks()  
        self.time_paused = False  
        self.show_help = False  
        self.recorded_time = 0  
        self.mistakes = 0  
        self.restart() 

    def getclick(self, x, y):
        if x <= 600:
            grid_x, grid_y = x // self.cell_size, y // self.cell_size
            if not self.is_cell_preoccupied(grid_x, grid_y):
                selected_num = self.selection.get_selected_number()
                if selected_num != 0: 
                    self.set_cell(grid_x, grid_y, selected_num)
        else:
            self.selection.button_clicked(x, y)
        if self.check_grids():
            self.win = True
            self.time_paused = True  
            self.recorded_time = (pygame.time.get_ticks() - self.start_time) // 1000  

    def set_cell(self, x, y, value):
        """Set the value of a cell and update mistakes if incorrect."""
        current_value = self.grid[y][x]
        correct_value = self.testgrid[y][x]

        if value != correct_value and value != 0:
            if current_value == 0:
                self.mistakes += 1  

        self.grid[y][x] = value

    def draw_mistakes(self, screen):
        """Draw the number of mistakes on the screen."""
        mistakes_text = f"Mistakes: {self.mistakes}"
        mistakes_surface = self.font.render(mistakes_text, True, (255, 0, 0))
        screen.blit(mistakes_surface, (630, 550)) 

    def check_grids(self):
        """Check if the current grid matches the solution grid."""
        return all(self.grid[y][x] == self.testgrid[y][x] for y in range(len(self.grid)) for x in range(len(self.grid[y])))

    def restart(self):
        """Restart the game with a new grid."""
        self.grid = create_grid(SUB_GRID_SIZE)
        self.testgrid = deepcopy(self.grid)
        self.remove()
        self.occupied = self.pre_occupied_cells()
        self.win = False
        self.selection.selnum = 0  
        self.start_time = pygame.time.get_ticks() 
        self.time_paused = False 
        self.recorded_time = 0  
        self.mistakes = 0  

    def is_cell_preoccupied(self, x, y):
        """Check if the cell is pre-occupied."""
        return (y, x) in self.occupied

    def pre_occupied_cells(self):
        """Return a list of pre-occupied cells."""
        return [(y, x) for y in range(len(self.grid)) for x in range(len(self.grid[y])) if self.get_cell(x, y) != 0]

    def draw_lines(self, pg, screen):
        """Draw grid lines on the screen."""
        for index, coordinates in enumerate(self.coordinates):
            color = (150, 100, 0) if index in [2, 5, 10, 13] else (0, 200, 255)
            width = 4 if index in [2, 5, 10, 13] else 1
            pg.draw.line(screen, color, coordinates[0], coordinates[1], width)

    def remove(self):
        """Remove a number of cells to create the puzzle."""
        num_of_cells = GRID_SIZE * GRID_SIZE
        empties = num_of_cells * 3 // 20
        for i in sample(range(num_of_cells), empties):
            self.grid[i // GRID_SIZE][i % GRID_SIZE] = 0

    def draw_numbers(self, screen):
        """Draw numbers on the grid."""
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                num = self.get_cell(x, y)
                if num != 0:
                    color = (0, 200, 255) if (y, x) in self.occupied else (0, 255, 0)
                    if num != self.testgrid[y][x]:
                        color = (255, 0, 0)
                    text_surface = self.font.render(str(num), False, color)
                    screen.blit(text_surface, (x * self.cell_size + self.x_offset, y * self.cell_size + self.y_offset))

    def show_select(self, py, screen):
        """Display the number selection panel."""
        self.selection.draw(screen)

    def get_cell(self, x, y):
        """Get the value of a cell."""
        return self.grid[y][x]

    def draw_timer(self, screen):
        """Draw the timer on the screen."""
        if not self.time_paused:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  
        else:
            elapsed_time = self.recorded_time  

        minutes = elapsed_time // 60
        seconds = elapsed_time % 60
        timer_text = f"Time: {minutes:02}:{seconds:02}"
        timer_surface = self.font.render(timer_text, True, (255, 255, 255))
        screen.blit(timer_surface, (630, 510)) 
    def draw_help(self, screen):
        """Draw help text on the screen."""
        help_text = [
            "Click on the grid cells to fill them.",
            "Use the number buttons to select numbers.",
            "Press SPACE to restart the game.",
            "Press H to toggle this help screen."
        ]
        y_offset = 50
        for line in help_text:
            help_surface = self.font.render(line, True, (255, 255, 255))
            screen.blit(help_surface, (650, y_offset))
            y_offset += 30 

    def toggle_help(self):
        """Toggle the help screen on and off."""
        self.show_help = not self.show_help
