'''
What you need to do is i guess account for strategies that
are 100% because if it's 100% you'll never actuall reach a part of the game tree
in which case those parts shouldn't be updated
'''

import random
class Kuhn:
    def __init__(self,epochs=1000):
        self.epochs = epochs
        self.fta = [[.5 for i in range(4)] for i in range(3)]
        self.sta = [[.5 for i in range(4)] for i in range(3)]
        self.cards = list(range(3))

        self.sta_sum = [[0 for i in range(4)]for i in range(3)]
        self.fta_sum = [[0 for i in range(4)]for i in range(3)]

        self.fta_regs = [[0 for i in range(4)]for i in range(3)]
        self.sta_regs = [[0 for i in range(4)]for i in range(3)]
        self.p1_winnings = 0
        self.p2_winnings = 0

    def get_final_strat(self):
        for i in range(len(self.fta)):
            for x in range(len(self.fta[i])):
                self.fta[i][x] = self.fta_sum[i][x] / self.epochs
                self.sta[i][x] = self.sta_sum[i][x] / self.epochs

    def train(self):
        for _ in range(self.epochs):
            for card in self.cards:
                self.cfrm(card)
            self.update()
            self.fta_regs = [[0 for i in range(4)]for i in range(3)]
            self.sta_regs = [[0 for i in range(4)]for i in range(3)]
        self.get_final_strat()
        self.printresults()
        self.run_sim(self.epochs)

    def run_sim(self, num_games):
        import random
        def bet_to(card1,card2):
            action = 3 if random.random() > self.sta[card2][2] else 2
            if action == 2:
                self.p1_winnings += 1
                self.p2_winnings -= 1
            else:
                if card1 > card2:
                    self.p1_winnings += 2
                    self.p2_winnings -= 2
                else:
                    self.p2_winnings += 2
                    self.p2_winnings -= 2


        def checked_to(card1,card2):
            action = 1 if random.random() > self.sta[card2][0] else 0
            if action == 0:
                if card1 > card2:
                    self.p1_winnings += 1
                    self.p2_winnings -= 1
                else:
                    self.p2_winnings +=1
                    self.p1_winnings -= 1
            else:
                action = 3 if random.random() > self.fta[card1][2] else 2
                if action == 2:
                    self.p2_winnings +=1
                    self.p1_winnings -= 1
                else:
                    if card1 > card2:
                        self.p1_winnings += 2
                        self.p2_winnings -= 2
                    else:
                        self.p2_winnings += 2
                        self.p1_winnings -= 2

        for _ in range(num_games):
            card1,card2 = random.sample(self.cards, 2)
            bet_to(card1,card2) if random.random() > self.fta[card1][0] else checked_to(card1,card2)
        print("*"*50)
        print(f"Player 1's win rate is: {self.p1_winnings/self.epochs}")
        print(f"Player 2's win rate is: {self.p2_winnings/self.epochs}")

    def update(self):
        for it in range(3):
            fta_sum1 = sum(self.fta_regs[it][:2])
            fta_sum2 = sum(self.fta_regs[it][2:])
            sta_sum1 = sum(self.sta_regs[it][:2])
            sta_sum2 = sum(self.sta_regs[it][2:])
            if fta_sum1 == 0:
                self.fta[it][0] = .5
                self.fta[it][1] = .5
                self.fta_sum[it][0] += .5
                self.fta_sum[it][1] += .5
            else:
                self.fta[it][0] = self.fta_regs[it][0] / fta_sum1
                self.fta[it][1] = self.fta_regs[it][1]/fta_sum1
                self.fta_sum[it][0] += self.fta[it][0]
                self.fta_sum[it][1] += self.fta[it][1]

            if fta_sum2 == 0:
                self.fta[it][2] = .5
                self.fta[it][3] = .5
                self.fta_sum[it][2] += .5
                self.fta_sum[it][3] += .5

            else:
                self.fta[it][2] = self.fta_regs[it][2] / fta_sum2
                self.fta[it][3] = self.fta_regs[it][3]/fta_sum2
                self.fta_sum[it][2] += self.fta[it][2]
                self.fta_sum[it][3] += self.fta[it][3]

            if sta_sum1 == 0:
                self.sta[it][0] = .5
                self.sta[it][1] = .5
                self.sta_sum[it][0] += .5
                self.sta_sum[it][1] += .5
            else:
                self.sta[it][0] = self.sta_regs[it][0] / sta_sum1
                self.sta[it][1] = self.sta_regs[it][1]/sta_sum1
                self.sta_sum[it][0] += self.sta[it][0]
                self.sta_sum[it][1] += self.sta[it][1]

            if sta_sum2 == 0:
                self.sta[it][2] = .5
                self.sta[it][3] = .5
                self.sta_sum[it][2] += .5
                self.sta_sum[it][3] += .5

            else:
                self.sta[it][2] = self.sta_regs[it][2] / sta_sum2
                self.sta[it][3] = self.sta_regs[it][3]/sta_sum2
                self.sta_sum[it][2] += self.sta[it][2]
                self.sta_sum[it][3] += self.sta[it][3]

    def printresults(self):
        card_dic = {0:"Jack",1:"Queen",2:"King"}
        strat_dic = {0:"Check",1:"Bet",2:"Fold When bet to", 3: "Call when bet to"}

        print("-" * 50)
        for i in range(3):
            print(f"STRATEGY FOR THE FIRST PLAYER TO ACT WITH {card_dic[i]}")
            print("-" * 50)
            temp = self.fta[i]
            for x in range(4):
                print(f"{strat_dic[x]} at {temp[x] * 100:.2f}%")
                print("-" * 50)

        print("-" * 50)
        for i in range(3):
            print(f"STRATEGY FOR THE SECOND PLAYER TO ACT WITH {card_dic[i]}")
            print("-" * 50)
            temp = self.sta[i]
            for x in range(4):
                print(f"{strat_dic[x]} at {temp[x] * 100:.2f}%")
                print("-" * 50)



    #Think all you need to do is add something that when a percentgae is 0
    #just make a very small value representing wins or losses insignificant
    #but greater or less than zero by a hair just so you don't get that problem
    #with having a zero and then having to select a uniform distribution
    #either that or prune all impossibly bad decisions form the tree with an if statment
    def cfrm(self,card):
        #regrets for fta and sta
        myfta = self.fta[card]
        mysta = self.sta[card]
        mycards = [i for i in self.cards if i != card]
        for i in mycards:
            tempsta = self.sta[i]
            tempfta = self.fta[i]
            fta_cc = myfta[0] * tempsta[0] if card > i else -1 * myfta[0] * tempsta[0]
            fta_cbc = myfta[0] * tempsta[1] * myfta[3] * 2 if card > i else -2 * myfta[0] * tempsta[1] * myfta[3]
            fta_cbf = -1 *  myfta[0] * tempsta[1] * myfta[2]
            fta_bc = 2 * myfta[1] * tempsta[3] if card > i else -2 * myfta[1] * tempsta[3]
            fta_bf =  myfta[1] * tempsta[2]
            fta_ev_check = fta_cc + fta_cbc + fta_cbf
            fta_ev_bet = fta_bc + fta_bf

            fta_temp1 = -1 * myfta[2]
            fta_temp2 = 2 * myfta[3] if card > i else -2 * myfta[3]

            self.fta_regs[card][0] += fta_ev_check - fta_ev_bet
            self.fta_regs[card][1] += fta_ev_bet - fta_ev_check
            self.fta_regs[card][2] += fta_cbf - fta_cbc
            self.fta_regs[card][3] += fta_cbc - fta_cbf
            #self.fta_regs[card][2] += fta_temp1 - fta_temp2
            #self.fta_regs[card][3] += fta_temp2 - fta_temp2


            sta_cc = mysta[0] * tempfta[0] if card > i else -1 * mysta[0] * tempfta[0]
            sta_cbf = tempfta[0] * mysta[1] * tempfta[2]
            sta_cbc = tempfta[0] * mysta[1] * tempfta[3] * 2 if card > i else -2 * tempfta[0] * mysta[1] * tempfta[3]
            sta_bf = tempfta[1] * mysta[2] * -1
            sta_bc = tempfta[1] * mysta[3] * 2 if card > i else -2 * tempfta[1] * mysta[3]
            temp_sta_bf = mysta[2] * -1
            temp_sta_bc = mysta[3] * 2 if card > i else -2 * mysta[3]

            self.sta_regs[card][0] += sta_cc - (sta_cbf + sta_cbc)
            self.sta_regs[card][1] += (sta_cbf + sta_cbc) - sta_cc
            #self.sta_regs[card][2] += temp_sta_bf - temp_sta_bc
            #self.sta_regs[card][3] += temp_sta_bc - temp_sta_bf
            self.sta_regs[card][2] += sta_bf - sta_bc
            self.sta_regs[card][3] += sta_bc - sta_bf

            self.fta_regs[card] = [max(0,i) for i in self.fta_regs[card]]
            self.sta_regs[card] = [max(0,i) for i in self.sta_regs[card]]


kuhn = Kuhn(1000)
kuhn.train()
