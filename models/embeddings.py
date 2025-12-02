import logging
from typing import List, Union
import numpy as np
from sentence_transformers import SentenceTransformer
from config.config import config


class EmbeddingModel:
    def __init__(self, model_name: str = None):
        """
        Initialize embedding model
        
        Args:
            model_name: Name of the sentence transformer model (uses config default if None)
        """

        self.model_name = model_name if model_name else config.EMBEDDING_MODEL
        self.logger = logging.getLogger(__name__)
        
        try:
            self.logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            self.logger.info("Embedding model loaded successfully")
        except Exception as e:
            self.logger.error(f"Failed to load embedding model: {str(e)}")
            raise
    
    def encode(
        self, 
        texts: Union[str, List[str]], 
        batch_size: int = 32,
        show_progress_bar: bool = False
    ) -> np.ndarray:
        """
        Encode text(s) into embeddings
        
        Args:
            texts: Single text string or list of text strings
            batch_size: Batch size for encoding
            show_progress_bar: Whether to show progress bar
            
        Returns:
            Numpy array of embeddings
        """
        try:
            if isinstance(texts, str):
                texts = [texts]
            
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                show_progress_bar=show_progress_bar,
                convert_to_numpy=True
            )
            
            return embeddings
        
        except Exception as e:
            self.logger.error(f"Error encoding texts: {str(e)}")
            raise
    
    def encode_query(self, query: str) -> np.ndarray:
        """
        Encode a single query string
        
        Args:
            query: Query text
            
        Returns:
            Query embedding as numpy array
        """
        try:
            embedding = self.encode(query, show_progress_bar=False)
            return embedding[0] 
        except Exception as e:
            self.logger.error(f"Error encoding query: {str(e)}")
            raise
    
    def encode_documents(self, documents: List[str]) -> np.ndarray:
        """
        Encode multiple documents
        
        Args:
            documents: List of document texts
            
        Returns:
            Document embeddings as numpy array
        """
        try:
            embeddings = self.encode(documents, show_progress_bar=True)
            self.logger.info(f"Encoded {len(documents)} documents")
            return embeddings
        except Exception as e:
            self.logger.error(f"Error encoding documents: {str(e)}")
            raise
    
    @property
    def embedding_dimension(self) ->int:
        """Get the dimension of embeddings"""
        return self.model.get_sentence_embedding_dimension()
