def check_message(message, wordlist):
    reversed_words = [word[::-1] for word in wordlist]
    matcher = Matcher(reversed_words)
    max_length = max([len(word) for word in wordlist])
    ingress_words = [None for _ in range(len(message))]
    for end in range(len(message)):
        start = max(end+1 - max_length, 0)
        substr = message[start:end+1][::-1]
        matches = matcher.match(substr)
        for match in matches: # maximum len(words) matches possible
            source = end - match.length
            if source == -1 or ingress_words[source] != None:
                ingress_words[end] = match.word
                break # we only need to know one way to split the string

    if ingress_words[-1] == None:
        return None
    else:
        return assemble_message(ingress_words, wordlist)


class Matcher:
    def __init__(self, wordlist):
        self.root = Node()
        for index, content in enumerate(wordlist):
            self.root.insert_word(content, index)

    def match(self, substring):
        matches = self.root.match_string(substring)
        return matches


class Match:
    def __init__(self, word):
        self.length = 0
        self.word = word

class Node:
    def __init__(self):
        self.word_id = None
        self.next_nodes = dict()

    def insert_word(self, string, index):
        letter = string[0]
        if letter not in self.next_nodes:
            self.next_nodes[letter] = Node()
        child = self.next_nodes[letter]
        if len(string) == 1:
            child.word_id = index
        else:
            # this will most likely copy (depends on python interna) and may be
            # replaced by passing an index of the handled chars
            child.insert_word(string[1:], index)

    def match_string(self, string):
        if len(string) == 0:
            if self.word_id != None:
                return [Match(self.word_id)]
            else:
                return []

        if string[0] not in self.next_nodes:
            matches = []
        else:
            child = self.next_nodes[string[0]]
            matches = child.match_string(string[1:])

        for match in matches:
            match.length += 1
        if self.word_id != None:
            matches.append(Match(self.word_id))
        return matches

    def get_child(self, letter):
        if letter not in self.next_nodes:
            self.next_nodes[letter] = Node()
        return self.next_nodes[letter]


def assemble_message(ingress_words, wordlist):
    # go from the back of the wordlist
    message = []
    index = len(ingress_words)-1
    while index >= 0:
        message.append(wordlist[ingress_words[index]])
        index -= len(message[-1])

    message = message[::-1]
    print(" ".join(message))


if __name__ == '__main__':
    words = [
        'A',
        'B',
        'AB',
        'ABAC',
        'C',
        ]

    check_message('ABABABABACAAABAC', words)
    # check_message('ABAC', words)
