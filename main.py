import os
import sys
import random
import collections

from text2image import Text2Image

from util.queryParser import SimpleQueryParser
from util.tools import readQidQuery, writeRankingResult, writeDCGResult

from simpleknn.bigfile import BigFile
from basic.metric import getScorer
from basic.annotationtable import readAnnotationsFrom
from basic.common import ROOT_PATH, printMessage, checkToSkip, makedirsforfile


def process(options, trainCollection, devCollection):
    rootpath = options.rootpath
    overwrite = options.overwrite
    metric = options.metric

    qrythres = options.qrythres
    ntopimg = options.ntopimg
    ntopqry = options.ntopqry
    mincc = options.mincc
    feature = options.feature


    # result path
    ranking_result_path = os.path.join(rootpath, devCollection, 'SimilarityIndex', devCollection, 'MetaData', 'text2image', feature)
    DCG_result_path = os.path.join(rootpath, devCollection, metric, 'text2image', feature)
    if checkToSkip(ranking_result_path, overwrite):
        sys.exit(0)
    if checkToSkip(DCG_result_path, overwrite):
        sys.exit(0)

    # inpute of query
    qp = SimpleQueryParser()
    qid_query_file = os.path.join(rootpath, devCollection, 'Annotations', 'qid.text.txt')
    qid_list, query_list = readQidQuery(qid_query_file)   #(qid query)
    qid2query =  dict(zip(qid_list, [qp.process(query) for query in query_list]))

    # random performance for specific queries
    qid_randomperf_file = os.path.join(rootpath, devCollection, 'Annotations', 'qid.random.NDCG@25.txt')
    qid2randomperf = {}
    for line in open(qid_randomperf_file):
        qid, random_perf = line.strip().split()
        qid2randomperf[qid] = float(random_perf)

    
    # path of image feature
    train_feat_path = os.path.join(rootpath, trainCollection, 'FeatureData', feature)
    dev_feat_path = os.path.join(rootpath, devCollection, 'FeatureData', feature)

    nnquery_file = os.path.join(rootpath, devCollection, 'TextData','querynn', options.nnqueryfile)
    qryClick_file = os.path.join(rootpath, trainCollection, 'TextData', options.queryclickfile)
    t2i_searcher = Text2Image(nnquery_file, qryClick_file, dev_feat_path, train_feat_path, ntopqry)

    # calculate DCG@25
    scorer = getScorer(metric)

    done = 0
    failed_count = 0
    qid2dcg = collections.OrderedDict()
    qid2iid_label_score = {}

    for query_id in qid_list:

        iid_list, label_list = readAnnotationsFrom(devCollection, 'concepts%s.txt' % devCollection, query_id, False, rootpath)        

        scorelist = t2i_searcher.doSearch( query_id, iid_list, ntopimg, qrythres, mincc)
         

        if len(scorelist) == 0: 
            failed_count += 1
            qid2dcg[query_id] = qid2randomperf[query_id]
        else:
            qid2iid_label_score[query_id] = zip(iid_list, label_list, scorelist)
            qid2iid_label_score[query_id] = sorted(qid2iid_label_score[query_id], key=lambda v:v[2], reverse=True)
            # calculate the result ranking of DCG@25 from our model
            qid2dcg[query_id] = scorer.score([x[1] for x in qid2iid_label_score[query_id]])
        printMessage("Done", query_id, qid2query[query_id])

        done += 1
        if(done % 20 == 0):
            writeRankingResult(ranking_result_path, qid2iid_label_score)
            qid2iid_label_score = {}
    
    writeRankingResult(ranking_result_path, qid2iid_label_score)
    writeDCGResult(DCG_result_path, qid2dcg)
    print "number of failed query: %d" % failed_count 
    print "average DCG@25: %f" % (1.0*sum(qid2dcg.values())/ len(qid2dcg.values()))
    


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    from optparse import OptionParser
    parser = OptionParser(usage="""usage: %prog [options] trainCollection devCollection""")

    parser.add_option("--overwrite", default=0, type="int", help="overwrite existing file (default: 0)")
    parser.add_option("--rootpath", default=ROOT_PATH, type="string", help="rootpath (default: %s)" % ROOT_PATH)
    parser.add_option("--metric", default='DCG@25', type="string", help="metric (default: DCG@25)")
    parser.add_option("--feature", default="ruccaffefc7.imagenet", type="string", help="image feature (default: ruccaffefc7.imagenet)")

    # text2image parameters
    parser.add_option("--nnqueryfile", default='qid.100nn.score.txt', type="string", help="top 100 visual neighbours with similarity score for each image")
    parser.add_option("--queryclickfile", default='query.clicked.txt', type="string", help="clicked data for each query")
    
    # image2text and text2image parameters
    parser.add_option("--qrythres", default=0.3, type="float", help="query similarity threshold (default: 0.3)")
    parser.add_option("--ntopimg", default=50, type="int", help="the number of top images to represent the test query (default: 50)")
    parser.add_option("--ntopqry", default=30, type="int", help="the number of top relevant queris (default: 10)")
    parser.add_option("--mincc", default=1, type="int", help="minimum click count (default: 1)")

    (options, args) = parser.parse_args(argv)
    if len(args) < 2:
        parser.print_help()
        return 1
    
    return process(options, args[0], args[1])


if __name__ == "__main__":
    sys.exit(main())
