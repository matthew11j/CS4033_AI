import time
from PriorityQueue import PriorityQueue
from StateNode import StateNode

# Search structure 
class Search(object):
    # Maximum amount of time in seconds that algorithm will search for goal state
    max_search_time = 60

    # Search object inits with start state provided from PuzzleBoard object
    def __init__(self, board):
        self.start_state = StateNode(board, 1, None, None, 0, " ")
        self.number_of_steps = 0
        self.nodes_generated = 0

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
                print("Number of steps: ", self.number_of_steps)
                print("Open List Size: ", priority_queue.length())
                print("Closed List Size: ", len(closed_list))
                print("Elapsed Time (sec): ", end-start)
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

            self.number_of_steps = self.number_of_steps + 1
            cur_time = time.time()
        
        # When the search ends, check to see if it was from elapsed time OR from open list being emptied
        if cur_time-start >= self.max_search_time:
            print('================')
            print('Search process suspended! Time elapsed is greater than ', self.max_search_time)
            print('================')
        else:
            print('Open list emptied! Goal state could not be found')

    # TODO
    def astar():
        return None
