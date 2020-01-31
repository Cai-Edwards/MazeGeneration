from random import choice, randint, random
import pygame, time

class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = self.make_maze()

    def make_maze(self):
        maze = []
        
        for y in range(self.size):
            maze.append([])

            for x in range(self.size):
                edges = 0b0000
                
                if y == 0: edges = edges | 0b1000
                if x == 0: edges = edges | 0b0001
                if y == self.size-1: edges = edges | 0b0010
                if x == self.size-1: edges = edges | 0b0100
                
                maze[y].append(Node(0b1111, edges, x, y))

        return maze                

class Node:
    def __init__(self, walls, edges, x, y):
        self.walls = walls
        self.edges = edges
        self.travelled = False
        self.x = x
        self.y = y


def available(current, maze, r):
        base = format(current.walls &~ current.edges, '04b')
        new = 0b0000

        if base[0] == "1" and (not maze.maze[current.y-1][current.x].travelled or random() < r):
            new = new | 0b1000
            
        if base[1] == "1" and (not maze.maze[current.y][current.x+1].travelled or random() < r):
            new = new | 0b0100
            
        if base[2] == "1" and (not maze.maze[current.y+1][current.x].travelled or random() < r):
            new = new | 0b0010
            
        if base[3] == "1" and (not maze.maze[current.y][current.x-1].travelled or random() < r):
            new = new | 0b0001

        return format(new, '04b')

def generate(maze, sx, sy, ex, ey, show, r):

    global display_width
    global ratio
    
    ratio = round(display_width/maze.size-0.5)
    nodes = [maze.maze[sy][sx]]

    while len(nodes) != 0:
        
        current_node = nodes[-1]
        current_node.travelled = True

        if current_node.x == ex and current_node.y == ey:
            path = [(z.x, z.y) for z in nodes]
            nodes = nodes[:-3]
            
            current_node = nodes[-1]
            current_node.travelled = True
            
        next_direction = available(current_node, maze, r)
        
        if next_direction == "0000":
            nodes.pop()
            
        else:
            direction = choice([x for x, i in enumerate(next_direction) if i == "1"])

            if direction == 0: #north
                current_node.walls = current_node.walls & 0b0111
                other = maze.maze[current_node.y-1][current_node.x]
                other.walls = other.walls & 0b1101

            elif direction == 1: #east
                current_node.walls = current_node.walls & 0b1011
                other = maze.maze[current_node.y][current_node.x+1]
                other.walls = other.walls & 0b1110

            elif direction == 2: #south
                current_node.walls = current_node.walls & 0b1101
                other = maze.maze[current_node.y+1][current_node.x]
                other.walls = other.walls & 0b0111

            else: #west
                current_node.walls = current_node.walls & 0b1110
                other = maze.maze[current_node.y][current_node.x-1]
                other.walls = other.walls & 0b1011

            nodes.append(other)

        if show == True:
            visualise_current(maze, current_node)

    visualise_end(maze, sx, sy, ex, ey, path)
    
    return maze

#Displays the ending state
def visualise_current(maze, current_node):
    global ratio

    d.fill(white)
    for row in maze.maze:
        for node in row:
            
            x = (ratio)*node.x
            y = (ratio)*node.y
            
            if node.walls & 0b1000 and node.y == 0:  #North
                pygame.draw.line(d, black, (x, y), (x + ratio, y), line_width)
                
            if node.walls & 0b0100:  #East
                pygame.draw.line(d, black, (x + ratio, y), (x + ratio, y + ratio), line_width)
                
            if node.walls & 0b0010:  #South
                pygame.draw.line(d, black, (x, y + ratio), (x + ratio, y + ratio), line_width)
                
            if node.walls & 0b0001 and node.x == 0:  #West
                pygame.draw.line(d, black, (x, y), (x, y + ratio), line_width)
                
            if current_node == node:
                pygame.draw.rect(d, red, (x, y, ratio, ratio))
                
    pygame.display.update()

def visualise_end(maze, sx, sy, ex, ey, path):
    global display_width
    global display_height
    show = False
    d = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)

    
    while True:
        display_width = min(d.get_width(), d.get_height())
        ratio = round(display_width/maze.size-0.5)
        
        d.fill(white)
        for row in maze.maze:
            for node in row:
                
                x = (ratio)*node.x
                y = (ratio)*node.y
                
                if node.walls & 0b1000 and node.y == 0:  #North
                    pygame.draw.line(d, black, (x, y), (x + ratio, y), line_width)
                    
                if node.walls & 0b0100:  #East
                    pygame.draw.line(d, black, (x + ratio, y), (x + ratio, y + ratio), line_width)
                    
                if node.walls & 0b0010:  #South
                    pygame.draw.line(d, black, (x, y + ratio), (x + ratio, y + ratio), line_width)
                    
                if node.walls & 0b0001 and node.x == 0:  #West
                    pygame.draw.line(d, black, (x, y), (x, y + ratio), line_width)

        pygame.draw.rect(d, green, (ratio*sx+line_width, ratio*sy+line_width, ratio - line_width, ratio - line_width))
        pygame.draw.rect(d, green, (ratio*ex+line_width, ratio*ey+line_width, ratio - line_width, ratio - line_width))

        if show:
            new_path = [(round((z[0] + 0.5) * ratio), round((z[1] + 0.5) * ratio)) for z in path]
            pygame.draw.lines(d, red, False, new_path, line_width)

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    
                if event.key == pygame.K_RETURN:
                    if show:
                        show = False
                    else:
                        show = True
                        
            if event.type == pygame.VIDEORESIZE:
                d = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
                
if __name__ == "__main__":

    s = 30 #Size of the maze
    r = 0.00 #Chance of ANY travelled node beyond being ignored. ie the chance for one node to "break through" a wall is ~4r
    k = True #Visualise the maze being made
    
    pygame.init()

    clock = pygame.time.Clock()

    white = (255, 255, 255)
    red = (255, 0, 0)
    green = (0, 255, 0)
    black = (0, 0, 0)

    line_width = 1

    display_width = 800
    display_height = 800

    d = pygame.display.set_mode((display_width, display_height), pygame.RESIZABLE)
    pygame.display.set_caption("Depth first maze generation")

    generate(Maze(s), 15, 15, randint(0, s-1), randint(0, s-1), k, r)

