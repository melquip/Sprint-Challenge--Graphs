from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from util import Stack, Queue
from collections import defaultdict
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# player.current_room.id
# player.current_room.get_exits()
# player.travel(direction)

# when moving to another room (going south for example)
# set previous room (south) to the id of current room
# set current room oposite direction (north) to id of previous room

def getCurrentRoomInfo(id, visited):
    currRoom = player.current_room.id
    if id == currRoom:
        exits = player.current_room.get_exits()
        room = visited[currRoom]
        room['id'] = currRoom
        room['exits'] = exits
        hasBeenFullyExplored = True
        for e in exits:
            if e not in visited[currRoom]:
                room[e] = '?'
        for e in exits:
            if visited[currRoom][e] == '?':
                hasBeenFullyExplored = False
                break
        room['explored'] = hasBeenFullyExplored
        return room
    else:
        raise ValueError(f"Player is in room #{currRoom} but you are trying to get room #{id}!")

def traverseMap():
    # 0: { 'n': '?', 's': '?', 'e': '?', 'w': '?' }
    visited = defaultdict(dict)
    lastRoom = None
    lastDirection = None
    oppositeDir = {
        'n': 's',
        's': 'n',
        'e': 'w',
        'w': 'e',
    }

    # dfs travel
    s = Stack()
    s.push([player.current_room.id])

    while s.size() > 0:
        path = s.pop()
        v_room = path[-1]
        currRoom = getCurrentRoomInfo(v_room, visited)
        vr_id = currRoom['id']
        vr_exits = currRoom['exits']
        print('\nroomInfo', v_room, currRoom)

        if not currRoom['explored']:
            if not visited[vr_id]:
                visited[vr_id] = dict()
                for e in vr_exits:
                    visited[vr_id][e] = '?'

            print('roomExits', vr_exits, 'visitedRoom', visited[vr_id])
            
            unexploredExit = [d for d in visited[vr_id] if visited[vr_id][d] == '?']
            print('unexploredExit', unexploredExit)
            if len(unexploredExit) > 0:
                # player travel in this direction
                randomExit = random.choice(unexploredExit)
                if player.travel(randomExit):
                    # set the new discovered room id on both rooms
                    playerRoom = player.current_room.id
                    visited[vr_id][randomExit] = playerRoom
                    visited[playerRoom][oppositeDir[randomExit]] = vr_id
                    traversal_path.append(randomExit)
                else:
                    # well poop
                    print(f'cant travel poop -> {randomExit} -> room #{vr_id}')

            else:
                # find shortest path to an unexplored room
                print('poop')
            #print(f'exit -> {e} -> {visited[vr_id][e]} -> {room_graph[vr_id][1][e]} -> {visited[vr_id][e] == room_graph[vr_id][1][e]}')
            
            new_path = list(path)
            new_path.append(player.current_room.id)
            s.push(new_path)


    
# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

traverseMap()

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



"""
# UNCOMMENT TO WALK AROUND
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
"""


"""
Start by writing an algorithm that picks a random unexplored direction from the player's current room, travels and logs that direction, then loops. This should cause your player to walk a depth-first traversal. When you reach a dead-end (i.e. a room with no unexplored paths), walk back to the nearest room that does contain an unexplored path.

You can find the path to the shortest unexplored room by using a breadth-first search for a room with a '?' for an exit. If you use the bfs code from the homework, you will need to make a few modifications.

Instead of searching for a target vertex, you are searching for an exit with a '?' as the value. If an exit has been explored, you can put it in your BFS queue like normal.

BFS will return the path as a list of room IDs. You will need to convert this to a list of n/s/e/w directions before you can add it to your traversal path.
"""