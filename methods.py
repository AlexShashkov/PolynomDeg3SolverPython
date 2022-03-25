from numpy import longdouble as ld

def arsh(x):
    return np.log(x + np.sqrt(x**ld(2)+ld(1)))

def arch(x):
    return np.log(x - np.sqrt(x**ld(2)-ld(1)))

def sh(x):
    return (np.exp(x) - np.exp(-x))/ld(2)

def ch(x):
    return (np.exp(x) + np.exp(-x))/ld(2)
