import random
import math


class Connect:
    def __init__(self):
        self.person = "⬤"
        self.ai = "◯"
        self.board = [
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
            [" ", " ", " ", " ", " ", " "],
        ]
        self.max_depth = 5

    def display(self):
        print((" ").join([" 0 ", " 1 ", " 2 ", " 3 ", " 4 ", " 5 "]))
        for x in self.board:
            print((" | ").join(x), end=" | \n")
        print()

    def is_valid(self, position):
        # for fill up on position                   for position putting
        if self.board[0][position] != " " or position <= -1 or position >= 6:
            return False

        return True

    def possible_moves(self):
        list = []
        for x in range(6):
            if self.board[0][x] == " ":
                list.append(x)
        return list

    def win_check(self, player):
        # Check horizontally
        for row in range(6):
            for col in range(3):
                if (
                    self.board[row][col] == player
                    and self.board[row][col + 1] == player
                    and self.board[row][col + 2] == player
                    and self.board[row][col + 3] == player
                ):
                    return True

        # Check vertically
        for row in range(3):
            for col in range(6):
                if (
                    self.board[row][col] == player
                    and self.board[row + 1][col] == player
                    and self.board[row + 2][col] == player
                    and self.board[row + 3][col] == player
                ):
                    return True

        # Check diagonally (positive slope)
        for row in range(3):
            for col in range(3):
                if (
                    self.board[row][col] == player
                    and self.board[row + 1][col + 1] == player
                    and self.board[row + 2][col + 2] == player
                    and self.board[row + 3][col + 3] == player
                ):
                    return True

        # Check diagonally (negative slope)
        for row in range(3, 6):
            for col in range(3):
                if (
                    self.board[row][col] == player
                    and self.board[row - 1][col + 1] == player
                    and self.board[row - 2][col + 2] == player
                    and self.board[row - 3][col + 3] == player
                ):
                    return True
        return False

    def undo_puck(self, position):
        for ypos in range(len(self.board)):
            if self.board[ypos][position] != " ":
                self.board[ypos][position] = " "
                break

    def place_puck(self, position, person):
        for ypos in reversed(range(len(self.board))):
            if self.board[ypos][position] == " ":
                self.board[ypos][position] = person
                break
            elif self.board[ypos][position] != " ":
                ypos -= 1

    def is_draw(self):
        # just checks for fill up on each x coord
        for x in self.board[0]:
            if x == " ":
                return False
        return True

    def minimax(self, maximizing, depth):
        if self.win_check(self.ai):
            return 100
        if self.win_check(self.person):
            return -100
        if self.is_draw() or depth == self.max_depth:
            return 0

        if maximizing:
            maxEval = -math.inf
            for move in self.possible_moves():
                # places a puck in that move
                self.place_puck(move, self.ai)
                # do a minimax which determines the score
                score = self.minimax(False, depth + 1)
                # undo itself
                self.undo_puck(move)

                maxEval = max(maxEval, score)

            return maxEval
        else:
            minEval = math.inf
            for move in self.possible_moves():
                # places a puck in that move
                self.place_puck(move, self.person)
                # do a minimax which determines the score
                score = self.minimax(True, depth + 1)
                # undo itself
                self.undo_puck(move)

                # DOES THE MIN
                minEval = min(minEval, score)

            return minEval

    def better_machine(self):
        bestScore = -math.inf
        bestMove = None

        # get all the possible moves
        for move in self.possible_moves():
            # places a puck in that move
            self.place_puck(move, self.ai)
            # do a minimax which determines the score
            score = self.minimax(False, 0)
            # undo itself
            self.undo_puck(move)

            if score > bestScore:
                bestScore = score
                bestMove = move
        self.place_puck(bestMove, self.ai)

    def player_move(self):
        while True:
            try:
                userInput = int(
                    input("Player : Which column do you want to put the ball in: ")
                )
                if self.is_valid(userInput):
                    return userInput

                else:
                    print("Invalid input")
            except Exception:
                print("Something went wrong")

    def machine(self):
        self.place_puck(random.randint(0, 5), self.ai)

    def play(self):
        while True:
            self.display()
            personInput = self.player_move()
            self.place_puck(personInput, self.person)

            if self.win_check(self.person) or self.is_draw():
                self.display()
                break

            self.better_machine()
            if self.win_check(self.ai) or self.is_draw():
                self.display()
                break
            print(self.possible_moves())

        self.display()
        if self.win_check(self.ai) or self.is_draw():
            print("you loose")
        else:
            print("print you win")


game = Connect()
game.play()
