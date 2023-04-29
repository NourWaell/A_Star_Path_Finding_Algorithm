import pygame
import math
from queue import PriorityQueue

# initialize constants and colors
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

# define Spot class representing individual cells on the grid
class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # get the row and column of the Spot object
    def get_pos(self):
        return self.row, self.col
    
    # check if Spot is marked as closed (already visited)
    def is_closed(self):
        return self.color == RED
    
    # check if Spot is marked as open (in the list of cells to be visited)
    def is_open(self):
        return self.color == GREEN

    # check if Spot is a barrier (cannot be traversed)
    def is_barrier(self):
        return self.color == BLACK

    # check if Spot is the starting point
    def is_start(self):
        return self.color == ORANGE

    # check if Spot is the end point
    def is_end(self):
        return self.color == TURQUOISE

    # reset the color of the Spot
    def reset(self):
        self.color = WHITE
        
    # mark the Spot as the starting point
    def make_start(self):
        self.color = ORANGE

    # mark the Spot as closed (visited)
    def make_closed(self):
        self.color = RED

    # mark the Spot as open (in the list of cells to be visited)
    def make_open(self):
        self.color = GREEN

    # mark the Spot as a barrier (cannot be traversed)
    def make_barrier(self):
        self.color = BLACK

    # mark the Spot as the ending point
    def make_end(self):
        self.color = TURQUOISE

    # mark the Spot as part of the path
    def make_path(self):
        self.color = PURPLE
    
    # draw the Spot on the window
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
    
    # update the list of neighbors for the Spot
    def update_neighbors(self, grid):
        self.neighbors = []
        # Check if the neighboring spot to the right is not a barrier, and if it is within the grid. If both conditions are met, append the neighbor to the list of neighbors for the current Spot.
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row + 1][self.col])
        # check neighbor to the left
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():
            self.neighbors.append(grid[self.row - 1][self.col])
        # check neighbor below
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col + 1])
        # check neighbor left
        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():
            self.neighbors.append(grid[self.row][self.col - 1])
    
# Define function for Spot class to be used by PriorityQueue
def __lt__(self, other):
    return False  # Not used, just need to define it to avoid errors

# Heuristic function: returns Manhattan distance between two points
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

# Reconstructs the path from start to end using the came_from dictionary
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]  # update current to its parent node
        current.make_path()  # mark current node as part of the path
        draw()  # draw the updated grid

# A* algorithm to find the shortest path from start to end on the grid
def algorithm(draw, grid, start, end):
    count = 0  # counter to break ties in PriorityQueue
    open_set = PriorityQueue()  # stores nodes to be explored
    open_set.put((0, count, start))  # put start node in open_set with priority 0
    came_from = {}  # stores the parent node of each explored node
    g_score = {spot: float("inf") for row in grid for spot in row }
    # initialize g_score for each node to infinity
    g_score[start] = 0  # set g_score of start node to 0
    f_score = {spot: float("inf") for row in grid for spot in row }
    # initialize f_score for each node to infinity
    f_score[start] = h(start.get_pos(), end.get_pos())  # set f_score of start node using heuristic
    
    open_set_hash = {start}  # set of nodes in the open_set for faster lookup
    
    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
        current = open_set.get()[2]  # get node with lowest f_score from open_set
        open_set_hash.remove(current)  # remove current node from open_set_hash
            
        if current == end:
            reconstruct_path(came_from, end, draw)  # reconstruct the path from start to end
            end.make_end()  # mark end node as the end point
            return True
            
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1  # g_score of neighbor via current node
                
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current  # update parent node of neighbor
                g_score[neighbor] = temp_g_score  # update g_score of neighbor
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())  # update f_score of neighbor
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))  # add neighbor to open_set
                    open_set_hash.add(neighbor)  # add neighbor to open_set_hash
                    neighbor.make_open()  # mark neighbor node as part of the frontier
                
        draw()  # draw the updated grid
            
        if current != start:
            current.make_closed()  # mark current node as explored
                
    return False  # return False if no path found

# Define function to create the grid of spots
def make_grid(rows, width):
    grid = []
    gap = width // rows
    # Iterate over each row and column of the grid
    for i in range(rows):
        # Create a new row
        grid.append([])
        for j in range(rows):
            # Create a new spot at this position
            spot = Spot(i, j, gap, rows)
            # Add the spot to the current row
            grid[i].append(spot)
    # Return the completed grid
    return grid

# Define function to draw the grid lines on the screen
def draw_grid(win, rows, width):
    gap = width // rows
    # Iterate over each row of the grid
    for i in range(rows):
        # Draw a horizontal line at this row
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        # Iterate over each column of the grid
        for j in range(rows):
            # Draw a vertical line at this column
            pygame.draw.line(win, GREY, (j * gap, 0), ( j * gap, width))

# Define function to draw the current state of the grid on the screen
def draw(win, grid, rows, width):
    # Fill the screen with white
    win.fill(WHITE)

    # Iterate over each spot in the grid and draw it
    for row in grid:
        for spot in row:
            spot.draw(win)

    # Draw the grid lines on top of the spots
    draw_grid(win, rows, width)
    # Update the display to show the changes
    pygame.display.update()

# Define function to get the row and column of the spot that was clicked by the user
def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    
    # Calculate the row and column of the spot that was clicked
    row = y // gap
    col = x // gap
    
    return row, col

# Define the main function that runs the program
def main(win, width):
    # Define the number of rows in the grid
    ROWS = 50
    # Create the initial grid
    grid = make_grid(ROWS, width)
    
    # Set the start and end spots to None
    start = None
    end = None
    
    # Set the program to run until the user quits
    run = True
    
    while run:
        # Draw the current state of the grid on the screen
        draw(win, grid, ROWS, width)
        # Iterate over each event in the event queue
        for event in pygame.event.get():
            # If the user clicks the close button, quit the program
            if event.type == pygame.QUIT:
                run = False
                
            # If the user clicks the left mouse button, set the start or end spot
            elif pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                spot = grid[row][col]
                # If the start spot hasn't been set yet and the clicked spot isn't the end spot, set the start spot
                if not start and spot != end:
                    start = spot
                    start.make_start()
                # If the end spot hasn't been set yet and the clicked spot isn't the start spot, set the end spot
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                    
                elif spot != end and spot != start:
                    spot.make_barrier()
                    
            elif pygame.mouse.get_pressed()[2]: # if the right mouse button is pressed
                pos = pygame.mouse.get_pos() # get the mouse position
                row, col = get_clicked_pos(pos, ROWS, width) # convert the mouse position to row and column in the grid
                spot = grid[row][col] # get the spot in the grid corresponding to the mouse position
                spot.reset() # reset the spot
                if spot == start: # if the spot is the starting node unselect the starting node
                    start = None 
                elif spot == end: # if the spot is the ending node unselect the ending node
                    end = None
                    
            # Handle keyboard events
            if event.type == pygame.KEYDOWN: # if a key is pressed
                if event.key == pygame.K_SPACE and start and end: # if the key is the space bar and both starting and ending nodes are selected
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid) # update the neighbors of all spots in the grid
                    
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end) # start algorithm
                    
                if event.key == pygame.K_c: # if the key is "c" reset game
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()
    
main(WIN, WIDTH)
