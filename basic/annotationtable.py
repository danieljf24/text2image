import os

from common import ROOT_PATH

def niceName(qid):
    return '0'if qid[1:-2] == '' else qid[1:-2]

def readAnnotations(inputfile, skip_0=True):
    data = [(str.split(x)[0], int(str.split(x)[1])) for x in open(inputfile).readlines()]
    names = [x[0] for x in data]
    labels = [x[1] for x in data]
    if skip_0:
        idx = [i for i in range(len(names)) if labels[i] != 0]
        names = [names[x] for x in idx]
        labels = [labels[x] for x in idx]
    return (names, labels)

def readAnnotationsFrom(collection, annotationName, concept, skip_0=True, rootpath=ROOT_PATH):
    annotationfile = os.path.join(rootpath, collection, "Annotations", "Image", annotationName, concept + ".txt")
    if not os.path.exists(annotationfile):
        annotationfile = os.path.join(rootpath, collection, "Annotations", "Image", annotationName, niceName(concept), concept + ".txt")
    return readAnnotations(annotationfile, skip_0)


def readConcepts(collection, annotationName, rootpath=ROOT_PATH):
    conceptfile = os.path.join(rootpath, collection, "Annotations",  annotationName)
    return [x.strip() for x in open(conceptfile).readlines() if x.strip()]

def writeConcepts(concepts, resultfile):
    try:
        os.makedirs(os.path.split(resultfile)[0])
    except Exception, e:
        #print e
        pass
    fout = open(resultfile, "w")
    fout.write("\n".join(concepts) + "\n")
    fout.close()

def writeConceptsTo(concepts, collection, annotationName, rootpath=ROOT_PATH):
    resultfile = os.path.join(rootpath, collection, "Annotations", annotationName)
    writeConcepts(concepts, resultfile)


def writeAnnotations(names, labels, resultfile):
    try:
        os.makedirs(os.path.split(resultfile)[0])
    except:
        pass
    fout = open(resultfile, "w")
    fout.write("".join(["%s %g\n" % (im,lab) for (im,lab) in zip(names,labels)]))
    fout.close()
    
def writeAnnotationsTo(names, labels, collection, annotationName, concept, rootpath=ROOT_PATH):
    annotationfile = os.path.join(rootpath, collection, "Annotations", "Image", annotationName, concept + ".txt")
    writeAnnotations(names, labels, annotationfile)
    
def readQueries(inputfile):
    data = [ str.split(x, " ", 1) for x in open(inputfile).readlines()]
    qids = [x[0] for x in data]
    queries = [x[1].rstrip('\n') for x in data]
    return (qids, queries)

def readQueriesFrom(collection, rootpath=ROOT_PATH):
    queryfile = os.path.join(rootpath, collection, "Annotations",  "qid.text.txt")
    return readQueries(queryfile)