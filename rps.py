strats = [.25,.25,.5]
options = ['r','p','s']
outcomes = {}
regrets = [0 for i in range(3)]
strat_sum = [0 for i in range(3)]
for i in options:
    for x in options:
        if i == x:
            outcomes[i+x] = 0
        elif i == 'r':
            outcomes[i+x] = 1 if x == 'p' else -1
        elif i == 'p':
            outcomes[i+x] = 1 if x == 's' else -1
        elif i == 's':
            outcomes[i+x] = 1 if x == 'r' else -1

#It's with respect to the second person chosing
for _ in range(2000):
    for i,p1 in enumerate(options):
        for x,p2 in enumerate(options):
            regrets[x] += outcomes[p1+p2] * strats[i] * strats[x]
            best = max(outcomes[p1+b] * strats[x] * strats[a] for a,b in enumerate(options) if p1+b != p1+p2)
            regrets[x] -= best
    for i in range(3):
        strats[i] = regrets[i] / sum(regrets)
        strat_sum[i] += strats[i]
    regrets = [0 for i in range(3)]

for i,x in enumerate(options):
    print(f"The strat for {x} is: {strat_sum[i]/2000}")






