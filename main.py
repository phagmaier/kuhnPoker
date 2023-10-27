class Kuhn:
    def __init__(self,epochs=100000,num_sims=1000000):
        self.epochs = epochs
        self.num_posisble_actions = 4
        self.cards = [0,1,2]
        self.fta_strat = [[0.5 for i in range(self.num_posisble_actions)]
                          for i in range(len(self.cards))]
        self.sta_strat = [[0.5 for i in range(self.num_posisble_actions)]
                          for i in range(len(self.cards))]
        self.strat_sum_fta = [[0 for i in range(4)] for x in range(3)]
        self.strat_sum_sta = [[0 for i in range(4)] for x in range(3)]

        self.train()
        self.print_results()
        print()
        print("*" * 20)
        self.p1_winnings = 0
        self.p2_winnings = 0

        self.run_sim(num_sims)
        print(f"PLAYER 1 WON AT A RATE OF: {self.p1_winnings/num_sims}")
        print(f"PLAYER 2 WON AT A RATE OF {self.p2_winnings/num_sims}")
        print("*"*20)



    def print_results(self):
        print("-"*50)
        cardDic = {0:"Jack",1:"Queen",2:"King"}
        actions = {0:"Check",1:"Bet", 2:"Fold", 3: "Call"}
        for i, card in enumerate(self.fta_strat):
            print(f"FIRST TO ACT STRATEGY FOR {cardDic[i]}")
            print("-"*50)
            for x,action in enumerate(card):
                print(f"{actions[x]} at a rate of: {action*100:.2f}%")
                print("-"*50)
        actions = {0:"Check When Checked To", 1: "Bet When Checked To", 2: "Fold When Bet To",
                   3: "Call When Bet To"}
        print("-" * 50)
        for i,card in enumerate(self.sta_strat):
            print(f"SECOND TO ACT STRATEGY FOR {cardDic[i]}")
            print("-"*50)
            for x,action in enumerate(card):
                print(f"{actions[x]} at a rate of: {action*100:.2f}%")
                print("-"*50)


#You should also try doing it where you only update after going through all cards actually yes you should do that now
    def train(self):
        regrets_fta = []
        regrets_sta = []
        for _ in range(self.epochs):
            for card in self.cards:
                regrets_fta.append(self.cfr_fta(card))
                regrets_sta.append(self.cfr_sta(card))
            self.update(regrets_fta,self.fta_strat,self.strat_sum_fta)
            self.update(regrets_sta, self.sta_strat,self.strat_sum_sta)
            regrets_fta = []
            regrets_sta = []
        self.get_final_strat()

    def get_final_strat(self):
        for card in range(len(self.cards)):
            for i in range(len(self.strat_sum_fta[card])):
                self.fta_strat[card][i] = self.strat_sum_fta[card][i]/self.epochs
                self.sta_strat[card][i] = self.strat_sum_sta[card][i] / self.epochs

    #You need to pass the entire star sum a
    def update(self,strat,current,strat_sum):
        for i in range(3):
            first_sum = sum(strat[i][:2])
            second_sum = sum(strat[i][2:])
            if first_sum <= 0:
                current[i][0] = .5
                current[i][1] = .5
            else:
                current[i][0] = strat[i][0]/first_sum
                current[i][1] = strat[i][1]/first_sum
            if second_sum <=0:
                current[i][2] = .5
                current[i][3] = .5
            else:
                current[i][2] = strat[i][2]/second_sum
                current[i][3] = strat[i][3]/second_sum
            strat_sum[i][0] += current[i][0]
            strat_sum[i][1] += current[i][1]
            strat_sum[i][2] += current[i][2]
            strat_sum[i][3] += current[i][3]

    #try this way may need to include my current betting strategies
    def cfr_sta(self,card):
        regret_matching = [0 for i in range(4)]
        sta = self.sta_strat[card]
        for acard in self.cards:
            if acard != card:
                fta = self.fta_strat[acard]

                #check_check = fta[0] if card > acard else fta[0] * -1
                check_check = fta[0] * sta[0] if card > acard else fta[0] * sta[0] * -1

                #bet_call = 2 * fta[1] if card > acard else -2 * fta[1]
                bet_call = 2 * fta[1] * sta[3] if card > acard else -2 * fta[1] * sta[3]

                #bet_fold = fta[1]
                bet_fold = fta[1] * sta[2]

                #check_bet_call = 2 * fta[3] if card > acard else -2 * fta[3]
                check_bet_call = 2 * fta[0] * sta[1] * fta[3] if card > acard else -2 * fta[0] * sta[1] * fta[3]

                #check_bet_fold = fta[2]
                check_bet_fold = fta[0] * sta[1] * fta[2]

                ev_betting = check_bet_call + check_bet_fold

                regret_matching[0] += check_check - ev_betting
                regret_matching[1] += ev_betting - check_check
                regret_matching[2] += bet_fold - bet_call
                regret_matching[3] += bet_call - bet_fold

        regret_matching = [max(0,i) for i in regret_matching]
        return regret_matching

    def cfr_fta(self,card):
        fta = self.fta_strat[card]
        regret_matching = [0 for i in range(4)]
        for acard in self.cards:
            if acard != card:
                sta = self.sta_strat[card]

                #check_check = sta[0] if card > acard else -1 * sta[0]
                check_check = sta[0] * fta[0] if card > acard else -1 * sta[0] * fta[0]

                #check_bet_fold = sta[1] * -1
                check_bet_fold = fta[0] * sta[1] * fta[2] * -1

                #check_bet_call = sta[1] * 2 if card > acard else -2 * sta[1]
                check_bet_call = fta[0] * sta[1] * fta[3] * 2 if card > acard else -2 * fta[0] * sta[1] * fta[3]

                #bet_fold = sta[2]
                bet_fold = fta[1] * sta[2]

                #bet_call = sta[3] * 2 if card > acard else -2 * sta[3]
                bet_call = fta[1] * sta[3] * 2 if card > acard else -2 * sta[3] * fta[1]

                ev_check = check_check + check_bet_call + check_bet_fold
                ev_bet = bet_fold + bet_call

                regret_matching[0] += ev_check - ev_bet
                regret_matching[1] += ev_bet - ev_bet
                regret_matching[2] += bet_fold - bet_call
                regret_matching[3] += bet_call - bet_fold
        regret_matching = [max(0,i) for i in regret_matching]

        return regret_matching

    def run_sim(self, num_games):
        import random
        #p1_winnings = 0
        #p2_winnings = 0
        #random.seed(42)

        def bet_to(card1,card2):
            action = 3 if random.random() > self.sta_strat[card2][2] else 2
            if 2:
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
            action = 1 if random.random() > self.sta_strat[card2][0] else 0
            if 0:
                if card1 > card2:
                    self.p1_winnings += 1
                    self.p2_winnings -= 1
                else:
                    self.p2_winnings +=1
                    self.p1_winnings -= 1
            else:
                action = 3 if random.random() > self.fta_strat[card1][2] else 2
                if 2:
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
            bet_to(card1,card2) if random.random() > self.fta_strat[card1][0] else checked_to(card1,card2)




kuhn = Kuhn()
