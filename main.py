import random
import math

class Connect4:
    def __init__(self):
        self.person = "⬤"
        self.ai = "◯"
        self.board = [
            [" ", " ", " " ," ", " ", " "],
            [" ", " ", " " ," ", " ", " "],
            [" ", " ", " " ," ", " ", " "],
            [" ", " ", " " ," ", " ", " "],
            [" ", " ", " " ," ", " ", " "],
            [" ", " ", " " ," ", " ", " "]          
        ]
        # O(b^d) 
        self.max_depth = 8
        
    
    def display(self):
        print((" "). join([" 0 ", " 1 ", " 2 ", " 3 ", " 4 ", " 5 "]))
        for x in self.board:
            print((" | ").join(x), end=" | \n")
            

    def place_puck(self, xposition, person):
        for ypos in reversed(range(len(self.board))):
            if self.board[ypos][xposition] == " ":
                self.board[ypos][xposition] = person
                break
            elif self.board[ypos][xposition] != " ":
                ypos -= 1
    
    
    def win_check(self, player):
        #horizontal
        for row in range(6):
            for col in range(3):
                if (
                    self.board[row][col] == player
                    and self.board[row][col +1] == player
                    and self.board[row][col +2] == player
                    and self.board[row][col +3] == player
                ):
                    return True
        
        #vertical
        for row in range(3):
            for col in range(6):
                if (
                    self.board[row][col] == player
                    and self.board[row + 1][col ] == player
                    and self.board[row + 2][col ] == player
                    and self.board[row + 3][col ] == player
                ):
                    return True

        #diag / positive slope
        for row in range(3):
            for col in range(3):
                if (
                    self.board[row][col] == player
                    and self.board[row + 1][col +1] == player
                    and self.board[row + 2][col +2] == player
                    and self.board[row + 3][col +3] == player
                ):
                    return True
        
        #diag \ 
        for row in range(3,6):
            for col in range(3):
                if (
                    self.board[row][col] == player
                    and self.board[row - 1][col +1] == player
                    and self.board[row - 2][col +2] == player
                    and self.board[row - 3][col +3] == player
                ):
                    return True
        return False

    def is_draw(self):
        for x in self.board[0]:
            if x ==  " ":
                return False
        return True
    
    def undo_puck(self, userInput):
        for ypos in range(len(self.board)):
            if self.board[ypos][userInput] != " ":
                self.board[ypos][userInput]= " "
                break
        
    def dumb_machine(self):
        self.place_puck(random.randint(0,5), self.ai)

    def possible_moves(self):
        list = []
        for x in range(6):
            if self.board[0][x] == " ":
                list.append(x)
        return list
    
    def minimax(self, maximizing, depth, alpha, beta):
        if self.win_check(self.ai):
            return 100
        if self.win_check(self.person):
            return -100
        if self.is_draw() or depth == self.max_depth:
            return 0

        if maximizing:
            maxEval = -math.inf
            for move in self.possible_moves():
                self.place_puck(move, self.ai)
                score = self.minimax(False,depth+1,alpha, beta)
                self.undo_puck(move)
                maxEval = max(maxEval, score)
                
                
                alpha = max(maxEval, score)
                if beta <= alpha:
                    break
            return maxEval
        else:
            minEval = math.inf
            for move in self.possible_moves():
                self.place_puck(move, self.person)
                score = self.minimax(True,depth+1, alpha, beta)
                self.undo_puck(move)
                minEval = min(minEval, score)
                
                beta = min(beta, score)
                if beta <= alpha:
                     break
                 
            return minEval

    
    def smart_machine(self):
        bestscore = -math.inf
        bestmove = None
        
        
        for move in self.possible_moves():
            
            self.place_puck(move, self.ai)
            
            score = self.minimax(False,0, -math.inf, math.inf)
           
            self.undo_puck(move)
            
            if score > bestscore:
                bestscore = score
                bestmove = move
        self.place_puck(bestmove, self.ai)
        
    def is_valid(self,userInput):
        if self.board[0][userInput] != " " or  userInput <= -1 or userInput >= 6:
            return False
        return True
    
    def person_move(self):
        while True:
            try:
                userInput = int(input("Player: place puck: "))
                if self.is_valid(userInput):
                    return userInput
                else:
                    print("invalid input")
            except:
                print("something went wrong")

    
    def play(self):
        while True:
            self.display()
            personInput = self.person_move()
            self.place_puck(personInput , self.person)
            
            if self.win_check(self.person) or self.is_draw():
                self.display()
                break
            
            self.smart_machine()
            if self.win_check(self.ai) or self.is_draw():
                self.display()
                break
        
        if self.win_check(self.ai) or self.is_draw():
            print("you loose")
        else:
            print("print you win")
        
        
    
         
game = Connect4()

game.play()
