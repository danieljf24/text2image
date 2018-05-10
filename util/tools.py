import os


def readQidQuery(inputfile):
    data = [ x.strip().split(" ", 1) for x in open(inputfile).readlines()]
    qid = [x[0] for x in data]
    query = [x[1] for x in data]
    return (qid, query)


def readNnData(inputfile, n_top = 50):    # format: key data1 data2 data1 data2
    keyid2data = {}
    for line in open(inputfile):
        data = line.strip().split(' ')
        key = data[0]
        data1_data2 = data[1:]
        if n_top == -1:
            length = len(data1_data2)
        else:
            length = 2*n_top if len(data1_data2) > 2*n_top else len(data1_data2)
        data1 = [data1_data2[x] for x in range(0,length,2)]
        data2 = [float(data1_data2[x]) for x in range(1,length,2)]
        assert(len(data1) == len(data2)),"data1: %d, data2:%d" % (len(data1),len(data2))
        keyid2data[key] = zip(data1, data2)
    return keyid2data


def readQueryClickture(inputfile, n_top=-1):    # format: key \t data1 data2 data1 data2
    keyid2data = {}
    for index, line in enumerate(open(inputfile)):
        data = line.strip().split('\t')
        if len(data) > 1:
            data1_data2 = data[1].strip().split()
        else:
            data1_data2 = []
        if n_top == -1:
            length = len(data1_data2)
        else:
            length = 2*n_top if len(data1_data2) > 2*n_top else len(data1_data2)
        data1 = [data1_data2[x] for x in range(0,length,2)]
        data2 = [data1_data2[x] for x in range(1,length,2)]
        assert(len(data1) == len(data2)),"data1: %d, data2:%d" % (len(data1),len(data2))
        keyid2data[index] = zip(data1, data2)
    return keyid2data



def readImageClickture(inputfile, n_top_query):   # format: img_id /t query /t click ...
    img2query_clc = {}
    for line in open(inputfile):
        data = line.strip().split('\t')
        img = data[0]
        querylist = data[1:]
        if n_top_query == -1:
            length = len(querylist)
        else:
            length = 2*n_top_query if len(querylist) > 2*n_top_query else len(querylist)
        query = [querylist[x] for x in range(0,length,2)]
        click = [int(querylist[x]) for x in range(1,length,2)]
        assert(len(query) == len(click))
        img2query_clc[img] = zip(query, click)

    return img2query_clc




def writeRankingResult(outputfileDir, qid2iid_label_score):
    try:
        os.makedirs(outputfileDir)
    except Exception, e:
        #print e
        pass
    for qid in qid2iid_label_score:
        fout = open(os.path.join(outputfileDir, qid+'.txt'), "w")
        fout.write("".join(["%s %g\n" % (iid,score) for (iid,lab,score) in qid2iid_label_score[qid]]))
        fout.close()
    

def writeDCGResult(outputfileDir, qid2dcg):
    try:
        os.makedirs(outputfileDir)
    except Exception, e:
        #print e
        pass
    fout = open(os.path.join(outputfileDir, 'DCG@25.txt'), "w")
    overall_DCG = sum(qid2dcg.values())/len(qid2dcg.values())
    fout.write("Overall: %g\n" % overall_DCG )
    fout.write("\n".join(["%s %g" % (k,v) for (k,v) in qid2dcg.iteritems() ]))
    fout.close()
