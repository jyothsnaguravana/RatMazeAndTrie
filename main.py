class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

def insert_word(root, word):
    node = root
    for char in word:
        if char not in node.children:
            node.children[char] = TrieNode()
        node = node.children[char]
    node.is_end_of_word = True

def construct_trie(dictionary):
    root = TrieNode()
    for word in dictionary:
        insert_word(root, word)
    return root

def levenshtein_distance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for index2, char2 in enumerate(s2):
        new_distances = [index2 + 1]
        for index1, char1 in enumerate(s1):
            if char1 == char2:
                new_distances.append(distances[index1])
            else:
                new_distances.append(1 + min((distances[index1], distances[index1 + 1], new_distances[-1])))
        distances = new_distances

    return distances[-1]

def suggest_corrections(root, word):
    suggestions = []
    stack = [(root, "", word)]

    while stack:
        node, current_prefix, remaining_word = stack.pop()
        if node.is_end_of_word:
            suggestions.append(current_prefix)

        for char, child in node.children.items():
            stack.append((child, current_prefix + char, remaining_word))

    suggestions.sort(key=lambda x: levenshtein_distance(x, word))

    return suggestions

def main():
    dictionary = ["the", "thy", "tar", "thru", "hr", "thor", "tur", "thar", "tor", "hell", "helly", "hello", "help", "hells", "sapa", "supa", "swa", "swap", "spa", "project", "coffee", "coffret", "coffer", "coffea"]
    trie_root = construct_trie(dictionary)
    while True:
        user_input = input("Enter a potentially misspelled word or 'exit' to quit: ").lower()
        if user_input == 'exit':
            break
        if user_input.isalpha():
            corrections = suggest_corrections(trie_root, user_input)
            if user_input in dictionary:
                print(f"{user_input} is a valid word.")
            elif corrections:
                print(f"Did you mean: {corrections}")
            else:
                print("No suggestions found.")
        else:
            print("Only alphabetic input is accepted for word suggestions.")

if __name__ == "__main__":
    main()
