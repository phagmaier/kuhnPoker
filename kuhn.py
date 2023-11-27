'''
FTA MEANS FIRST TO ACT
STA MEANS SECOND TO ACT
STRATEGIES ARE STORED AS FOLLOWS:
EACH ROW REPRSENTS A STRATEGY FOR A PARTICULAR CARD
FOR FTA:
COL 0 = CHECK
COL 1 = BET
COL 2 = FOLD WHEN FTA CHECKS AND STA BETS
COL 3 = CALL WHEN FTA CHECKS AND STA BETS

FOR STA:
COL 0 = CHECK BACK WHEN CHECKED TO
COL 1 = BET WHEN CHECKED TO
COL 2 = FOLD WHEN BET TO
COL 3 = CALL WHEN BET TO
'''


class Kuhn:
    def __init__(self,epochs):
        self.epochs = epochs
        self.fta = [[.5 for _ in range(4)]for _ in range(3)]
        self.sta = [[.5 for _ in range(4)]for _ in range(3)]
        self.fta_regrets = [[0 for _ in range(4)]for _ in range(3)]
        self.sta_regrets = [[0 for _ in range(4)]for _ in range(3)]
        self.cards = list(range(3))
        self.final_fta = None
        self.final_sta = None
        self.results = self.get_results()
        self.train()
        self.get_final_strat()
        self.print_strat()

    def print_strat(self):
        cards = {0:"Jack",1:"Queen",2:"King"}
        p1_strat = {0:"Check",1:"Bet",2:"Fold when bet to",3:"Call when bet to"}
        p2_strat = {0:"Check back", 1:"Bet when checked to",2:"Fold when bet to",
                    3:"Call when bet to"}
        print("STRATEGY FOR PLAYER 1")
        print("-"*50)
        for i in range(len(self.fta)):
            print(f"Strategy for when player has a {cards[i]}")
            print("-"*50)
            for x,strat in enumerate(self.fta[i]):
                print(f"{p1_strat[x]} at a rate of: {strat*100:.2f}%")
                print("-"*50)

        print("STRATEGY FOR PLAYER 2")
        print("-"*50)
        for i in range(len(self.sta)):
            print(f"Strategy for when player has a {cards[i]}")
            print("-"*50)
            for x,strat in enumerate(self.sta[i]):
                print(f"{p2_strat[x]} at a rate of: {strat*100:.2f}%")
                print("-"*50)


    def get_results(self):
        results = {}
        for i in self.cards:
            for x in self.cards:
                if i != x:
                    results[(i,x)] = 1 if i> x else -1
        return results

    def get_final_strat(self):
        for count in range(len(self.fta)):
            for i in range(0,4,2):
                total1 = self.fta_regrets[count][i] + self.fta_regrets[count][i+1]
                total2 = self.sta_regrets[count][i] + self.sta_regrets[count][i+1]
                if total1 == 0:
                    self.fta[count][i] = .5
                    self.fta[count][i+1] = .5
                else:
                    self.fta[count][i] = self.fta[count][i]/total1
                    self.fta[count][i+1] = self.fta[count][i+1]/total1

                if total2 == 0:
                    self.sta[count][i] = .5
                    self.sta[count][i+1] = .5
                else:
                    self.sta[count][i] = self.sta[count][i]/total2
                    self.sta[count][i+1] = self.sta[count][i+1]/total2

    def train(self):
        for _ in range(self.epochs):
            regs1 = [[0 for _ in range(4)]for _ in range(3)]
            regs2 = [[0 for _ in range(4)]for _ in range(3)]
            for card in self.cards:
                regs1[card],regs2[card] = self.cfrm(card)
            self.update(regs1,regs2)

    def update(self,fta,sta):
        count = 0
        for card1,card2 in zip(fta,sta):
            for i in range(0,4,2):
                total1 = card1[i] + card1[i+1]
                total2 = card2[i] + card2[i+1]
                if total1 == 0:
                    self.fta[count][i] = .5
                    self.fta[count][i+1] = .5
                else:
                    self.fta[count][i] = card1[i] / total1
                    self.fta[count][i+1] = card1[i+1] / total1
                    self.fta_regrets[count][i] += card1[i]
                    self.fta_regrets[count][i+1] += card1[i+1]

                if total2 == 0:
                    self.sta[count][i] = .5
                    self.sta[count][i+1] = .5
                else:
                    self.sta[count][i] = card2[i] / total2
                    self.sta[count][i+1] = card2[i+1] / total2
                    self.sta_regrets[count][i] += card2[i]
                    self.sta_regrets[count][i+1] += card2[i+1]
            count +=1


    def cfrm(self,card):
        ev_fta = 0
        ev_sta = 0
        #modified version where the strategy we are looking at is played 100% of the time
        m_fta = [0 for _ in range(4)]
        m_sta = [0 for _ in range(4)]
        deck = [i for i in self.cards if i!= card]
        fta = self.fta[card]
        sta = self.sta[card]
        for card2 in deck:
            payoff = self.results[(card,card2)]
            sta2 = self.sta[card2]
            fta2 = self.fta[card2]

            #calculate the total ev at current strat
            ev_fta += fta[0] * sta2[0] * payoff
            ev_fta += fta[0] * sta2[1] * fta[2] * -1
            ev_fta += fta[0] * sta2[1] * fta[3] * 2 * payoff
            ev_fta += fta[1] * sta2[2]
            ev_fta += 2 * payoff * fta[1] * sta2[3]

            #calculating for always checking
            m_fta[0] += sta2[0] * payoff
            m_fta[0] += sta2[1] * -1 * fta[2]
            m_fta[0] += sta2[1] * fta[3] * 2 * payoff

            #calculate always betting
            m_fta[1] += sta2[3] * 2 * payoff
            m_fta[1] += sta2[2] * -1

            #always fold when bet to
            m_fta[2] += fta[0] * sta2[0] * payoff
            m_fta[2] += fta[0] * sta2[1] * -1
            m_fta[2] += fta[1] * sta2[2]
            m_fta[2] += fta[1] * sta2[3] * 2 * payoff

            #always call when bet to
            m_fta[3] += fta[0] * sta2[0] * payoff
            m_fta[3] += fta[0] * sta2[1] * 2 * payoff
            m_fta[3] += fta[1] * sta2[2]
            m_fta[3] += fta[1] * sta2[3] * 2 * payoff


            #calculate the total ev at current strat
            ev_sta += fta2[0] * sta[0] * payoff
            ev_sta += fta2[0] * sta2[1] * fta2[2]
            ev_sta += fta2[0] * sta[1] * fta2[3] * 2 * payoff
            ev_sta += fta2[1] * sta[2] * -1
            ev_sta += 2 * payoff * fta2[1] * sta[3]

            #always check back
            m_sta[0] += fta2[0] * payoff
            m_sta[0] += fta2[1] * sta[2] * -1
            m_sta[0] += fta2[1] * sta[3] * 2 * payoff

            #always bet when checked to
            m_sta[1] += fta2[0] * fta2[2]
            m_sta[1] += fta2[0] * fta2[3] * 2 * payoff
            m_sta[1] += 2 * payoff * fta2[1] * sta[3]
            m_sta[1] += fta2[1] * sta[2] * -1

            #always call when bet to
            m_sta[3] += fta2[0] * sta[0] * payoff
            m_sta[3] += fta2[0] * sta[1] * fta2[2]
            m_sta[3] += fta2[0] * sta[1] * fta2[3] * 2 * payoff
            m_sta[3] += fta2[1] * 2 * payoff

            #always fold when bet to
            m_sta[2] += fta2[0] * sta[0] * payoff
            m_sta[2] += fta2[0] * sta2[1] * fta2[2]
            m_sta[2] += fta2[0] * sta[1] * fta2[3] * 2 * payoff
            m_sta[2] += fta2[1] * -1

        return [max(0,i-ev_sta) for i in m_fta],[max(0,i-ev_sta) for i in m_sta]

if __name__ == '__main__':
    kuhn = Kuhn(10000)
