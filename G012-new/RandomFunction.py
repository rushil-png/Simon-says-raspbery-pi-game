import random
import numpy as np
from collections import defaultdict

l = []

#Start value -1 as 0 would mean appeared as first number
last_seen = {
    1: -1,
    2: -1,
    3: -1,
    4: -1
}

max_gap = 6

#Markov transition history (records number transitions rather than standalone number)
transitions = defaultdict(float)

for i in range(1, 21):

    numbers = [1, 2, 3, 4]
    weights = []

    #Weights for future number generation
    for n in numbers:
        w = 1.0 #Starting weight

        #Penalises repeated transitions
        if len(l) >= 1:
            prev = l[-1]
            w /= (1 + transitions[(prev, n)])

        #Reduce doubles and triples (almost entirely)
        if len(l) >= 1 and l[-1] == n:
            w *= 0.5 #Discourages doubles

        if len(l) >= 2 and l[-1] == l[-2] == n:
            w *= 0.1 #Strongly discourages triples

        #Penalises 1212 patterns
        if len(l) >= 3:
            if l[-3] == l[-1] and l[-2] == n:
                w *= 0.3

        #Promote numbers not seen for a while
        gap = i - last_seen[n]
        if gap > max_gap:
            w *= 5.0 #Encourage overdue numbers
        else:
            w *= (1 + gap * 0.1)

        weights.append(w)

    #Weighted random selection
    x = random.choices(numbers, weights=weights)[0]

    #Prevent quadruples
    while (len(l) >= 3) and (l[-1] == l[-2] == l[-3] == x):
        x = random.choice(numbers)
    
    #Order of last three sections/blocks strictly necessary

    #Update all variables
    l.append(x)
    last_seen[x] = i

    #Update transition memory
    if len(l) >= 2:
        transitions[(l[-2], l[-1])] += 1

    #Decay transitions/memory fade (old patterns matter less)
    for k in transitions:
        transitions[k] *= 0.98

print(l)
