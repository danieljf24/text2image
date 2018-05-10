import os
import copy
from util.queryParser import SimpleQueryParser


def gene_imagenet_synset(output_file):
    sid2synset = {}
    for line in open('visualness_data/words.txt'):
        sid, synset = line.strip().split('\t')
        sid2synset[sid] = synset

    fout = open(output_file, 'w')
    for line in open('visualness_data/imagenet.synsetid.txt'):
        sid = line.strip()
        fout.write(sid + "\t" + sid2synset[sid].lower().replace('-', ' ') + '\n')
    fout.close()


def readImageNetSynset():
    len2visualsynset = {}

    data_file = 'visualness_data/imagenet.sid.synset.txt'
    if not os.path.exists(data_file):
        gene_imagenet_synset(data_file)


    for line in open(data_file):
        sid, synsets_data = line.strip().split("\t")
        synsets = map(str.strip, synsets_data.strip().split(','))
        for synset in synsets:
            words = synset.strip().split()
            length = len(words)
            len2visualsynset.setdefault(length, []).append(" ".join(words))

    # print 'length:', len2visualsynset.keys()
    new_len2visualsynset = {}
    for key in len2visualsynset:
        new_len2visualsynset[key] = set(len2visualsynset[key])
    return new_len2visualsynset

class VisualDetector:
    def __init__(self):
        self.len2visualsynset = readImageNetSynset()
        self.qp = SimpleQueryParser()

    def predict(self, query):

        origin_word_list = self.qp.process_list(query)
        original_len = len(origin_word_list)

        word_list = copy.deepcopy(origin_word_list)
        all_len = len(word_list)
        valid_len = len(word_list)
        current_group = max(self.len2visualsynset.keys())
        match_counter = 0

        while current_group > 0:
            if valid_len == 0:
                break
            while current_group > valid_len:
                current_group -= 1
            match_flag = 0
            for i in range(0, all_len + 1 - current_group):
                pattern = " ".join(word_list[i:i+current_group])
                if "#" in pattern:
                    continue
                else:
                    if pattern in self.len2visualsynset[current_group]:
                        word_list = word_list[:i] + ['#%d' % current_group] + word_list[i+current_group:]
                        all_len = all_len - current_group + 1
                        valid_len = valid_len - current_group
                        match_counter += current_group
                        match_flag = 1
                        break

            if match_flag == 0:
                current_group -= 1

        index = 0
        labeled_query = []
        for word in word_list:
            if word.startswith("#"):
                n_words = int(word[1:])
                new_word = "[" + " ".join(origin_word_list[index:index+n_words]) + "]"
                labeled_query.append(new_word)
                index += n_words
            else:
                labeled_query.append(word)
                index += 1

        return 0 if match_counter == 0 else 1.0*match_counter/original_len, " ".join(labeled_query)


if __name__ == "__main__":
    vd = VisualDetector()
    query_list = ["flowers", "soccer ball", "dogs and cat", "tattoo design", "barack obama family", "hot weather girls", "funny", "saying and quote"]
    for query in query_list:
        # print query
        visualness_score, labeled_query =  vd.predict(query)
        print query, "->", labeled_query, visualness_score, '\n'
