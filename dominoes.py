import random
from strategies import Play_First_Domino_Strategy


class Player:
    def __init__(self, name):
        self.name = name
        self.strategy = Play_First_Domino_Strategy()
        self.dominoes = []

    def assign_strategy(self, strategy):
        self.strategy = strategy

    def assign_dominoes(self, dominoes):
        self.dominoes = dominoes

    def __repr__(self):
        return "Player {}".format(self.name)

    def play(self, board):
        '''Play using the strategy, returning a message describing what was played'''
        # find the valid dominoes by calling available_plays
        # take a domino from self.dominoes and put it on the board
        valid_domino_plays = board.available_plays(self.dominoes)
        if not valid_domino_plays:
            return str(self) + " can't play"

        play = self.strategy.choose_play(self, board, valid_domino_plays)
        print(str(self) + " is about to play " + str(play[0]))
        board.putdown(*play)
        self.dominoes.remove(play[0])
        message = str(self) + " played " + str(play[0])
        return message


class Bad_Domino(Exception):
    pass


class Board:
    def __init__(self):
        self.board_dominoes = []

    def putdown(self, domino, put_at_end):
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
            self.board_dominoes.insert(0, domino)

    def available_plays(self, player_dominoes):
        if self.board_dominoes:
            beginning = self.board_dominoes[0][0]
            end = self.board_dominoes[-1][-1]
            beginning_plays = [(d, False)
                               for d in player_dominoes if beginning in d]
            if beginning != end:
                end_plays = [(d, True) for d in player_dominoes if end in d]
            # don't have to calculate end plays when both ends are the same
            else:
                end_plays = []
            x = beginning_plays + end_plays
        else:
            pos = True   # Play at end, doesn't matter since empty board
            x = [(d, pos) for d in player_dominoes]
        return x

    def is_blocked(self):
        # if there are no dominoes the board is not blocked
        if not self.board_dominoes:
            return False

        last_pip = self.board_dominoes[-1][-1]
        first_pip = self.board_dominoes[0][0]

        # number of dominoes played with first_pip
        first_pip_count = len(
            [d for d in self.board_dominoes if first_pip in d])
        # number of dominoes played with last_pip
        last_pip_count = len([d for d in self.board_dominoes if last_pip in d])
        return first_pip_count == 7 and last_pip_count == 7

    def will_block(self, available_plays):
        # makes each play in available plays and finds out if said play will block the board
        # stops as soon as a play to block is found
        # if none are found return None
        saved_board = list(self.board_dominoes)
        for p in available_plays:
            self.putdown(*p)
            if self.is_blocked():
                self.board_dominoes = list(saved_board)
                return p
            self.board_dominoes = list(saved_board)
        return None

    def __repr__(self):
        return str(self.board_dominoes)


class Game:
    def __init__(self, players):
        self.players = players
        assert len(self.players) == 4
        self.team_1 = [self.players[0], self.players[2]]
        self.team_2 = [self.players[1], self.players[3]]
        print("Team 1 is " + str([p.name for p in self.team_1]))
        print("Team 2 is " + str([p.name for p in self.team_2]))
        self.end_score = int(input("How many points do you want to play to? "))
        self.reset()

    def reset(self):
        # Some messages about what has happened
        self.round_msg = ''
        self.play_msg = ''
        self.team_1_score = 0
        self.team_2_score = 0
        self.board = None
        self.game_generator = None

    def pip_total(self, player_list):
        '''pip_total calculates the total of the dominoes in the given players'''
        total = sum(sum(sum([p.dominoes for p in player_list], []), ()))
        return total

    def score_round(self, last_player, is_blocked):
        # if someone goes out their team wins
        # else they team with the lowest pip total in their hands wins
        '''score round determines the winning team'''

        # game must be blocked, since last player didn't win
        last_player_won = not is_blocked

        team_1_total = self.pip_total(self.team_1)
        team_2_total = self.pip_total(self.team_2)
        points = team_1_total + team_2_total
        if (last_player_won and last_player in self.team_1) or (
                is_blocked and team_1_total < team_2_total):
            # team 1 won
            self.round_msg = "Team 1 won: {} points".format(points)
            self.team_1_score += points
        elif (last_player_won and last_player in self.team_2) or (
                is_blocked and team_2_total < team_1_total):
            # team 2 won
            self.round_msg = "Team 2 won: {} points".format(points)
            self.team_2_score += points
        else:
            # it is a tie
            self.round_msg = "Blocked game, Tie! {} == {}".format(
                team_1_total, team_2_total)

        if self.team_1_score >= self.end_score:
            # team 1 won the game
            self.game_msg = "Team 1 won the game {} to {}".format(
                self.team_1_score, self.team_2_score)
            self.game_over = True
        elif self.team_2_score >= self.end_score:
            # team 2 won the game
            self.game_msg = "Team 2 won the game {} to {}".format(
                self.team_2_score, self.team_1_score)
            self.game_over = True

        print("Team 1 has a score of {} and Team 2 has a score of {}".format(
            self.team_1_score, self.team_2_score))

    def new_round(self):
        self.round_over = False 
        self.round_msg = 'New round'
        self.board = Board()
        x = get_dominoes()
        self.players[0].assign_dominoes(x[0:7])
        self.players[1].assign_dominoes(x[7:14])
        self.players[2].assign_dominoes(x[14:21])
        self.players[3].assign_dominoes(x[21:28])

    def make_game_generator(self):
        self.play_msg = ''
        self.game_msg = ''
        self.game_over = False
        while not self.game_over:
            self.new_round()
            while not self.round_over:
                for p in self.players:
                    self.round_msg = ''
                    # Game stores message about what just was played
                    self.play_msg = p.play(self.board)
                    is_blocked = self.board.is_blocked()
                    if p.dominoes == [] or is_blocked:
                        print("Last player {} ({} dominoes) : Game is blocked: {}".format(
                            p.name, len(p.dominoes), self.board.is_blocked()))
                        self.round_over = True
                        # Set the round message, and self.game_over if it is...
                        self.score_round(p, is_blocked)
                    # This pauses until someone calls next()
                    yield
                    if self.round_over:
                        break
                if self.game_over:
                    break

    def next(self):
        if not self.game_generator:
            self.game_generator = self.make_game_generator()
        next(self.game_generator)



def get_dominoes():
    game_dominoes = []
    for i in range(7):
        for j in range(i, 7):
            game_dominoes.append((i, j))
    random.shuffle(game_dominoes)
    return game_dominoes
