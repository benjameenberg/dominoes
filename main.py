from dominoes import Player, Board, Game
from strategies import Player_Input_Strategy, Block_If_Possible_Strategy, Bota_Gorda

def main():
    p1= Player("Ben")
    p2= Player("Kitty")
    p3= Player("Lucio")
    p4= Player("Harry")

    p1.assign_strategy(Block_If_Possible_Strategy())
    p3.assign_strategy(Block_If_Possible_Strategy())
    p4.assign_strategy(Bota_Gorda())

    g= Game([p1,p2,p3,p4])

    while True:
        
        try:
            g.next()
        except StopIteration:
            print("Game Over")
            break

if __name__ == '__main__':
    main()