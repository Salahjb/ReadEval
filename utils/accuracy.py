# import Levenshtein
#
# def calculate_accuracy(transcript, expected_text):
#     distance = Levenshtein.distance(transcript.lower(), expected_text.lower())
#     accuracy = 1 - distance / max(len(transcript), len(expected_text))
#     return round(accuracy * 100, 2)
#


import Levenshtein

def calculate_accuracy(transcript, expected):
    distance = Levenshtein.distance(transcript.lower(), expected.lower())
    max_len = max(len(transcript), len(expected))
    return round((1 - distance / max_len) * 100, 2)
