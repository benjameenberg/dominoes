from dominoes import Player, Board, Game
from strategies import Player_Input_Strategy, Block_If_Possible_Strategy

p1= Player("Ben")
p2= Player("Kitty")
p3= Player("Lucio")
p4= Player("Harry")

p1.assign_strategy(Block_If_Possible_Strategy())
p3.assign_strategy(Block_If_Possible_Strategy())

g= Game([p1,p2,p3,p4])

while g.next_round():
    g.play_round()