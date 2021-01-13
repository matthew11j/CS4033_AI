import time
import sys
from copy import deepcopy

""" PriorityQueue structure
This will be used as the open_list for the breadth first search to hold StateNodes of possible moves
"""
class PriorityQueue(object):
    # PriorityQueue constructor
    def __init__(self):
        self.queue = []

    def length(self): # Gets length of queue
        return len(self.queue)

    def is_empty(self): # Checks to see if queue is empty
        return len(self.queue) == []

    def enqueue(self, data): # Enqueue data into queue
        self.queue.append(data)

    def get(self): # Dequeue data from queue based on priority
        try:
            min = 0
            for i in range(len(self.queue)):
                if self.queue[i].priority < self.queue[min].priority and self.queue[i].depth <= self.queue[min].depth:
                    min = i
            item = self.queue[min]
            del self.queue[min]
            return item
        except:
            pass

""" StateNode structure
This structure represents a "state" or possible move from the previous StateNode that the search methods will use
to look for goal_state
"""
class StateNode(object):

    state_id = 0
    parent_state_id = 0
    moves = []
    depth = 0

    # StateNode object constructor
    def __init__(self, board, state_id, parent_state_id, parent, g, move):
        self.puzzle_board = board
        self.state_id = state_id
        self.parent_state_id = parent_state_id
        self.g = g
        self.h = 0
        self.f = g + self.h
        self.priority = self.f
        self.move = move

        self.parent = parent
        if parent is None: # If new state has parent, copy the moves from the parent
            self.depth = 0
        else:
            self.depth = parent.depth + 1
            self.moves = deepcopy(parent.moves)
            self.moves.append(move)

    def display_stats(self): # Displays important information about the state
        print(f'\n======== State {str(self.state_id)} ========')
        print("State ID: " + str(self.state_id))
        print("Parent State ID: " + str(self.parent_state_id))
        print("Depth: " + str(self.depth))
        print("Cost: " + str(self.priority))
        print("Last Move: " + str(self.move))
        print("Moves: " + str(self.moves))

    def check_goal_state(self): # Used to check if state matches goal state
        return self.puzzle_board.check_board_complete()

    def get_possible_moves(self, closed_list): # Gets all possible moves from the current state
        possible_moves = PriorityQueue()
        state_id = self.state_id + 1
        for m in self.puzzle_board.move_options: # For each possible move (U,R,D,L), perform the move
            current_node = deepcopy(self)
            p = deepcopy(self.puzzle_board)
            tile_value = p.make_move(m)
            if p.zero is not self.puzzle_board.zero: # Determine the total cost after performing a move
                if 1 <= tile_value <= 6:
                    cost = current_node.priority + 1
                elif 7 <= tile_value <= 16:
                    cost = current_node.priority + 3
                elif tile_value == 17:
                    cost = current_node.priority + 15
                else:
                    print(':(')

                if p.board not in closed_list: 
                    # If the board array is not already in the closed list,
                    # Create a new state node with calculated priority and append to the list of possible moves,
                    new_state_node = StateNode(p, state_id, self.state_id, current_node, cost, m)
                    possible_moves.enqueue(new_state_node)
                    state_id += 1
                    del new_state_node

        return possible_moves

