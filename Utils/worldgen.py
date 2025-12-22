import random

#tiles and seed config!!

worldseed = 1337
 
WALL = "#"
FLOOR = '.'
WATER = '~'
DOOR = '|'

#RNG FUCTION

def _rng(x,y):
    """A deterministic Random Generator For A Coordinates Or Room Index."""
    return random.Random(worldseed + x * 9999 + y *8888)

#Room Generation:-

def generate_room(x0, y0, rw, rh, world):
    """Fills the Room With Symbols"""
    for y in range (y0, y0 + rh):
        for x in range(x0, x0 + rw):
            if y==y0 or y== y0+rh-1 or x==x0 or x==x0+rw-1:
                world[y][x] = WALL
            else:
                world[y][x] = FLOOR

#Connect Corridors

def connect_rooms(world, room1, room2):
    """Connects Two Room Centers With An L-Shaped Corridor"""

    x1, y1 = room1
    x2, y2 = room2
    for x in range(min(x1,x2), max(x1,x2)+1):
        world[y1][x] = FLOOR
    for y in range(min(y1,y2), max(y1,y2)+1):
        world[y][x2] = FLOOR

#World Generation

def generate_world(width, height, num_rooms=5):
    """Generates deterministic ASCII World"""
    """Also just for your knoledge the markups are done by AI"""

    #Intilize World With Walls

    world = [[WALL for _ in range(width)] for _ in range(height)]
    rooms = []

    #Generates Rooms
    for i in range(num_rooms):
        r = _rng(i, i)
        rw , rh = r.randint(3,6), r.randint(3,6)
        rx , ry = r.randint(1, width-rw-1), r.randint(1, height-rh-1)
        generate_room(rx,ry,rw,rh,world)
        #STORE IT CUZ WE NEED IT!!!
        rooms.append((rx+rw//2,ry+rh//2))

    #CONNECT 'EM
    for i in range(len(rooms)-1):
        connect_rooms(world,rooms[i],rooms[i+1])

    #WATTA CUZ WE WANT IT
    for y in range(height):
        for x in range(width):
            r = _rng(x, y)
            if world[y][x] == FLOOR and r.random() < 0.1:
                world[y][x] = WATER

    return world


#RENDER TO GET CLI OUTPUT!!!

def print_world(world):
    """PRINTS THE ASCII WORLD INTO THE CLI."""
    for row in world:
        print("".join(row))

#TEST CLI RUN

if __name__=="__main__":
    w = generate_world(30,15)
    print_world(w)