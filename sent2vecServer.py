#!/usr/bin/env python3
import sent2vec

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

# Intialize model
print("Loading model")
model = sent2vec.Sent2vecModel()
model.load_model("models/wiki_unigrams.bin")
print("Model loaded")

# Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

def embed_sentence(sentence):
	return model.embed_sentence(sentence).tolist()
def embed_sentences(sentences):
	return model.embed_sentences(sentences).tolist()

# Create server
print("Starting server")
with SimpleXMLRPCServer(("localhost", 8123), requestHandler=RequestHandler) as server:
    server.register_introspection_functions()
    server.register_function(embed_sentence)
    server.register_function(embed_sentences)
    server.serve_forever()