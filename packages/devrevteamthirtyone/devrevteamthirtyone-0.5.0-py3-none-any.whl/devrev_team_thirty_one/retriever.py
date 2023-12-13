from .imports import *
import numpy as np


class Retriever:
    def __init__(self, model_name):
        self.model_name = model_name
        self._tools = []
        self._tool_names = set()

    def embed(self, text):
        return np.array(EmbeddingBackend(self.model_name, text).data[0]['embedding'])

    def get_doc(self, tool):
        s = tool['tool_description']
        for arg in tool['args']:
            s += ' ' + arg['arg_description']
        return s

    def index(self, tools):
        for tool in tools:
            if tool['tool_name'] in self._tool_names:
                continue
            tool['embedding'] = self.embed(self.get_doc(tool))
            self._tool_names.add(tool['tool_name'])
            self._tools.append(tool)

    def embedding_similarity(self, query_embedding, tool_embedding):
        return (query_embedding.T @ tool_embedding)

    def __call__(self, query, tools=None, k=8):
        self.index(tools)
        query_embed = self.embed(query)
        for tool in self._tools:
            tool['similarity'] = self.embedding_similarity(query_embed, tool['embedding'])
        return_tools = sorted(self._tools, key=lambda x: x['similarity'], reverse=True).copy()
        return_tools = [tool for tool in return_tools if tool in tools]
        return return_tools[:k]

    @staticmethod
    def strip_embeddings(tools):
        tools = copy.deepcopy(tools)
        for tool in tools:
            del tool['embedding']
            del tool['similarity']
        return tools
