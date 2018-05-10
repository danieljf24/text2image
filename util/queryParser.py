import re, nltk

# SEARCH_STOP_WORDS = set() #set(str.split('and or for of the pic img picture image photo'))
SEARCH_STOP_WORDS = set(str.split( 'pic img picture image photo imgs images pics pictures photos am is are was were be been being a an the and but if or because as until while of at by for with about against between into through during before after above below to from up down in out on off over under again s t can will just don should now d ll m o re ve y ain aren couldn didn doesn hadn hasn haven isn ma mightn mustn needn shan shouldn wasn weren won wouldn'))


wnlemm = nltk.WordNetLemmatizer()


def replace(m):
    return re.sub(r'[\s]', '', m.group(0))

def merge_single_chars(query):
    res = re.sub(r"\"(\s*[a-z0-9]\s+[a-z0-9]+\s*)\"", replace, query)
    #res = re.sub(r"\"([a-z0-9]+\s[a-z0-9])\"", replace, res)
    res = re.sub(r"\"(\s*[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s*)\"", replace, res)
    res = re.sub(r"\"(\s*[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s*)\"", replace, res)
    res = re.sub(r"\"(\s*[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s*)\"", replace, res)
    res = re.sub(r"\"(\s*[a-z0-9]\s+[a-z0-9]\s*)\"", replace, res)
    res = re.sub(r"\"(\s*[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s*)\"", replace, res)
    res = re.sub(r"\"(\s*[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]*)\"", replace, res)    
    res = re.sub(r"\"(\s*[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]\s+[a-z0-9]+[a-z0-9]*)\"", replace, res)
    return res    

# def remove_meaningless_words(query):
#     query = query.strip()
#     res = re.sub(r"^ *images?( +of *)? +",' ',query)
#     res = re.sub(r" +images?( +of *)?$",' ',res)
#     res = re.sub(r" +images?( +of *)? +",' ',res)
#     res = re.sub(r"^ *photos?( +of *)? +",' ',res)
#     res = re.sub(r" +photos?( +of *)?$",' ',res)
#     res = re.sub(r" +photos?( +of *)? +",' ',res)
#     res = re.sub(r"^ *pictures?( +of *)? +",' ',res)
#     res = re.sub(r" +pictures?( +of *)?$",' ',res)
#     res = re.sub(r" +pictures?( +of *)? +",' ',res)
#     res = re.sub(r"^ *pics?( +of +)? +",' ',res)
#     res = re.sub(r" +pics?( +of *)?$",' ',res)
#     res = re.sub(r" +pics?( +of *)? +",' ',res)
#     res = re.sub(r"^ *an? +",' ',res)
#     res = re.sub(r" +an? *$",' ',res)
#     res = re.sub(r" +an? +",' ',res)
#     #res = re.sub(r" *the +",'',res)
#     #res = re.sub(r" +the *",'',res)

#     return res.strip()


class QueryParser:
    def __init(self):
        self.name = self.__class__.__name__

    def process(self, rawquery):
        return rawquery


class SimpleQueryParser (QueryParser):
    def process(self, rawquery):
        result = rawquery.lower()
        result = merge_single_chars(result)
        result = re.sub('[^0-9a-z\s]+', '', result)
        # result = remove_meaningless_words(result)
        taglist = []
        for tag in str.split(result):
            if len(tag)<=3:
                taglist.append(tag)
            else:
                taglist.append(wnlemm.lemmatize(tag))
        result = [x for x in taglist if x not in SEARCH_STOP_WORDS]
        return ' '.join(result)

    def process_list(self, rawquery):
        result = rawquery.lower()
        result = merge_single_chars(result)
        result = re.sub('[^0-9a-z\s]+', '', result)
        # result = remove_meaningless_words(result)
        taglist = []
        for tag in str.split(result):
            if len(tag)<=3:
                taglist.append(tag)
            else:
                taglist.append(wnlemm.lemmatize(tag))
        result = [x for x in taglist if x not in SEARCH_STOP_WORDS]
        return result


if __name__ == '__main__':
    queries = ['this u"s', "picture of a dog", "dogs images", 'DoGs', 'jessie "t  v" show house', 'tokyo "   h o t"',
               'images of "3 d" figures', 'drawing "3 dimensional" shapes,', 'thing 1 "t shirt"', '"u s" army', 
               '"U s A " army',' "U   s    A" army', 'pictures of cats', 'cats images', 'image of DoGs', 'a dog', 
               'the dog','pic of obama','  a dog', 'a dog', 'he is an girl', 'image of nishi  a  ', 'fda an', 'a pic of', 'olpicjfdjanimage pic ']  
    qp = SimpleQueryParser()
    
    for query in queries:
        print query, '->', qp.process(query)

