from calendar import c
from enum import Enum
from tokenize import String
from xmlrpc.client import boolean

from sympy import denom, true

from ..Exceptions.HandsNotExist import HandsNotExistException
from ..PokerHand import PokerHand
from collections import Counter

#unique possibility
royal_straight_flush=["A","K","Q","J","10"]

#values to special cards
other_values = {
    "A":14,
    "K":13,
    "Q":12,
    "J":11
}

def return_int_value(x:String):
    """
        With a string that represent the denomination
        returns the integer value representation

        Args:
            x: String, denomination of a card

        Returns:
            int value thats represent this denomination
    """
    if not x in other_values.keys() :
        return int(x)
    else:
        return other_values[x]

def its_highest_five(denominations:list[String]):
    """
        With a list of denominations values returns if
        is the highest five values
        Args:
            denominations: list[String], list of all the denominations in a hand
        Returns:
            True or False

    """
    denominations.sort()
    royal_straight_flush.sort()
    return denominations == royal_straight_flush

def its_sequence(denominations:list[String]):
    """
        With a list of denominations values returns if
        is a sequence of five values
        Args:
            denominations: list[String], list of all the denominations in a hand
        Returns:
            True or False

    """
    as_numbers_ = list(map(return_int_value,denominations))
    as_numbers_.sort()

    prev_deno = as_numbers_[0];
    list_of_dist_of_value_1 = []
    
    for i in as_numbers_[1:]:
        dist = i-prev_deno
        if(dist == 1):
            list_of_dist_of_value_1.append(dist)        
        prev_deno = i  

    if(len(list_of_dist_of_value_1)==4):
        return True
    #As usado como carta baixa
    elif as_numbers_ == [2,3,4,5,11]:
        return True
    else: 
        return False
    

class RankingHands(Enum):
    ROYAL_STRAIGHT_FLUSH=1
    STRAIGHT_FLUSH=2
    FOUR_OF_KIND=3
    FULL_HOUSE=4
    FLUSH=5
    STRAIGHT=6
    THREE_OF_KIND=7
    TWO_PAIR=8
    ONE_PAIR=9
    HIGH_CARD=10

    @staticmethod
    def get_rank(hand:PokerHand)->"RankingHands":
        """
            with a Hand return the rank 

            Args:
                hand: PokerHand, a hand from a player
            Returns:
                return the rank of hand player

        """
        denominations = hand.get_denominations()
        suits  = hand.get_suits()
        counter = Counter(suits)
        most_common_suit = counter.most_common()
        counter_denom = Counter(denominations)
        most_common_denom = counter_denom.most_common()
        
        if most_common_denom[0][1] == 5:
            raise HandsNotExistException("this hand: "+hand.toString()+" doesnt exist in poker game")

        elif most_common_suit[0][1] == 5:
            if(its_highest_five(denominations)):
                return RankingHands.ROYAL_STRAIGHT_FLUSH
            elif(its_sequence(denominations)):
                return RankingHands.STRAIGHT_FLUSH
            else:
                return RankingHands.FLUSH
        else:
            if most_common_denom[0][1] == 4:
                return RankingHands.FOUR_OF_KIND
            elif most_common_denom[0][1] == 3:
                if most_common_denom[1][1] == 2:
                    return RankingHands.FULL_HOUSE
                else:
                    return RankingHands.THREE_OF_KIND
            elif most_common_denom[0][1] == 2 and most_common_denom[1][1] ==2:
                return RankingHands.TWO_PAIR
            elif most_common_denom[0][1]==2 and most_common_denom[1][1] !=2:
                return RankingHands.ONE_PAIR
            else:
                if its_sequence(denominations):
                    return RankingHands.STRAIGHT
                else:
                    return RankingHands.HIGH_CARD

    @staticmethod
    def compare (hand_1:PokerHand,hand_2:PokerHand)->boolean:
        rank_1 = RankingHands.get_rank(hand_1)
        rank_2 = RankingHands.get_rank(hand_2)
        
        #lista dos valores para desempatar 
        #ordena de forma reversa
        denom_1 = [ return_int_value(x) for x in hand_1.get_denominations()]
        denom_1.sort(reverse=True)
        denom_2 = [ return_int_value(x) for x in hand_2.get_denominations()]
        denom_2.sort(reverse=True)
        
        # considerando a sequencia (2,3,4,5,A) A == 14
        # só uma condição de A == 1 a sequencia 2,3,4,5,14(A)
        if(denom_1 == [14,5,4,3,2]):
            denom_1 = [5,4,3,2,1]
        if(denom_2 == [14,5,4,3,2]):
            denom_2 = [5,4,3,2,1]

        # pega os valores mais comum, retorna uma lista ordenada de forma decrescente
        # tanto em valor quanto na contagem (a etapa de ordenar reversa faz ter os valores mais altos em ordem aqui)
        most_common_1 = [value[0] for value in Counter(denom_1).most_common()]
        most_common_2 = [value[0] for value in Counter(denom_2).most_common()]

        #mesmo rank desempate de valores
        if rank_1.value == rank_2.value:
            return most_common_1 > most_common_2
        else :
            #cartas ordenadas de maior rank com menor número de representação
            return rank_1.value < rank_2.value