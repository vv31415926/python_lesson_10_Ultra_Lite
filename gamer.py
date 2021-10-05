import random
# Игрок


class Gamer:
    def __init__(self, name):
        self.name = name
        self.cards = []   # карты игрока [рейтинг, достоинство(название), код символа, масть ]

    def get_name(self):
        '''
        :return: имя игрока
        '''

        return self.name

    def assept_cards(self, *args ):
        '''
        Принять карту/карты
        :param card: карты
        :return:
        '''
        if len(args) == 1:
            self.cards.append( args[0] )
        else:
            self.cards.extend( args )

    def del_card(self,i):
        del self.cards[i]

    def set_tramp(self, trump_color, trump_weight ):
        for i in range( len(self.cards) ):
            v = self.cards[i]
            c = v[3]
            if c == trump_color:
                v[0] += trump_weight
                self.cards[i] = v
            #print( self.cards[i] )

    def index_card(self,i):  # [рейтинг, достоинство(название), код символа, масть ]
        v = self.cards[i]
        s = v[1] + v[2]
        return s

    def get_index_cards(self):
        lst=[]
        for i in range( len(self.cards) ):
           lst.append( self.index_card(i) )
        return lst

    def get_cards(self):
        return self.cards

    def get_count(self):
        return len(self.cards)

    def move(self):
        pass

    def test_cards(self,in_card, n):

        if n == 0:
            return True
        out_card = self.cards[n - 1]
        res = False
        r_in = in_card[0]
        m_in = in_card[3]
        r_out = out_card[0]
        m_out = out_card[3]
        if r_in < r_out:
            if m_in == m_out or r_out > 100:
                res = True
        return res


    def give_card(self, t=None, i=None, rej = 'hand'):   # 1-hand, 2-answer, 3-brain
        res = []
        if rej == 'hand':
            res = self.cards[i-1]
            self.del_card(i-1)
        elif rej == 'answer':   # ответ картой  [рейтинг, достоинство(название), код символа, масть ] или пас[]
            r = i[0]
            m = i[3]
            for j,v in enumerate(self.cards):
                if v[3] == m or v[0] > 100:
                    if v[0] > r:
                        res = v
                        self.del_card(j)
                        break
        else:  # ход компа
            if len( t ) > 0:
                lst = []
                lst_t=[]
                for vt in t:
                    lst_t.append( vt[1] )
                for ind,v in enumerate(self.cards):
                    if v[1] in lst_t:
                        lst.append( (ind,v) )
                if len( lst ) > 0:
                    j = random.randint(0, len(lst)-1 )
                    res = lst[j][1]
                    self.del_card(lst[j][0])
            else:
                j = random.randint( 0, len(self.cards)-1 )
                res = self.cards[j]
                self.del_card(j)

        return res



