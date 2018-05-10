import numpy as np
from scipy.spatial import distance
from simpleknn.bigfile import BigFile


def calImageSimiByL2(image_1, image_2):
    A = np.mat(image_1)
    B = np.mat(image_2)
    dist = 1.0/(1 + np.linalg.norm(A-B, axis=1))
    return dist.tolist()

def calImageSimiByCos(image_1, image_2):
    A = np.mat(image_1)
    B = np.mat(image_2)
    num = A * B.T
    denom = np.linalg.norm(A) * np.linalg.norm(B, axis=1)
    cos = num / denom

    return cos.tolist()[0]


class ImageSimer:
    def __init__(self, dev_feat_path, train_feat_path):
        self.dev_feats = BigFile(dev_feat_path)
        self.train_feats =  BigFile(train_feat_path)


    def calsimImage(self, img, imgs):
        imgfeat = self.dev_feats.read_one(img)

        renamed, test_X = self.train_feats.read(imgs)
        resorted_feats = [None] * len(renamed)
        for i in xrange(len(renamed)):
            idx = imgs.index(renamed[i])
            resorted_feats[idx] = test_X[i]

        return calImageSimiByCos( imgfeat, resorted_feats)


    def calsimiImagewithClick(self, img, img_click_list, clickthres):
        
        imgfeat = self.dev_feats.read_one(img)

        img_list = [x[0] for x in img_click_list if int(x[1]) >= clickthres]
        clc_list = [int(x[1]) for x in img_click_list if int(x[1]) >= clickthres]
        assert (len(img_list) == len(clc_list))

        renamed, test_X = self.train_feats.read(img_list)

        # re-sort the label list according to the renamed
        resorted_feats = [None] * len(renamed)
        for i in xrange(len(renamed)):
            idx = img_list.index(renamed[i])
            resorted_feats[idx] = test_X[i]

        img_simi = calImageSimiByCos( imgfeat, resorted_feats)

        return sum(np.array(img_simi) * np.log(clc_list)) / len(img_list)


    def clasimiImgwithWeightImgs(self, img, imgs, weightes):

        assert(len(imgs) == len(weightes))
        imgfeat = self.dev_feats.read_one(img)
        renamed, feats = self.train_feats.read(imgs)
        
        # re-sort the label list according to the renamed
        resorted_weight = [None] * len(weightes)
        for i in xrange(len(renamed)):
            idx = imgs.index(renamed[i])
            resorted_weight[i] = weightes[idx]

        simi_list = calImageSimiByCos(imgfeat, feats)

        normal_weight = np.array(resorted_weight) / sum(resorted_weight)

        score = np.dot(normal_weight, np.array(simi_list) )

        return score


    def simiImgs_WeightImgs(self, t_img_list, s_img_list, weightes):
        assert(len(s_img_list) == len(weightes))

        t_renamed, t_feats = self.dev_feats.read(t_img_list)
        s_renamed, s_feats = self.train_feats.read(s_img_list)

        # re-sort the label list according to the renamed
        resorted_weight = [None] * len(weightes)
        for i in xrange(len(s_renamed)):
            idx = s_img_list.index(s_renamed[i])
            resorted_weight[i] = weightes[idx]
        normal_weight = np.array(resorted_weight) / sum(resorted_weight)

        cosineSimi = -(distance.cdist(t_feats, s_feats, 'cosine')-1)
        weightSimi = np.dot(cosineSimi, normal_weight)

        renamed2sim = dict(zip(t_renamed, list(weightSimi)))
        final_score = []
        for key in t_img_list:
            final_score.append(renamed2sim[key])
        return final_score


if __name__ == '__main__':
    image_1 = [1,2,3,4,5]
    image_2 = [2,2,3,4,5]
    image_3 = [4,0,0,2,1]
    image_list = [[2,2,3,4,5],[4,0,0,2,1]]
    print calImageSimiByCos(image_1, image_2)
    print calImageSimiByCos(image_1, image_3)
    print calImageSimiByCos(image_1, image_list)