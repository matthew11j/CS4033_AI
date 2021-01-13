from PriorityQueue import PriorityQueue
from copy import deepcopy

class StateNode(object):

    state_id = 0
    parent_state_id = 0
    g = 0
    n = 0
    f = g + n
    moves = []
    depth = 0

    # StateNode object constructor
    def __init__(self, board, state_id, parent_state_id, parent, g, move):
        self.puzzle_board = board
        self.state_id = state_id
        self.parent_state_id = parent_state_id
        self.g = g
        self.priority = g
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
