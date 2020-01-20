from random import choice

class Maze:
    def __init__(self, size):
        self.size = size
        self.maze = [[Node(x, y) for x in range(size)] for y in range(size)]

class Node:
    def __init__(self, x, y):
        self.wall = True
        self.x = x
        self.y = y

    def next_point(self):
        self.wall = False
        
def adjacent(maze, current_pos):
    adj = []

    try:
        if current_pos[0] != 0 and maze.maze[current_pos[0]-1][current_pos[1]].wall:
            try:
                if maze.maze[current_pos[0]-2][current_pos[1]].wall and maze.maze[current_pos[0]-1][current_pos[1]-1].wall and maze.maze[current_pos[0]-1][current_pos[1]+1].wall:
                    adj.append((current_pos[0]-1, current_pos[1]))
            except:
                adj.append((current_pos[0]-1, current_pos[1]))         
    except:
        pass

    try:
        if current_pos[0] != maze.size-1 and maze.maze[current_pos[0]+1][current_pos[1]].wall:
            try:
                if maze.maze[current_pos[0]+2][current_pos[1]].wall and maze.maze[current_pos[0]+1][current_pos[1]-1].wall and maze.maze[current_pos[0]+1][current_pos[1]+1].wall:
                    adj.append((current_pos[0]+1, current_pos[1]))
            except:
                adj.append((current_pos[0]+1, current_pos[1]))
    except:
        pass

    try:
        if current_pos[1] != 0 and maze.maze[current_pos[0]][current_pos[1]-1].wall:
            try:
                if maze.maze[current_pos[0]][current_pos[1]-2].wall and maze.maze[current_pos[0]-1][current_pos[1]-1].wall and maze.maze[current_pos[0]+1][current_pos[1]-1].wall:
                    adj.append((current_pos[0], current_pos[1]-1))
            except:
                adj.append((current_pos[0], current_pos[1]-1))
    except:
        pass

    try:    
        if current_pos[1] != maze.size-1 and maze.maze[current_pos[0]][current_pos[1]+1].wall:
            try:
                if maze.maze[current_pos[0]][current_pos[1]+2].wall and maze.maze[current_pos[0]-1][current_pos[1]+1].wall and maze.maze[current_pos[0]+1][current_pos[1]+1].wall:
                    adj.append((current_pos[0], current_pos[1]+1))
            except:
                adj.append((current_pos[0], current_pos[1]+1))
    except:
        pass

    return adj

def depth_first(maze, sx, sy):

    maze.maze[sy][sx].next_point()

    nodes = [maze.maze[sy][sx]]
    
    while len(nodes) != 0:
        current_pos = (nodes[-1].y, nodes[-1].x)
        available = adjacent(maze, current_pos)
        visualise(maze)
        input()

        if len(available) == 0:
            nodes.pop()
        else:
            current_pos = choice(available)
            nodes.append(maze.maze[current_pos[0]][current_pos[1]])
            nodes[-1].next_point()


def visualise(maze):
    for i in maze.maze:
        string = ""
        for k in i:
            if k.wall:
                string += "O"
            else:
                string += "X"
        print(string)
        
