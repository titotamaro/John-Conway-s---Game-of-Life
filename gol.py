import sys
import pygame
import random
import time
from datetime import datetime

BOARD_SIZE = WIDTH, HEIGHT = 840,620
CELL_SIZE = 10
DEAD_COLOR = 0, 0, 0
ALIVE_COLOR = 0, 255, 255
MAX_FPS = 10

class LifeGame:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(BOARD_SIZE)
        self.clear_screen()
        pygame.display.flip()

        self.last_update_completed = 0
        self.desired_miliseconds_between_updates = (1.0 / MAX_FPS) * 1000.0
        
        self.active_grid = 0
        self.grids = []
        self.num_cols = int(WIDTH / CELL_SIZE)
        self.num_rows = int(HEIGHT / CELL_SIZE)
        self.init_grids()
        self.set_grid()

        self.paused = False
        self.game_over = False

    def init_grids(self):

        def create_grid():
            rows = []
            for row_num in range(self.num_rows):
                list_of_columns = [0] * self.num_cols
                rows.append(list_of_columns)
            return rows
 
        self.grids.append(create_grid())
        self.grids.append(create_grid())

    def clear_screen(self):
        self.screen.fill(DEAD_COLOR)

    def set_grid(self, value=None, grid=0):
        '''
        Examples:
        set_grid(0) #all dead
        set grid(1) #all alive
        set_grid() #random
        set_grid(None) #random 
        '''
        for r in range(self.num_rows):
            for c in range(self.num_cols):
                if value is None:
                    cell_value = random.randint(0,1)
                else:
                    cell_value = value
                self.grids[grid][r][c] = cell_value

    def draw_grid(self):
        # circle_rect = pygame.draw.circle(self.screen, ALIVE_COLOR, (50,50), 5, 0)
        self.clear_screen()
        for c in range(self.num_cols):
            for r in range(self.num_rows):
                if self.grids[self.active_grid][r][c] == 1:
                    color = ALIVE_COLOR
                else:
                    color = DEAD_COLOR
                pygame.draw.circle(self.screen, 
                color, 
                (int(c * CELL_SIZE + (CELL_SIZE/2)),
                int(r * CELL_SIZE + (CELL_SIZE/2))),
                int(CELL_SIZE/2),
                0)
        pygame.display.flip()

    def clear_screen(self):
        self.screen.fill(DEAD_COLOR)

    def get_cell(self,r,c):
        try:
            cell_value = self.grids[self.active_grid][r][c]
        except:
            cell_value = 0
        return cell_value

    def check_cell_neighbors(self, row_index, col_index):
        # Get the number of alive cells surrounding current cell
        # implement 4 rules, too populated, underpopulated, death, birth
        # self.grids[self.active_grid][r][c]
        num_alive_neighbors = 0
        
        num_alive_neighbors += self.get_cell(row_index - 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index)
        num_alive_neighbors += self.get_cell(row_index - 1, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index, col_index + 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index - 1)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index)
        num_alive_neighbors += self.get_cell(row_index + 1, col_index + 1)

        # rules for life and death
        if self.grids[self.active_grid][row_index][col_index] == 1:
            if num_alive_neighbors > 3 : # overpopulation
                return 0
            if num_alive_neighbors < 2: # underpopulation
                return 0
            if num_alive_neighbors == 2 or num_alive_neighbors == 3:
                return 1
        elif self.grids[self.active_grid][row_index][col_index] == 0:
            if num_alive_neighbors ==3:
                return 1

        return self.grids[self.active_grid][row_index][col_index]

    def update_generation(self):
        # inspect the current active generation
        # update the inactive grid to store net generation
        # swap out the active grid
        self.set_grid(0,self.inactive_grid())
        for r in range(self.num_rows - 1):
            for c in range(self.num_cols - 1):
                next_gen_state = self.check_cell_neighbors(r,c)
                self.grids[self.inactive_grid()][r][c] = next_gen_state     
        self.active_grid = self.inactive_grid()

    def inactive_grid(self):
        return (self.active_grid + 1) % 2

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.unicode =='s': # pause
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True
                elif event.unicode =='r': # random
                    self.active_grid = 0
                    self.set_grid(None, self.active_grid)
                    self.set_grid(0,self.inactive_grid())
                    self.draw_grid()
                elif event.unicode =='q': # random
                    self.game_over = True 
                
                        
            if event.type == pygame.QUIT:
                sys.exit()

    def run(self):
        while True:
            if self.game_over:
                return

            self.handle_events()

            if self.paused:
                continue

            self.update_generation() # time checking
            self.draw_grid()
            self.cap_frame_rate()

    def cap_frame_rate(self):
            now = pygame.time.get_ticks()
            miliseconds_since_last_updates = now - self.last_update_completed
            # print("Desired miliseconds between updates: %s " % desired_miliseconds_between_updates)
            time_to_sleep = self.desired_miliseconds_between_updates - miliseconds_since_last_updates
            # print("Time to sleep %s" % time_to_sleep)
            if time_to_sleep > 0:
                pygame.time.delay(int(time_to_sleep))
            self.last_update_completed = now

if __name__=='__main__':
    game = LifeGame()
    game.run()