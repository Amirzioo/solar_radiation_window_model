

def calc_absorbed(tau, G, A):
    return (1 - tau) * G * A

def calc_transmitted(tau, G, A):
    return (tau) * G * A