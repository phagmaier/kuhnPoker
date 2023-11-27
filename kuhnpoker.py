'''
PRETTY SURE WHAT I NEED TO DO TO FIX THE ALGORITHM IS KEEP THE EXACT SAME STRATEGY EXPECT
FOR THE STRAT I'M CALCULATING REGRET FOR YOU JUST TURN THAT TO 100% TAKING THAT ACTION
100% OF THE TIME SO YOU JUST DON'T EVEN CONSIDER BETTING JUST PLAY THE CURRENT
STRAT FOR BOTH PLAYER BUT ONLY CHECK
THEN YOU CALCULATE REGRET BY DOING MODIFIEF 100% STRAT - CURRENT STRAT
'''

class Kuhn:
    def __init__(self,epochs=1000):
        self.epochs = epochs
        self.cards = list(range(3))
        self.fta = [[.5 for i in range(4)] for x in range(3)]
        self.sta = [[.5 for i in range(4)] for x in range(3)]
        self.regrets_fta = [[0 for i in range(4)] for x in range(3)]
        self.regrets_sta = [[0 for i in range(4)] for x in range(3)]
        self.payoffs = self.get_payoffs()
        self.train()
        self.print_results()

    def print_results(self):
        card_dic = {0:"Jack",1:"Queen", 2:"King"}
        fta_dic = {0:"Check", 1:"Bet", 2:"Fold when bet to", 3:"Call when bet to"}
        sta_dic = {0:"Check back", 1:"Bet when checked to", 2: "Fold when bet to", 3: "Call when bet to"}
        print("PLAYER 1 STRATEGY")
        print("-"*50)
        for i,card in enumerate(self.fta):
            print(f"PLAYER 1 STRATEGY with a {card_dic[i]}")
            print("-"*50)
            for x,strat in enumerate(card):
                print(f"{fta_dic[x]} at a rate of: {strat*100:.2f}%")
                print("-"*50)


        print("PLAYER 2 STRATEGY")
        print("-"*50)
        for i,card in enumerate(self.sta):
            print(f"PLAYER 2 STRATEGY with a {card_dic[i]}")
            print("-"*50)
            for x,strat in enumerate(card):
                print(f"{sta_dic[x]} at a rate of: {strat*100:.2f}%")
                print('-'*50)


    def get_payoffs(self):
        temp = {}
        for i in self.cards:
            for x in self.cards:
                if i != x:
                    temp[(i,x)] = 1 if i > x else -1
        return temp

    def train(self):
        for _ in range(self.epochs):
            for card in self.cards:
                regs_fta, regs_sta = self.cfrm(card)
                self.add_regrets(regs_fta,regs_sta,card)
            self.update()

    #WILL HAVE TO REWRITE THIS
    #because you have to average this shit
    #because this is just supposed to give you the next strat to try
    def update(self):
        '''
        fr
        '''
        for i in range(3):
            for x in range(0,4,2):
                total = self.regrets_fta[i][x] + self.regrets_fta[i][x+1]
                total2 = self.regrets_sta[i][x] + self.regrets_sta[i][x+1]
                if total == 0:
                    self.fta[i][x] = .5
                    self.fta[i][x+1] = .5
                else:
                    self.fta[i][x] = self.regrets_fta[i][x] / total
                    self.fta[i][x+1] = self.regrets_fta[i][x+1] / total
                if total2 == 0:
                    self.sta[i][x] = .5
                    self.sta[i][x+1] = .5
                else:
                    self.sta[i][x] = self.regrets_sta[i][x] / total2
                    self.sta[i][x+1] = self.regrets_sta[i][x+1] / total2

    def add_regrets(self,fta,sta,card):
        for i in range(4):
            self.regrets_fta[card][i] += fta[i]
            self.regrets_sta[card][i] += sta[i]

    '''
    DON'T ACTUALLY THINK I NEED THE BAYES FUNCTION JUST DIVIDE BY 2
    '''
    def cfrm(self,card):
        pass
'''
    def bayes(self,cards,index,player,card):
        prob_action = sum(player[i][index] * .5 for i in cards)
        return (player[card][index] * .5) / prob_action
'''


if __name__ == "__main__":
    epochs = 20000
    kuhn = Kuhn(epochs)

