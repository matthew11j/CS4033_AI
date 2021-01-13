from copy import deepcopy

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
