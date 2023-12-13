def getCompoundingRate(principal, amount, time):
    """Returns compounding rate for given p, a and t"""
    if amount <= 0 or  principal <= 0:
        return None
    try:
        rate = round(((amount / principal)**(1 / time) - 1) * 100, 2)
        return rate
    except:
        return None