""" PuzzleBoard structure
This structure represents the tile board and includes methods used by search methods to find goal_state
"""
class PuzzleBoard(object):
    width = 3
    height = 6

    # PuzzleBoard constructor
    def __init__(self, start_state_array, goal_state_array):
        self.board = []
        self.zero = (0, 0)
        self.move_options = ["Up", "Right", "Down", "Left"]
        self.goal_state_board = []

        count = 0
        for i in range(self.height): # Populates board array based on start_state_array
            self.board.append([])
            self.goal_state_board.append([])
            for j in range(self.width):
                self.board[i].append(start_state_array[count])
                self.goal_state_board[i].append(goal_state_array[count])

                if start_state_array[count] == 0: # If the current value is '0', assign it as "zero"
                    self.zero = (i, j)
                count += 1

    def print_board(self): # Displays current board in console
        print('======== Current Board ========')
        for i in range(self.height):
            print(self.board[i])

    def check_board_complete(self): # Used to check if state matches goal state
        for i in range(self.height):
            for j in range(self.width):
                if self.board[i][j] != self.goal_state_board[i][j]:
                    return 0
        return 1

    def make_move(self, direction): # Wrapper to call 'tile move' functions based on directional input
        if direction == "Up":
            value = self.move_up()
        elif direction == "Right":
            value = self.move_right()
        elif direction == "Down":
            value = self.move_down()
        elif direction == "Left":
            value = self.move_left()
        return value

    def move_tile(self, new_spot, blank_spot): # Switches "zero" tile with the provided coordinates of directional move tile
        temp = self.board[new_spot[0]][new_spot[1]]
        self.board[new_spot[0]][new_spot[1]] = self.board[blank_spot[0]][blank_spot[1]]
        self.board[blank_spot[0]][blank_spot[1]] = temp
        return temp

    def move_up(self): # Moves "zero" UP, updates self.zero
        if self.zero[0] != 0:
            value = self.move_tile((self.zero[0] - 1, self.zero[1]), self.zero)
            self.zero = (self.zero[0] - 1, self.zero[1])
            return value
        else:
            return None

    def move_right(self): # Moves "zero" RIGHT, updates self.zero
        if self.zero[1] != self.width - 1:
            value = self.move_tile((self.zero[0], self.zero[1] + 1), self.zero)
            self.zero = (self.zero[0], self.zero[1] + 1)
            return value
        else:
            return None

    def move_down(self): # Moves "zero" DOWN, updates self.zero
        if self.zero[0] != self.height - 1:
            value = self.move_tile((self.zero[0] + 1, self.zero[1]), self.zero)
            self.zero = (self.zero[0] + 1, self.zero[1])
            return value
        else:
            return None

    def move_left(self): # Moves "zero" LEFT, updates self.zero
        if self.zero[1] != 0:
            value = self.move_tile((self.zero[0], self.zero[1] - 1), self.zero)
            self.zero = (self.zero[0], self.zero[1] - 1)
            return value
        else:
            return None

""" Search structure
This structure helps improve readability and maintainability, since there are multiple search methods being used (bfs, astar)
"""
class Search(object):
    # Maximum amount of time in seconds that algorithm will search for goal state
    max_search_time = 60

    # Search object inits with start state provided from PuzzleBoard object
    def __init__(self, board):
        self.start_state = StateNode(board, 1, None, None, 0, " ")
        self.nodes_generated = 0

    def f(self, state):
        state.f = self.h(state) + state.g
        state.priority = state.f
        return state.f

    def h(self, state):
        temp = 0
        for i in range(state.puzzle_board.height):
            for j in range(state.puzzle_board.width):
                if state.puzzle_board.board[i][j] != state.puzzle_board.goal_state_board[i][j] and state.puzzle_board.board[i][j] != '0':
                    temp += 1
        state.h = temp
        return state.h

    # Performs BFS on start_state
    def breadth_first_search(self):
        # Instantiate open/closed lists as well populate open list with start_state
        start = time.time()
        closed_list = list()
        priority_queue = PriorityQueue()

        priority_queue.enqueue(self.start_state)
        cur_time = time.time()
        while cur_time-start < self.max_search_time: # Algorithm will keep searching until time elapsed exceeds max_search_time
            if priority_queue.is_empty(): # If the open list is empty, end the search
                return None

            # Get next highest priority item from queue
            state = priority_queue.get()
            state.display_stats()

            if state.check_goal_state(): # If the current state matches the goal state, end the search
                # Print out important details of the search
                end = time.time()
                print("\n\n\n")
                print('\n======== Goal State Found! ========')
                print("Open List Size: ", priority_queue.length())
                print("Closed List Size: ", len(closed_list))
                print("Elapsed Time (sec): ", end-start)
                print("Number of moves: ", len(state.moves))
                print("Path:")
                state.display_stats()

                parent_state = state.parent
                while parent_state:
                    parent_state.display_stats()
                    parent_state = parent_state.parent
                return 0
                
            elif state.puzzle_board.board not in closed_list:
                # If the board array is not already in the closed list,
                # Append the current board to the closed list,
                # Get all possible moves from the current state
                closed_list.append(state.puzzle_board.board)
                possible_moves = state.get_possible_moves(closed_list)
                for x in range(possible_moves.length()):
                    # For all possible moves, enqueue the move into the open list
                    self.nodes_generated = self.nodes_generated + 1
                    priority_queue.enqueue(possible_moves.get())

            cur_time = time.time()
        
        # When the search ends, check to see if it was from elapsed time OR from open list being emptied
        if cur_time-start >= self.max_search_time:
            print('================')
            print('Search process suspended! Time elapsed is greater than ', self.max_search_time)
            print('================')
        else:
            print('Open list emptied! Goal state could not be found')

    def astar(self):
        start = time.time()
        closed_list = list()
        priority_queue = PriorityQueue()

        priority_queue.enqueue(self.start_state)
        cur_time = time.time()
        while cur_time-start < self.max_search_time: # Algorithm will keep searching until time elapsed exceeds max_search_time
            if priority_queue.is_empty(): # If the open list is empty, end the search
                return None
            # Get next highest priority item from queue
            state = priority_queue.get()
            state.display_stats()

            if state.check_goal_state():
                # Print out important details of the search
                end = time.time()
                print("\n\n\n")
                print('\n======== Goal State Found! ========')
                print("Open List Size: ", priority_queue.length())
                print("Closed List Size: ", len(closed_list))
                print("Elapsed Time (sec): ", end-start)
                print("Number of moves: ", len(state.moves))
                print("Path:")
                state.display_stats()

                parent_state = state.parent
                while parent_state:
                    parent_state.display_stats()
                    parent_state = parent_state.parent
                return 0
            elif state.puzzle_board.board not in closed_list:
                # If the board array is not already in the closed list,
                # Append the current board to the closed list,
                # Get all possible moves from the current state
                closed_list.append(state.puzzle_board.board)
                possible_moves = state.get_possible_moves(closed_list)
                for x in range(possible_moves.length()):
                    # For all possible moves, enqueue the move into the open list
                    possible_move = possible_moves.get()
                    self.nodes_generated = self.nodes_generated + 1
                    self.f(possible_move)
                    priority_queue.enqueue(possible_move)

            cur_time = time.time()

        # When the search ends, check to see if it was from elapsed time OR from open list being emptied
        if cur_time-start >= self.max_search_time:
            print('================')
            print('Search process suspended! Time elapsed is greater than ', self.max_search_time)
            print('================')
        else:
            print('Open list emptied! Goal state could not be found')


