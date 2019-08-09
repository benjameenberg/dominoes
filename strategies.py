class Play_First_Domino_Strategy:
    def choose_play(self, player, board, available_plays):
        chosen_play = available_plays[0]
        return chosen_play


class Player_Input_Strategy:
    def choose_play(self, player, board, available_plays):
        print("What do you want to play? " + str(available_plays))
        while True:
            try:
                chosen_play = available_plays[int(input("Enter number "))]
                print(chosen_play)
                return chosen_play
            except Exception as e:
                print(e)


class Block_If_Possible_Strategy:
    '''If the player is able to block the board then return that play, otherwise use
    the backup strategy'''

    def __init__(self, backup_strategy=None):
        if backup_strategy:
            self.backup_strategy = backup_strategy
        else:
            self.backup_strategy = Play_First_Domino_Strategy()

    def choose_play(self, player, board, available_plays):
        chosen_play = board.will_block(available_plays)
        if not chosen_play:
            chosen_play = self.backup_strategy.choose_play(
                player, board, available_plays)
        return chosen_play

class Bota_Gorda:
     def choose_play(self, player, board, available_plays):
        sorted_plays = sorted(available_plays, key=pip_total, reverse=True)
        chosen_play = sorted_plays[0]
        return chosen_play

def pip_total(play):
    return sum(play.domino)