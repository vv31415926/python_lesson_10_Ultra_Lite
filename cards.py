import random

class Cards:
    def __init__(self):
       self.cards = []    # [ [рейтинг, достоинство(название), код символа, масть ],... ]

    def get_cards(self):
        dic_card_suit = {'бубны':['\u2663','красный'],
                         'червы':['\u2666','красный'],
                         'трефы':['\u2661','черный'],
                         'пики':['\u2664','черный']}
        rating = {' 6':6,' 7':7,' 8':8,' 9':9,'10':10,' В':11,' Д':12,' К':13,' Т':14}    # имя : рейтинг

        self.cards = []   # обязательно
        for name,r in rating.items():   # название, рейтинг
            for k,v in dic_card_suit.items():  # масть: [код символа, цвет]
                self.cards.append( [r, name, v[0], k] )  # [[рейтинг, достоинство(название), код символа, масть ],...]

        random.shuffle(self.cards)

        return self.cards

    def ind(self, card ):  # [рейтинг, достоинство(название), код символа, масть ]
        s = card[1] + card[2]
        return s

    def __str__(self):
        s = ''
        for i in Cards.get_cards():   # рейтинг, название, []
            s +=  i[0]+', '+i[1][0]+' '+i[1][1]+'\n'
        return s

if __name__ == '__main__':
    c = Cards()
    z = c.get_cards()