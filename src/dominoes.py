import random

class Player:
    def __init__ (self,name):
        self.name = name
        self.dominoes = []

    def assign (self,dominoes):
        self.dominoes = dominoes

    def __repr__ (self):
        return (str(self.name)+" "+str(self.dominoes))
    
    def play (self, board):
    #find the valid dominoes by calling available_plays
    #take a domino from self.dominoes and put it on the board
        valid_dominoes = board.available_plays(self.dominoes)
        if not valid_dominoes:
            print (str(self) + " can't play")
            return
        print (str(self) + " is about to play " + str(valid_dominoes[0]))
        print (board)
        try:
            board.putdown(valid_dominoes[0],True)
        except Bad_Domino:
            board.putdown(valid_dominoes[0],False)
        self.dominoes.remove(valid_dominoes[0])
        print (str(self) + " played " + str(valid_dominoes[0]))

class Bad_Domino(Exception):
    pass

class Board:
    def __init__ (self):
        self.board_dominoes = []
    
    def putdown(self,domino,put_at_end):
        '''put down one dominop onto the board
        if put at end is true it will put it at the
        end of the board'''
        domino = list(domino)
        if self.board_dominoes == []:
            self.board_dominoes.append(domino)
        elif put_at_end:
            if self.board_dominoes[-1][-1] not in domino:
                raise Bad_Domino("Stupid")
            if domino[-1] == self.board_dominoes[-1][-1]:
                domino.reverse()
            self.board_dominoes.append(domino)
        else:
            if self.board_dominoes[0][0] not in domino:
                raise Bad_Domino("Dummy")
            if domino[0] == self.board_dominoes[0][0]:
                domino.reverse()
            self.board_dominoes.insert(0,domino)

    def available_plays (self,player_dominoes):
        if self.board_dominoes:
            valid= self.board_dominoes[0][0], self.board_dominoes[-1][-1]
        else:
            valid = range(7)
        x=[d for d in player_dominoes if d[0] in valid or d[1] in valid]
        return x
        
    def is_blocked (self):
        #if there are no dominoes the board is not blocked
        if not self.board_dominoes:
            return False
        
        last_pip = self.board_dominoes[-1][-1]
        first_pip = self.board_dominoes[0][0]

        # number of dominoes played with first_pip
        first_pip_count = len([d for d in self.board_dominoes if first_pip in d])
        # number of dominoes played with last_pip
        last_pip_count = len([d for d in self.board_dominoes if last_pip in d])
        return first_pip_count == 7 and last_pip_count == 7
        
    def __repr__ (self):
        return str(self.board_dominoes)
    
class Game:
    def __init__ (self, players):
        self.players = players
        assert len(self.players) == 4

    def score_round (self):
        pass

    def play_round (self):
        self.board= Board()
        x= get_dominoes()
        self.players[0].assign(x[0:7])
        self.players[1].assign(x[7:14])
        self.players[2].assign(x[14:21])
        self.players[3].assign(x[21:28])
        round_over = False
        while not round_over:   
            for p in self.players:
                p.play(self.board)
                if p.dominoes == [] or self.board.is_blocked():
                    print("Last player {} ({} dominoes) : Game is blocked: {}".format(
                        p.name, len(p.dominoes), self.board.is_blocked()))
                    round_over = True
                    break


def get_dominoes():
    game_dominoes = []
    for i in range(7):
        for j in range (i,7):
            game_dominoes.append((i,j))
    random.shuffle(game_dominoes)
    return game_dominoes


