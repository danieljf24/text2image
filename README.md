# text2image

The package provides a python implementation of a new text2image baseline for image retrieval and query visualness computation proposed in [1].

## Requirements
### Required Packages
* **python** 2.7
* **NLTK** for query preprocessing

Run the following script to install the NLTK.
```shell
sudo pip install -U nltk
```

### Required Data
Run the following script to download and extract dataset (4.9G).
The extracted data is placed in `$HOME/VisualSearch/`.
```shell
ROOTPATH=$HOME/VisualSearch
mkdir -p $ROOTPATH && cd $ROOTPATH

wget http://lixirong.net/data/text2image-tmm2018/clickture_dataset.tar.gz
tar zxf clickture_dataset.tar.gz
```


## text2image baseline
Run the following script to evaluate text2image baseline on Clickture-dev.
```shell
python main.py msr2013train msr2013dev
# expected performance: NDCG@25 0.5156
```


## Predicting visualness score of a new query
Run the following python snippet to predict visualness score of a new query.
Query words fully matched with specific ImageNet classes are marked out via square brackets.
```python
from visual_detector import VisualDetector

vd = VisualDetector()
query ='hot weather girl' # new query
visualness_score, labeled_query =  vd.predict(query)
print query, "->", labeled_query, visualness_score
# expected output
# hot weather girl -> hot weather [girl] 0.333333333333
```

## Celerity-related Queries
[Here](celebrity.qid.text.txt) we provide 240 celerity-related queries in the Clickture-dev via automatic and manual verification.


### Reference
1. Jianfeng Dong, Xirong Li, Shuai Liao, Jieping Xu, Duanqing Xu, Xiaoyong Du. [Image Retrieval by Cross-Media Relevance Fusion](https://dl.acm.org/citation.cfm?id=2809929). ACM Multimedia, 2015.
2. Jianfeng Dong, Xirong Li, Duanqing Xu. [Cross-Media Similarity Evaluation for Web Image Retrieval in the Wild](https://ieeexplore.ieee.org/abstract/document/8265097/). IEEE Transactions on Multimedia, 2018.