# Used to parse input state vectors into arrays of tiles
def parse_input(input_string):
    parsed_vector = []

    str_array = input_string.split(' ')
    for x in str_array:
        if x != ' ':
            try:  
                parsed_vector.append(int(x))
            except:
                pass

    if len(parsed_vector) is not 18:
        print(f'Input string "{input_string}" must be 18 integers. It is {str(len(parsed_vector))} integers\n')
        quit()
    return parsed_vector


# Used to validate script arguments
def validate_inputs():
    available_search_types = ['bfs', 'astar']
    
    if len(sys.argv) > 3:
        search_type,start_state_input,goal_state_input = [sys.argv[i] for i in range(1,len(sys.argv))]  
        use_case = "1"
    elif len(sys.argv) > 2:
        search_type,use_case = [sys.argv[i] for i in range(1,len(sys.argv))]
        start_state_input = ""
        goal_state_input = ""
    elif len(sys.argv) == 2:
        search_type = sys.argv[1]
        use_case = "1"
        start_state_input = ""
        goal_state_input = ""
    else:
        search_type = "bfs"
        use_case = "1"
        start_state_input = ""
        goal_state_input = ""

    if search_type and search_type not in available_search_types:
        print('<search_type> cannot be: ', search_type)
        quit()
    if use_case and use_case != "1" and use_case != "2":
        print('<use_case> cannot be: ', use_case)
        quit()

    return search_type,use_case,start_state_input,goal_state_input

if __name__ == "__main__": 
    if len(sys.argv) > 4: # Only allow 0-3 additional parameters from user
        print(f'Script cannot be run with {str(len(sys.argv) - 1)} parameters. There must be 0-3\n')
        quit()

    # Start/Goal state input vector - use case c)i)
    start_state_input = '1 13 3 5 6 9 11 0 8 12 14 10 7 16 15 4 17 2'
    goal_state_input = '1 13 3 5 6 9 11 14 8 12 16 10 7 17 15 0 4 2'

    search_type,use_case,start_state_input,goal_state_input = validate_inputs()
    if search_type and use_case and start_state_input and goal_state_input: # User inputs provided
        start_state_input = start_state_input
        goal_state_input = goal_state_input
    elif search_type and use_case and use_case == "2":
        # Start/Goal state input vector - use case c)ii)
        start_state_input = '1 13 3 5 17 9 11 0 8 12 14 10 7 16 15 4 6 2'
        goal_state_input = '5 1 3 13 17 9 11 0 8 12 14 10 7 16 15 4 6 2'
    else: # Default
        # Start/Goal state input vector - use case c)i)
        search_type = 'bfs'

    # Get parsed input arrays from input vectors
    start_state_array = parse_input(start_state_input)
    goal_state_array = parse_input(goal_state_input)

    # Create board object using start/goal states
    board = PuzzleBoard(start_state_array, goal_state_array)
    
    # Creates search object with the created board as the input
    search = Search(board)

    if search_type == 'bfs':
        # Breadth First Search performed
        search.breadth_first_search()
    elif search_type == 'astar':
        # A* Search performed
        search.astar()
    else: # Default
        search.breadth_first_search()
