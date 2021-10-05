
class Table:
    def __init__(self):
        self.card_in=[]
        self.card_out=[]

    def assept_card(self,c):
        self.card_in.append( c )

    def clear_table(self):
        self.card_in = []

    def get_cards(self):
        return self.card_in
