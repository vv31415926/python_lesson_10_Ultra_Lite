import time

#from cards import Cards
from gamer import Gamer
from koloda import Koloda
from table import Table


class GoGame:
    def __init__(self):
        args = ['Comp', 'Homo Sapiens']
        self.gamers = []   # игроки
        self.table = Table()  # Стол
        #self.cards = Cards()
        self.card_in = ''
        self.card_answer = ''
        self.koloda = Koloda()  # получить полную колоду карт
        self.trump = None
        self.trump_color=''
        self.trump_weight=100

        print('Вступили в игру:')
        for s in args:  # чтение игроков
            self.gamers.append(Gamer(s))
        for i, g in enumerate(self.gamers):  # вывод имен игроков
            print(g.get_name())

        self.my = 1
        self.comp = 0
        self.main_gamer = self.my
        self.slave_gamer = self.comp

        self.gamer_count = len(args)

    def win_gamer(self, ig, num=False):
        com1 = 'ходит'
        if ig == self.slave_gamer:
            com1 = 'отбивается'

        com2 = self.gamers[ig].get_count()
        print('Игрок: {}-{} карт ({})'.format(self.gamers[ig].name,com2, com1))

        lst = self.gamers[ig].get_cards() # все карты тек игрока
        s = '\u2502'
        ss = ' '
        i = 1
        for v in lst:
            s += self.card_ind(v)+'\u2502'
            ss += f' {i}  '
            i = i+1
        print(s, end='')
        if self.slave_gamer == ig:   # к кому ходят
            print(' '*10 + 'Стол:'+self.win_table()+'   колода:'+str(self.koloda.get_count() ),'    Козырь:'+self.trump[1]+self.trump[2]  )
        else:
            print()

        if self.gamers[ig].name != 'Comp':
            print(ss)

    def win_game(self):
        print('*'*60)
        self.win_gamer(self.comp)
        self.win_gamer(self.my, num=True)

    def win_table(self):
        lst = self.table.get_cards()
        s = ''
        i = 0
        for v in lst:
            if i == 0:
                s += '\u2502'
            s += self.card_ind(v)+'\u2502'
            if i == 1:
                s += '   '
                i = 0
            else:
                i += 1
        return s

    def card_ind(self, card ):  # [рейтинг, достоинство(название), код символа, масть ]
        s = card[1] + card[2]
        return s

    def is_end_game(self):
        if self.gamers[self.slave_gamer].get_count() <= 0:
            return True
        if self.gamers[self.main_gamer].get_count() <= 0:
            return True

    def assept_cards(self):
        for i in range(self.gamers[self.main_gamer].get_count(), 6):
            if self.koloda.get_count() > 0:
                self.gamers[self.main_gamer].assept_cards(self.koloda.card_out())
        for i in range(self.gamers[self.slave_gamer].get_count(), 6):
            if self.koloda.get_count() > 0:
                self.gamers[self.slave_gamer].assept_cards(self.koloda.card_out())

        if self.koloda.get_count() <= 0:
            print( '**************\nколода пуста')

    def is_err_key(self,n,ig):
        if n < 0 or n > self.gamers[ig].get_count():
            return True
        else:
            return False

    def start(self):

        # раздача карт игрокам
        for i in range(6):
            for i in range( len(self.gamers) ):
                self.gamers[i].assept_cards(  self.koloda.card_out()  )
        self.trump = self.koloda.card_out(trump=True)
        self.trump_color = self.trump[3]


        # Приведение к козырям
        for i in range( self.koloda.get_count() ):
            v = self.koloda.get_card(i)
            c = v[3]
            if c == self.trump_color:
                v[0] += self.trump_weight
                self.koloda.set_card(i,v)
            #print( self.koloda.get_card(i) )
        for i in range(len(self.gamers)):
            self.gamers[i].set_tramp( self.trump_color, self.trump_weight )


        self.main_gamer = self.my
        self.slave_gamer = self.comp
        game = True
        while game:
            self.win_game()  # стол игры

            if self.main_gamer == self.comp:  # ходит комп
                self.card_in = self.gamers[self.main_gamer].give_card( t=self.table.get_cards() , rej='brain')
                if self.is_end_game():
                    game = False
                    break
                if len( self.card_in) > 0:  # был выбор
                    self.table.assept_card(self.card_in)  # положить выбр карту на стол

                    self.win_game()  # стол игры

                    # ответ принимающего - чела
                    while True:
                        n = int(input('выбрать номер карты или 0 - "принять":'))
                        # Проверить ввод
                        if self.is_err_key( n, self.slave_gamer ):
                            print(  'Ошибка выбора карты!')
                        else:
                            if not self.gamers[self.slave_gamer].test_cards( self.card_in, n ):
                                print( '************************\nДжентельмены так не ходят! Повторите!')
                            else:
                                break
                    if n > 0:  # был выбор
                        self.card_answer = self.gamers[self.slave_gamer].give_card(i=n, rej='hand')  # отдал выбр карту
                        if self.is_end_game():
                            game = False
                            break
                        self.table.assept_card(self.card_answer)  # положить выбр карту на стол
                    else:   # отказ - пасс (чел принимает карты)
                        self.gamers[self.slave_gamer].assept_cards( *self.table.get_cards())
                        self.table.clear_table()
                        self.assept_cards()
                        print( '*******************\nПринял карты')
                else:  # пасс - отказ ходить - cмена ходящего
                    tmp = self.main_gamer
                    self.main_gamer = self.slave_gamer
                    self.slave_gamer = tmp
                    self.table.clear_table()

                    self.assept_cards()

            else:   # ходит чел - выбирает номер карты  -----------------------------------------------------
                while True:
                    n = int(input('выбрать номер карты или 0 - "бита"):'))
                    if self.is_err_key(n, self.main_gamer):
                        print('Ошибка выбора карты!')
                    else:
                        break

                if n > 0:  # был выбор
                    self.card_in = self.gamers[self.main_gamer].give_card(i=n, rej='hand')  # отдал выбранную карту
                    if self.is_end_game():
                        game = False
                        break
                    self.table.assept_card(self.card_in)  # положить выбр карту на стол

                    self.win_game()  # стол игры

                    time.sleep(1)   # думаем

                    # ответ принимающего - компа
                    self.card_answer = self.gamers[self.slave_gamer].give_card( i=self.card_in, rej='answer')
                    if self.is_end_game():
                        game = False
                        break
                    if len(self.card_answer) > 0:
                        self.table.assept_card(self.card_answer)  # положить выбр карту на стол
                    else:   # отказ - пасс (комп принимает карты)
                        self.gamers[self.slave_gamer].assept_cards( *self.table.get_cards())
                        self.table.clear_table()
                        self.assept_cards()
                        print('*******************\nПринял карты')
                else: # отказ - пасс
                    tmp = self.main_gamer
                    self.main_gamer = self.slave_gamer
                    self.slave_gamer = tmp
                    self.table.clear_table()

                    self.assept_cards()

            #time.sleep(1)  # думаем
        if self.gamers[self.slave_gamer].get_count() <= 0:
            print('Выиграл {}!!!'.format(self.gamers[self.slave_gamer].name))
        if self.gamers[self.main_gamer].get_count() <= 0:
            print('Выиграл {}!!!'.format(self.gamers[self.main_gamer].name))