import os
import math
from util.irc_image import ImageSimer
from util.tools import readNnData, readQueryClickture 


class Text2Image:
    def __init__(self, nnquery_file, qryClick_file, dev_feat_path, train_feat_path, top_n=50):

        # load nn info with score of query
        self.qid2nnqidscore = readNnData(nnquery_file, top_n) # format: query_id query_id score ...
        print ("[%s] %d queris and these top %d nearest neighbours with score loaded from %s" %
        	(self.__class__.__name__, len(self.qid2nnqidscore) , top_n, nnquery_file))


        self.qry2img_clk = readQueryClickture(qryClick_file)   # format: query_id  \t image_id click ...  
        print ("[%s] %d queris and these click info loaded from %s" % 
        	(self.__class__.__name__, len(self.qry2img_clk) ,  qryClick_file))


        self.imgSimer = ImageSimer( dev_feat_path, train_feat_path )



    def doSearch(self, qid, img_list, topImages = 50, qrythres = 0.3, clickthres = 1):
        scorelist = []
        iid_list, weight_list = self.getWeightedImages(qid, topImages, qrythres, clickthres)
        if len(iid_list) == 0 or sum(weight_list) == 0: # cannot find similiar images with similiar query
            return scorelist
        else:
            # for img in img_list:
            #     score = self.imgSimer.clasimiImgwithWeightImgs(img, iid_list, weight_list)
            #     scorelist.append(score)
            scorelist = self.imgSimer.simiImgs_WeightImgs(img_list, iid_list, weight_list)
            
        return scorelist


    def getWeightedImages(self, qid, topImages = 50, qrythres = 0.3, clickthres = 1):
        
        im2click = {}
        flag = 0
        for trainqid, score in self.qid2nnqidscore[qid]:
            score = float(score)
            if score < qrythres: continue
            if score == 1.0:
                flag = 1
            if score < 1.0 and flag > 0 and len(im2click) >= 5:
                break
            for iid, click in self.qry2img_clk[int(trainqid)]:
                if int(click) < clickthres: continue
                im2click[iid] = im2click.get(iid,0) + math.log(int(click)+1)*score

        weightedImages = sorted(im2click.iteritems(), key=lambda v:v[1], reverse=True)

        img_list = [x[0] for x in weightedImages[:topImages] ]
        weight_list = [x[1] for x in weightedImages[:topImages] ]

        return (img_list, weight_list)