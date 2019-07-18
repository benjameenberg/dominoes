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
        self.team_1 = [self.players[0] , self.players[2]]
        self.team_2 = [self.players[1] , self.players[3]]
        print ("Team 1 is " + str([p.name for p in self.team_1]))
        print ("Team 2 is " + str([p.name for p in self.team_2]))
        self.team_1_score = 0
        self.team_2_score = 0
        self.end_score = int(input("How many points do you want to play to? "))

    def pip_total (self, player_list):
        '''pip_total calculates the total of the dominoes in the given players'''
        total = sum(sum(sum([p.dominoes for p in player_list],[]),()))
        return total

    def score_round (self, last_player):
        #if someone goes out their team wins
        #else they team with the lowest pip total in their hands wins
        '''score round determines the winning team'''
        if last_player.dominoes:
            # game must be blocked, since last player had dominoes
            team_1_total = self.pip_total(self.team_1)
            team_2_total = self.pip_total(self.team_2)
            if team_1_total < team_2_total:
                #team 1 won
                self.team_1_score += team_1_total + team_2_total
            elif team_2_total < team_1_total:
                #team 2 won
                self.team_2_score += team_1_total + team_2_total
            else:
                #it is a tie
                pass
        else:
            #last player went out and won
            all_total = self.pip_total(self.players)
            if last_player in self.team_1:
                self.team_1_score += all_total
            else:
                self.team_2_score += all_total
        print ("Team 1 has a score of {} and Team 2 has a score of {}".format(
            self.team_1_score, self.team_2_score))

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
                    self.score_round(p)
                    break

    def next_round (self):
        #if neither team has reached the end score then play another round
        #else the team that reached the score wins
        another_round = True
        if self.team_1_score >= self.end_score:
            #team 1 won the game
            print("Team 1 won the game with {} points".format(self.team_1_score))
            another_round = False
        elif self.team_2_score >= self.end_score:
            #team 2 won the game
            print("Team 2 won the game with {} points".format(self.team_2_score))
            another_round = False
        return another_round

def get_dominoes():
    game_dominoes = []
    for i in range(7):
        for j in range (i,7):
            game_dominoes.append((i,j))
    random.shuffle(game_dominoes)
    return game_dominoes


