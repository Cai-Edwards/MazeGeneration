from random import choice
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

    def available(self, maze): #REWORK TODO
        base = format(self.walls &~ self.edges, '04b')
        new = 0b0000

        if base[0] == 1 and not maze.maze[self.y+1][self.x].travelled:
            print("North fine")
            new = new | 0b1000
        if base[1] == 1 and not maze.maze[self.y][self.x+1].travelled:
            print("East fine")
            new = new | 0b0100
        if base[2] == 1 and not maze.maze[self.y-1][self.x].travelled:
            print("South fine")
            new = new | 0b0010
        if base[3] == 1 and not maze.maze[self.y][self.x-1].travelled:
            new = new | 0b0001

        return new


#This is broken, cai fix or i angery
def generate(maze, sx, sy):

    nodes = [maze.maze[sy][sx]]

    while len(nodes) != 0:
        
        current_node = nodes[-1]
        current_node.travelled = True

        try:
            direction = choice([x for x, k in enumerate(current_node.available(maze)) if k == '1'])

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

        except IndexError:
            nodes.pop()
        
        visualise(maze)
        input()

    return maze

def oldvisualise(maze):
    s = ""
    s+="+" + "--+"*maze.size

    for i in maze.maze:
        for k in i:
            if k.walls & 0b0001:
                s += "|"
            else:
                s + " "
            
            s+= "  "
        
        s += "\n|"
        for k in i:
            if k.walls & 0b0010:
                s += "--"
            else:
                s += "  "
            
            s += "+"
        s+="\n"

    print(s)

#new stuff
pygame.init()
clock = pygame.time.Clock()
white = (255, 255, 255)
black = (0, 0, 0)
display_width = 800
display_height = 800
window_gap = 100
maze_width = display_width - window_gap*2     #For square maze and square window
mazeDisp = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("aMazeing")
mazeDisp.fill(white)
pygame.display.update()

#Displays a current state of the maze and displays it
def visualise(maze):
    mazeDisp.fill(white)
    for row in maze.maze:
        for node in row:
            x = (maze_width/maze.size)*node.x + window_gap   #x and y position from top left corner of cell
            y = (maze_width/maze.size)*node.y + window_gap
            if node.walls & 0b1000:  #North
                pygame.draw.line(mazeDisp, black, [x,y], [x+maze_width/maze.size, y], 5)
            if node.walls & 0b0100:  #East
                pygame.draw.line(mazeDisp, black, [x+maze_width/maze.size,y], [x+maze_width/maze.size, y+maze_width/maze.size], 5)
            if node.walls & 0b0010:  #South
                pygame.draw.line(mazeDisp, black, [x,y+maze_width/maze.size], [x+maze_width/maze.size, y+maze_width/maze.size], 5)
            if node.walls & 0b0001:  #West
                pygame.draw.line(mazeDisp, black, [x,y], [x, y+maze_width/maze.size], 5)
    clock.tick(3)   #Controls speed of display
    pygame.display.update()

maze = Maze(6)
while True:
    visualise(maze)
    maze.maze[0][0].walls = 0b1011
    maze.maze[0][1].walls = 0b1110
    visualise(maze)
    maze.maze[0][0].walls = 0b1111
    maze.maze[0][1].walls = 0b1111
print("debugg")