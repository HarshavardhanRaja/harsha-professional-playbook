"""

Group anagrams
I get a list of words [cat, tac, act, debitcard, badcredit, temp]
define a function group_anagram which gives list of groups [[cat, tac, act], [debitcard, badcredit], [temp]]

Method 1: Brute force (compare every pair)
Idea
    For each word, compare with every other word
    Two words are anagrams if sorted(word1) == sorted(word2)

def group_anagrams_bruteforce(words):
    visited = [False] * len(words)
    result = []

    for i in range(len(words)):
        if visited[i]:
            continue

        group = [words[i]]
        visited[i] = True

        for j in range(i + 1, len(words)):
            if not visited[j] and sorted(words[i]) == sorted(words[j]):
                group.append(words[j])
                visited[j] = True

        result.append(group)

    return result

Complexity
Time: O(n² · k log k) (n = number of words, k = average word length)
Space: O(n)

Verdict
❌ Too slow
❌ Not interview-friendly beyond explanation

"""