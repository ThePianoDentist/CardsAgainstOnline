import random
import tornado.gen
from CardsAgainstGame.card_data import CardParser
from CardsAgainstGame import CAHPlayer, Card

SUBMISSION_STATE = object()
JUDGING_STATE = object()


class CardHandler():
    def __init__(self):
        self.card_db = CardParser()
        self.black_deck = self.create_deck(card_type='Q')
        self.white_deck = self.create_deck(card_type='A')
        self.all_cards = {card.card_id: card for card in self.black_deck + self.white_deck}
        self.discarded_white_cards = []
        self.judged_cards = []

    def create_deck(self, card_type, expansions=None):
        """
        Initialises new white or black card deck for play
        :param card_type:  Indicates whether to return a white deck or black deck
        :return:
        """
        if not expansions:
            expansions = ["Base"]
        deck = []
        cards = self.card_db.return_cards()
        for card in cards:
            if card['expansion'] not in expansions:
                continue

            if card['cardType'] == card_type:
                card = Card(card_id=card['id'],
                            card_type=card['cardType'],
                            text=card['text'],
                            num_answers=card['numAnswers'],
                            expansion=card['expansion'])
                deck.append(card)
        random.shuffle(deck)
        return deck

    def draw_hand(self, player):
        """
        For the player specified, draw back up to 10 cards.
        :param player:
        :return:
        """
        cards_to_draw = (10 - player.hand_size)
        if len(self.white_deck) < cards_to_draw:
            self.shuffle_discards_into_white_deck()
        for _ in range(cards_to_draw):
            player.hand.add(self.white_deck.pop())
        assert player.hand_size == 10
        return

    def discard(self, card=None):
        """
        Appends a card being removed from a players hand to the discard pile
        :type card: Card
        :return:
        """
        self.discarded_white_cards.append(card)
        return

    def shuffle_discards_into_white_deck(self):
        self.white_deck.append(self.discarded_white_cards)
        random.shuffle(self.white_deck)
        return

    def get_card_by_id(self, card_id):
        return self.all_cards.get(card_id)


class Game():
    def __init__(self):
        self.pre_game = True
        self.quitting = False
        self.cards = CardHandler()
        self.discards = self.cards.discarded_white_cards
        self.players = []
        self.round = 0
        self.black_deck = self.cards.black_deck
        self.white_deck = self.cards.white_deck
        self.card_czar = None

        self.time_to_judge_cards = 60
        self.time_to_pick_cards = 60

        # Turn state handlers
        self.turn_state = None


    def add_player(self, player_name=None):
        player = CAHPlayer(name=player_name)
        self.cards.draw_hand(player)
        print('%s, has entered the game' % player.name)
        self.players.append(player)
        return

    def remove_player(self, player_name=None):
        quitter = self.get_player_by_name(player_name)
        for card in quitter.hand:
            self.cards.discard(card)
        quitter.awesome_points = 0
        quitter.hand = set()
        self.players.remove(quitter)
        return

    def get_player_by_name(self, player_name=None):
        """
        Return player from game's player list via player's name.
        :type players: CAHPlayer
        """
        return [player for player in self.players if player_name in player.name][0]

    def new_game(self):
        """
        Initialises a new game
        :return:
        """
        self.black_deck = self.cards.create_deck(card_type='Q')
        self.white_deck = self.cards.create_deck(card_type='A')
        for player in self.players:
            self.cards.draw_hand(player)
        return

    def clean_up(self):
        for player in self.players:
            player.hand = []
            player.awesome_points = 0
        return

    def get_czar(self):
        if self.card_czar is None:
            self.card_czar = random.choice(self.players)
        return self.card_czar

    @tornado.gen.coroutine
    def update(self):
        print("Update Called")
        if self.pre_game:
            print("PreGame Called")
            # Wait for Players
            if len(self.players) > 2:
                self.pre_game = False
                # Game Starts
                self.turn_state = SUBMISSION_STATE
                pass
            pass


        if self.turn_state == SUBMISSION_STATE:
            if not self.card_czar:
                self.card_czar = self.get_czar()

            pass
            # Do stuff before cards are revealed to czar
        elif self.turn_state == JUDGING_STATE:
            # do stuff after cards are being picked by czar
            pass

        if self.quitting:
            return
        yield




