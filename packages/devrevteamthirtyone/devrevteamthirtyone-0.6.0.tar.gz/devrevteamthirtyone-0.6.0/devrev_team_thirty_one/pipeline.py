from .imports import *
from .model import Model
from .retriever import Retriever
from .pipeline_config import PipeConfig
class Pipeline:
    def __init__(self,config):
        self.config = config
        self.rtr = Retriever(config.embedding_model)
        self.model = Model(self.config)
    def __call__(self,query, tools,examples):
        retrieved_tools = self.rtr(query,tools,self.config.num_retrieved)
        output = self.model(query,self.rtr.strip_embeddings(retrieved_tools),examples)
        return json.loads(output)