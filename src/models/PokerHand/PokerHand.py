from multiprocessing.dummy import Array
from typing import List
from sqlalchemy import String
from ..Card import Card
from ..Exceptions import ManyCardsException
from ..Result import Result
from ..RankingHands import RankingHands

class PokerHand:
    def __init__(self,cards:String):
       
        """
            Args:
                cards: Array[Card], its a five Cards to represent the Hand of player.
            Returns:
                None
        """
        hand_cards = [Card(card) for card in cards.split(" ")]
        if(len(hand_cards)>5 or len(hand_cards) < 5):
            raise ManyCardsException("A quantidade de cartas que um jogador deve ter é 5.")
        self.cards = hand_cards

    def get_cards (self)->List[Card]:
        """
            Returns:
                Five cards that represent player hand
        """
        return self.cards

    def get_denominations (self)->List[String]:
        """
            Returns:
                Five denominations from cards
        """
        cards = self.get_cards()
        denominations = [card.get_denomination() for card in cards]
        return denominations

    def get_suits (self)->List[String]:
        """
            Returns:
                Five suits from cards
        """
        cards = self.get_cards()
        suits  = [card.get_suit() for card in cards]
        return suits

    def toString(self)->String:

        cards = self.get_cards()
        return " ".join([card.get_denomination()+card.get_suit() for card in cards])

    def compare_with(self,second_hand:"PokerHand")->Result:
        if RankingHands.compare(self,second_hand):
            return Result.WIN
        else:
            return Result.LOSS
        
