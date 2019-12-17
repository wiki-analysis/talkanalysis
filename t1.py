import gensim
from scipy import spatial
model = gensim.models.Word2Vec.load('doc2vec.model')
def simu(s1,s2):
    vec1 = model.infer_vector(s2.split())
    vec2=model.infer_vector(s1.split())
    similairty = spatial.distance.cosine(vec1, vec2)
    return similairty
