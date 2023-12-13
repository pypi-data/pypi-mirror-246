LOG_A = 20
basis = [0] * LOG_A

def insert_vector(mask):
    for i in range(LOG_A - 1, -1, -1):
        if(mask & (1 << i)) == 0:
            continue

        if not basis[i]:
            basis[i] = mask
            return
        
        mask ^= basis[i]


def gcd(a, b, x, y):
    if b == 0:
        x[0] = 1
        y[0] = 0
        return a
    
    x1, y1 = [0], [0]
    d = gcd(b, a%b, x1, y1)
    x[0] = y1[0]
    y[0] = x1[0] - y1[0] * (a // b)
    return d