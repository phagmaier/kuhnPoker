class Kuhn:
    def __init__(self,epochs=1000):
        self.epochs = epochs
        self.cards = list(range(3))
        self.current_fta = [[.5 for i in range(4)] for x in range(3)]
        self.current_sta = [[.5 for i in range(4)] for x in range(3)]
        self.regrets_fta = [[0 for i in range(4)] for x in range(3)]
        self.regrets_sta = [[0 for i in range(4)] for x in range(3)]
        self.payoffs = self.get_payoffs()

    def get_payoffs(self):
        temp = {}
        for i in self.cards:
            for x in self.cards:
                if i != x:
                    temp[(i,x)] = 1 if i > x else -1
        return temp

    def train(self,card):
        for _ in range(self.epochs):
            for card in self.cards:
                self.cfrm(card)

    def cfrm(self,card):
        fta_regrets = [0 for i in range(4)]
        sta_regrets = [0 for i in range(4)]
        deck = [i for i in self.cards if i!= card]
        fta = self.current_fta[card]
        sta = self.current_sta[card]
        for card2 in deck:
            temp_fta = self.current_fta[card2]
            temp_sta = self.current_sta[card2]
            payoff = self.payoffs[(card,card2)]
            fta_cc = payoff
            fta_cbf = -1
            fta_cbc = 2 * payoff
            fta_bc = 2 * payoff
            fta_bf = 1

            fta_ev_cc = fta[0] * temp_sta[0] * fta_cc
            fta_ev_cbf = -1 * (fta[0] * temp_sta[1] * fta[2])
            fta_ev_cbc = fta_cbc * (fta[0] * temp_sta[1] * fta[3])
            fta_ev_bf = fta[1] * sta[2]
            fta_ev_bc = fta_bc * fta[1] * sta[3]

            sta_ev_cc = temp_fta[0] * sta[0] * -payoff
            sta_ev_cbf = temp_fta[0] * sta[1] * temp_fta[2]
            sta_ev_cbc = temp_fta[0] * sta[1] * temp_fta[3] * -fta_cbc
            sta_ev_bf = -1 * (temp_fta[1] * sta[2])
            sta_ev_bc = -fta_bc * (temp_fta[1] * sta[3])

            fta_ev_checking = fta_ev_cc + fta_ev_cbf + fta_ev_cbc
            checking = fta_cc + fta_cbf + fta_cbc

            fta_ev_betting = fta_ev_bf + fta_ev_bc
            betting = fta_bc + fta_bf

            fta_regrets[0] += checking - fta_ev_checking
            fta_regrets[1] += betting - fta_ev_betting
            fta_regrets[2] += fta_bf - fta_ev_bf
            fta_regrets[3] += fta_bc - fta_ev_bc

            sta_regrets[0] += -fta_cc - sta_ev_cc
            sta_regrets[1] += -1 * (fta_cbf + fta_cbc) - (sta_ev_cbf + sta_ev_cbc)
            sta_regrets[2] += -1 - sta_ev_cbf
            sta_regrets[3] += -sta_ev_cbc - sta_ev_cbc












if __name__ == "__main__":
    epochs = 1000
    kuhn = Kuhn(epochs)
