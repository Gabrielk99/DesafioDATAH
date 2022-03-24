from src.models.PokerHand import PokerHand
from src.models.PokerHand import RankingHands

def main():
    hand1 = PokerHand("10C 10H 5C 5H KH");
    hand2 = PokerHand("9C 9H 5C 5H AC")
    print(hand1.compare_with(hand2))

if __name__ == "__main__":
    main()