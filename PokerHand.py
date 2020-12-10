from collections import Counter

from Result import Result


class PokerHand(object):
    cards_values = {"2": 1,
                    "3": 2,
                    "4": 3,
                    "5": 4,
                    "6": 5,
                    "7": 6,
                    "8": 7,
                    "9": 8,
                    "T": 9,
                    "J": 10,
                    "Q": 11,
                    "K": 12,
                    "A": 13}
    suits_values = {"D": 1,
                    "S": 2,
                    "H": 3,
                    "C": 4}
    hands_values = {"HC": 0,
                    "OP": 1,
                    "TP": 2,
                    "TK": 3,
                    "ST": 4,
                    "FL": 5,
                    "FH": 6,
                    "FK": 7,
                    "SF": 8,
                    "RS": 9}

    def __init__(self, hand):
        if len(hand) != 14:
            raise Exception("Invalid hand!")
        self.hand = hand
        self.cards = []
        self.suits = []
        self.sorted_cards = []
        self.sorted_suits = []

    def compare_with(self, other_hand):
        hand_value, max_card_value = self.eval_hand()
        other_hand_value, other_hand_max_card_value = other_hand.eval_hand()

        if hand_value > other_hand_value:
            return Result.WIN
        elif hand_value < other_hand_value:
            return Result.LOSS
        else:
            if max_card_value > other_hand_max_card_value:
                return Result.WIN
            elif max_card_value < other_hand_max_card_value:
                return Result.LOSS
            else:
                return Result.WIN if sum(self.cards) > sum(other_hand.cards) else Result.LOSS

    def eval_hand(self):
        for i in range(0, len(self.hand), 3):
            self.cards.append(self.cards_values[self.hand[i]])
            self.suits.append(self.suits_values[self.hand[i + 1]])

        self.sorted_cards = sorted(self.cards)
        self.sorted_suits = sorted(self.suits)

        max_card_value = self.suits[0]
        if self.is_royal() and self._is_flush():  # Royal Straight flush
            hand_value = self.hands_values["RS"]
        elif self._is_straight() and self._is_flush():  # Straight flush
            hand_value = self.hands_values["SF"]
        elif self._is_flush():  # Flush
            hand_value = self.hands_values["FL"]
        elif self._is_straight():  # Flush
            hand_value = self.hands_values["ST"]
        else:
            hand_value, max_card_value = self._get_combination()
            hand_value = self.hands_values[hand_value]

        return hand_value, max_card_value

    def _is_flush(self):
        return True if self.sorted_suits[0] == self.sorted_suits[-1] else False

    def _is_straight(self):
        if self.sorted_cards[0] + 4 == self.sorted_cards[-1] or \
                (self.sorted_cards[0] == 13 and self.sorted_cards[-1] == 4):
            return True
        else:
            return False

    def is_royal(self):
        return True if self.sorted_cards[0] == 9 and self.sorted_cards[-1] == 13 else False

    def _get_combination(self):
        groups = Counter(self.cards)
        if len(groups) == 5:
            return "HC", next(iter(groups.keys()))  # Hight Card
        elif len(groups) == 4:
            return "OP", next(iter(groups.keys()))  # One Pair
        elif len(groups) == 3:
            if 3 in groups.values():
                return "TK", next(iter(groups.keys()))  # Three of a kind
            else:
                return "TP", next(iter(groups.keys()))  # 2 Pairs
        elif len(groups) == 2:
            if 4 in groups.values():
                return "FK", next(iter(groups.keys()))  # Four of a kind
            else:
                return "FH", next(iter(groups.keys()))  # Full House


if __name__ == "__main__":
    teste = PokerHand("9H 9S 8D 8C")

    teste1 = PokerHand("9H 9S 8D 8C TH")
    print(teste1.compare_with(PokerHand("9C 9H 5C 5H AC")))

    poker_hand_1 = PokerHand("KS 2H 5C JD TD")
    poker_hand_2 = PokerHand("9C 9H 5C 5H AC")
    print(poker_hand_1.compare_with(poker_hand_2))
