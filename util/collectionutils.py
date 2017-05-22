from collections import Counter


def sublist(lst1, lst2):
    c1 = Counter(lst1)
    c2 = Counter(lst2)
    for item, count in c1.items():
        if count > c2[item]:
            return False
    return True
