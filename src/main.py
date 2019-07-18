import dominoes
from dominoes import Player, Board, Game

p1= Player("Ben")
p2= Player("Kitty")
p3= Player("Lucio")
p4= Player("Harry")

g= Game([p1,p2,p3,p4])

while g.next_round():
    g.play_round()