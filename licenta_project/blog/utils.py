import re

def normalize_label(label):
    words = label.replace('_',' ').split()
    return ' '.join(word.capitalize() for word in words)