import difflib

s1 = [1, 2, 3, 5, 6, 4]
s2 = [2, 3, 5, 4, 6, 1]

matcher = difflib.SequenceMatcher(a=s1, b=s2)

