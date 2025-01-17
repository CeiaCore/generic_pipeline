

from typing import List
from src.core.components.embedding.interfaces.embedding_interface import EmbeddingInteface
from langchain_openai import AzureOpenAIEmbeddings, OpenAIEmbeddings


class AzureEmbeddings(EmbeddingInteface):
    
    def __init__(self, model: str,azure_deployment: str, dimensions:int = None):
        
        self.embeddings = AzureOpenAIEmbeddings(
        model=model,
        azure_deployment=azure_deployment,
        dimensions=dimensions
    )
            
    def embedding_query(self, query: str) -> List[float]:
        query_embedded = self.embeddings.embed_query(query)
        return query_embedded    
    
    def embedding_documents(self, documents: List[str], chunk_size: int | None = None) -> List[List[float]]:
        return super().embedding_documents(documents, chunk_size)
        
    def embedding_chunks(self, chunks, batch_size: int = 1) -> List[dict]:
        
        for i in range(0, len(chunks), batch_size):
                request = [x["conteudo"] for x in chunks[i : i + batch_size]]
                response = self.embeddings.embed_documents(texts=request)
                for x, e in zip(chunks[i : i + batch_size], response):
                    x["embedding"] = e
                print(f"Embedded {i}")
        
        return chunks