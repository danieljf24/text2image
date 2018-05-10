import sys,os
import numpy as np
import cPickle as pickle


# SEARCH_STOP_WORDS = set(str.split('and with or for of the pic img picture image photo a an imgs images pics pictures photos'))
SEARCH_STOP_WORDS = set(str.split( 'pic img picture image photo imgs images pics pictures photos am is are was were be been being a an the and but if or because as until while of at by for with about against between into through during before after above below to from up down in out on off over under again s t can will just don should now d ll m o re ve y ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn'))


class QuerySimer:
    def __init__(self):
        print "Done" 

    def sim(self, query_1, query_2):
        return 0.0
    
    def simList(self, query, query_list):
        return [ self.sim(query, x) for x in query_list]


class OverlapSimer(QuerySimer):
    def __init__(self):
        QuerySimer.__init__(self)

    def sim(self, query_1, query_2):
        query_1_list = [query for query in query_1.split() if query not in SEARCH_STOP_WORDS]
        query_2_list = [query for query in query_2.split() if query not in SEARCH_STOP_WORDS]
        inter_len = len(set(query_1_list).intersection(set(query_2_list)))
        union_len = len(set(query_1_list).union(set(query_2_list)))
        
        return 0 if union_len == 0 else 1.0*inter_len/union_len


    def calsimiQuerywithClick(self, query, qry_click_list, clickthres):

        qry_simi = []
        qry_list = [x[0] for x in qry_click_list if int(x[1]) >= clickthres]
        clc_list = [int(x[1]) for x in qry_click_list if int(x[1]) >= clickthres]

        # clc_list = np.array(clc_list) + 1

        for idx in xrange(len(qry_list)):
            qry_simi.append(self.sim(query, qry_list[idx]))

        return 0 if len(qry_list)==0 else sum(np.array(qry_simi) * np.log(clc_list)) / len(qry_list)


def getQuerySimer(name):
    mapping = {"O":OverlapSimer}  #you can add other query simer here
    return mapping[name]()

def claSimQuery2WeightedQ(query, weightedQuery):
    words = query.split()
    score = 0
    for word in words:
        score = score + weightedQuery.get(word, 0)
    if len(words) == 0:
        return 0
    else:
        return 1.0*score/ len(words)




if __name__ == '__main__':
    query_1 = "a big dog image"
    query_2 = "a red dog image"
    query_3 = ["funny dog", "a red dog"]
    
    name = "O"
    simer = getQuerySimer('/home/danieljf24/RUC/VisualSearch/msr2013train/TextData', name)

    print simer.sim(query_1, query_2)
    print simer.simList(query_1, query_3)
    # print scorer.score(sorted_labels)
    # print scorer.getLength(sorted_labels)