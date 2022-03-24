from tokenize import String
import re

from ..Exceptions import DenominationNotExistException
from ..Exceptions.SuitNotExist import SuitNotExistException

#possibles denominations 
denominations_that_exist = ["2","3","4","5","6","7","8","9","10","J","Q","K","A"]
#possibles suits
suits_that_exist = ["S","D","H","C"]

class Card:

    def __init__(self,card:String):
        """
            Args:
                card: is the string with denomination suit info. "5 D", "2 S".
            Returns:
                None 
        """
        card = re.findall(r'[A-Za-z0-9][0-9*]*',card)
        card = [value.upper() for value in card]

        if card[0].upper() == "T" :
            card[0] = "10"

        if(not card[0] in denominations_that_exist):
            raise DenominationNotExistException("this denomination "+card[0]+" not exist in poker game, all values that exist is "+str(denominations_that_exist))
        if(not card[1] in suits_that_exist):
            raise SuitNotExistException("this suit "+card[1]+" not exist in poker game, all values that exist is "+str(suits_that_exist))
       
        self.denomi = card[0]
        self.suit = card[1]
    
    def get_denomination(self)->String:
        """
            Returns:
                Denomination value from card
        
        """
        return self.denomi
    
    def get_suit(self)->String:
        """
            Returns:
                Suit value from card 
        """
        return self.suit