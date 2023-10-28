'''
fta = first to act
first row is the jack then the queen then the king
first col of each row is strategy percentage to check
second col is strategu percentage to bet
third is percentage to fold when i check and player bets
fourth row is percentage to call when i check and other player bets

sta = second to act
rows here also represent strategis for when holding certain cards same as fta
first col is percentage to check back
2nd is percentage to bet when check to
3rd is percentage to fold when bet to
3th is percentage to call when bet to
'''
import random
random.seed(42)

fta = [[.5 for i in range(4)] for i in range(3)]
sta = [[.5 for i in range(4)] for i in range(3)]
cards = [0,1,2]
sta_sum = [[0 for i in range(4)] for i in range(3)]
fta_sum = [[0 for i in range(4)] for i in range(3)]

fta_regs = []
sta_regs = []

epochs = 100000
def cfrm(card,fta=fta,sta=sta,cards=cards):
    fta_regrets = [0 for i in range(4)]
    sta_regrets = [0 for i in range(4)]
    myfta = fta[card]
    mysta = sta[card]
    mycards = [i for i in cards if i != card]
    for i in mycards:
        tempsta = sta[i]
        tempfta = fta[i]

        fta_cc = myfta[0] * tempsta[0] if card > i else -1 * myfta[0] * tempsta[0]
        fta_cbc = myfta[0] * tempsta[1] * myfta[3] * 2 if card > i else -2 * myfta[0] * tempsta[1] * myfta[3]
        fta_cbf = -1 *  myfta[0] * tempsta[1] * myfta[2]

        fta_bc = 2 * myfta[1] * tempsta[3] if card > i else -2 * myfta[1] * tempsta[3]
        fta_bf =  myfta[1] * tempsta[2]

        fta_ev_check = fta_cc + fta_cbc + fta_cbf
        fta_ev_bet = fta_bc + fta_bf

        fta_regrets[0] += fta_ev_check - fta_ev_bet
        fta_regrets[1] += fta_ev_bet - fta_ev_check
        fta_regrets[2] += fta_bf - fta_bc
        fta_regrets[3] += fta_bc - fta_bf

        sta_cc = mysta[0] * tempfta[0] if card > i else -1 * mysta[0] * tempfta[0]
        sta_cbf = tempfta[0] * mysta[1] * tempfta[2]
        sta_cbc = tempfta[0] * mysta[1] * tempfta[3] * 2 if card > i else -2 * tempfta[0] * mysta[1] * tempfta[3]
        sta_bf = tempfta[1] * mysta[2] * -1
        sta_bc = tempfta[1] * mysta[3] * 2 if card > i else -2 * tempfta[1] * mysta[3]

        sta_regrets[0] += sta_cc - (sta_cbf + sta_cbc) * random.random()
        sta_regrets[1] += (sta_cbf + sta_cbc) - sta_cc * random.random()
        sta_regrets[2] += sta_bf - sta_bc
        sta_regrets[3] += sta_bc - sta_bf

    return [max(0,i) for i in fta_regrets],[max(0,i) for i in sta_regrets]

def update():
    for it in range(len(sta_regs)):
        # adding randomness to try and get out of local minimums
        a = random.random()
        b = random.random()
        c = random.random()
        d = random.random()
        fta_regs[it][0] *= a
        fta_regs[it][1] *= b
        fta_regs[it][2] *= c
        fta_regs[it][3] *= d
        sta_regs[it][0] *= a
        sta_regs[it][1] *= b
        sta_regs[it][2] *= c
        sta_regs[it][3] *= d
        fta_sum1 = sum(fta_regs[it][:2])
        fta_sum2 = sum(fta_regs[it][2:])
        sta_sum1 = sum(sta_regs[it][:2])
        sta_sum2 = sum(sta_regs[it][2:])

        if fta_sum1 == 0:
            fta[it][0] = .5
            fta[it][1] = .5
            fta_sum[it][0] += .5
            fta_sum[it][1] += .5
        else:
            fta[it][0] = fta_regs[it][0] / fta_sum1
            fta[it][1] = fta_regs[it][1]/fta_sum1
            fta_sum[it][0] += fta[it][0]
            fta_sum[it][1] += fta[it][1]

        if fta_sum2 == 0:
            fta[it][2] = .5
            fta[it][3] = .5
            fta_sum[it][2] += .5
            fta_sum[it][3] += .5

        else:
            fta[it][2] = fta_regs[it][2] / fta_sum2
            fta[it][3] = fta_regs[it][3]/fta_sum2
            fta_sum[it][2] += fta[it][2]
            fta_sum[it][3] += fta[it][3]

        if sta_sum1 == 0:
            sta[it][0] = .5
            sta[it][1] = .5
            sta_sum[it][0] += .5
            sta_sum[it][1] += .5
        else:
            sta[it][0] = sta_regs[it][0] / sta_sum1
            sta[it][1] = sta_regs[it][1]/sta_sum1
            sta_sum[it][0] += sta[it][0]
            sta_sum[it][1] += sta[it][1]

        if sta_sum2 == 0:
            sta[it][2] = .5
            sta[it][3] = .5
            sta_sum[it][2] += .5
            sta_sum[it][3] += .5

        else:
            sta[it][2] = sta_regs[it][2] / sta_sum2
            sta[it][3] = sta_regs[it][3]/sta_sum2
            sta_sum[it][2] += sta[it][2]
            sta_sum[it][3] += sta[it][3]


for _ in range(epochs):
    for card in cards:
        regs1,regs2 = cfrm(card)
        fta_regs.append(regs1)
        sta_regs.append(regs2)
    update()
    fta_regs = []
    sta_regs = []
for i in range(3):
    for x in range(4):
        sta[i][x] = sta_sum[i][x] / epochs
        fta[i][x] = fta_sum[i][x] / epochs


card_dic = {0:"Jack",1:"Queen",2:"King"}
strat_dic = {0:"Check",1:"Bet",2:"Fold When bet to", 3: "Call when bet to"}

print("-" * 50)
for i in range(3):
    print(f"STRATEGY FOR THE FIRST PLAYER TO ACT WITH CARD {card_dic[i]}")
    print("-" * 50)
    temp = fta[i]
    for x in range(4):
        print(f"{strat_dic[x]} at {temp[x] * 100:.2f}%")
        print("-" * 50)

print("-" * 50)
for i in range(3):
    print(f"STRATEGY FOR THE SECOND PLAYER TO ACT WITH CARD {card_dic[i]}")
    print("-" * 50)
    temp = sta[i]
    for x in range(4):
        print(f"{strat_dic[x]} at {temp[x] * 100:.2f}%")
        print("-" * 50)


