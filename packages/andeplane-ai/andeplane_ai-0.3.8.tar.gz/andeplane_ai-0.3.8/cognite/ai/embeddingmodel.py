import numpy as np

class EmbeddingModel:
    '''
    EmbeddingModel gets vector embeddings from Cognite Data Fusion
    '''
    def __init__(self, client, model_name='multilingual-e5-small'):
        self.client = client
        self.model_name = model_name
        if self.model_name == "multilingual-e5-small":
            self.dimension = 384
            self.max_seq_length = 1000 # Depending on model
        elif self.model_name == "all-minilm-l6-v2":
            self.dimension = 384
            self.max_seq_length = 1000 # Depending on model
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
    def embed(self, texts, max_seq_length=256):
        # Divide chunks of 10 texts
        chunks = [texts[i:i + 10] for i in range(0, len(texts), 10)]
        vectors = []
        for chunk in chunks:
            body = {
                "items": [{"text": text, "model": self.model_name} for text in chunk],
            }
            
            embedding_response = self.client.post(f"/api/v1/projects/{self.client.config.project}/vectorstore/embeddings", body)
            vectors.extend([v["values"] for v in embedding_response.json()["items"]])
            
        return np.asarray(vectors)
