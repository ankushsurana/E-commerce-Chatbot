import os
import logging
from typing import List, Tuple, Optional
import numpy as np
import faiss
import pickle
from config.config import config
from models.embeddings import EmbeddingModel


class RAGPipeline:
    
    def __init__(self, data_dir: str = None):
        self.data_dir = data_dir or config.DATA_DIR
        self.logger = logging.getLogger(__name__)
        
        self.embedding_model = None
        self.index = None
        self.chunks = []
        self.chunk_metadata = []
        
        try:
            self.embedding_model = EmbeddingModel()
            self.logger.info("RAG pipeline initialized")
        except Exception as e:
            self.logger.error(f"Failed to initialize RAG pipeline: {str(e)}")
            raise
    
    def load_documents(self) -> List[dict]:
        try:
            documents = []
            
            if not os.path.exists(self.data_dir):
                self.logger.warning(f"Data directory not found: {self.data_dir}")
                return documents
            
            for filename in os.listdir(self.data_dir):
                filepath = os.path.join(self.data_dir, filename)
                content = None
                
                try:
                    if filename.lower().endswith('.txt'):
                        content = self._load_txt(filepath)
                    elif filename.lower().endswith('.pdf'):
                        content = self._load_pdf(filepath)
                    
                    if content:
                        documents.append({
                            'filename': filename,
                            'content': content
                        })
                        self.logger.info(f"Loaded document: {filename}")
                        
                except Exception as e:
                    self.logger.error(f"Error loading {filename}: {str(e)}")
            
            self.logger.info(f"Loaded {len(documents)} documents")
            return documents
        
        except Exception as e:
            self.logger.error(f"Error loading documents: {str(e)}")
            raise

    def _load_txt(self, filepath: str) -> str:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()

    def _load_pdf(self, filepath: str) -> str:
        try:
            import pypdf
            text = ""
            with open(filepath, 'rb') as f:
                reader = pypdf.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except ImportError:
            self.logger.error("pypdf not installed. Cannot load PDF.")
            return ""
        except Exception as e:
            self.logger.error(f"Error reading PDF {filepath}: {str(e)}")
            return ""
    
    def chunk_text(self, text: str, chunk_size: int = None, overlap: int = None) -> List[str]:
        chunk_size = chunk_size or config.CHUNK_SIZE
        overlap = overlap or config.CHUNK_OVERLAP
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            if chunk.strip():
                chunks.append(chunk.strip())
            
            start += chunk_size - overlap
        
        return chunks
    
    def create_chunks_from_documents(self, documents: List[dict]) -> List[dict]:
        all_chunks = []
        
        for doc in documents:
            filename = doc['filename']
            content = doc['content']
            
            text_chunks = self.chunk_text(content)
            
            for idx, chunk in enumerate(text_chunks):
                all_chunks.append({
                    'text': chunk,
                    'source': filename,
                    'chunk_id': idx
                })
        
        self.logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks
    
    def build_vector_store(self, chunks: List[dict]):
        try:
            texts = [chunk['text'] for chunk in chunks]
            
            self.logger.info("Generating embeddings...")
            embeddings = self.embedding_model.encode_documents(texts)
            
            dimension = embeddings.shape[1]
            self.index = faiss.IndexFlatL2(dimension)
            self.index.add(embeddings.astype('float32'))
            
            self.chunks = texts
            self.chunk_metadata = [
                {'source': chunk['source'], 'chunk_id': chunk['chunk_id']}
                for chunk in chunks
            ]
            
            self.logger.info(f"Built vector store with {len(texts)} chunks")
        
        except Exception as e:
            self.logger.error(f"Error building vector store: {str(e)}")
            raise
    
    def retrieve(self, query: str, top_k: int = None) -> List[Tuple[str, dict, float]]:
        """
        Retrieve most relevant chunks for a query
        """
        try:
            if self.index is None:
                self.logger.warning("Vector store not initialized")
                return []
            
            top_k = top_k or config.TOP_K_RETRIEVAL
            
            query_embedding = self.embedding_model.encode_query(query)
            query_embedding = query_embedding.reshape(1, -1).astype('float32')
            
            distances, indices = self.index.search(query_embedding, top_k)
            
            results = []
            for dist, idx in zip(distances[0], indices[0]):
                if idx < len(self.chunks):
                    results.append((
                        self.chunks[idx],
                        self.chunk_metadata[idx],
                        float(dist)
                    ))
            
            self.logger.info(f"Retrieved {len(results)} chunks for query")
            return results
        
        except Exception as e:
            self.logger.error(f"Error retrieving chunks: {str(e)}")
            raise
    
    def get_context_for_query(self, query: str, top_k: int = None) -> str:
        try:
            results = self.retrieve(query, top_k)
            
            if not results:
                return ""
            
            context_parts = []
            for idx, (chunk, metadata, distance) in enumerate(results, 1):
                source = metadata['source']
                context_parts.append(f"[Source: {source}]\n{chunk}")
            
            context = "\n\n---\n\n".join(context_parts)
            return context
        
        except Exception as e:
            self.logger.error(f"Error getting context: {str(e)}")
            return ""
    
    def save_vector_store(self, path: str = None):
        try:
            path = path or config.VECTOR_STORE_PATH
            os.makedirs(os.path.dirname(path), exist_ok=True)
            
            faiss.write_index(self.index, f"{path}.index")
            
            with open(f"{path}.pkl", 'wb') as f:
                pickle.dump({
                    'chunks': self.chunks,
                    'metadata': self.chunk_metadata
                }, f)
            
            self.logger.info(f"Saved vector store to {path}")
        
        except Exception as e:
            self.logger.error(f"Error saving vector store: {str(e)}")
            raise
    
    def load_vector_store(self, path: str = None) -> bool:
        try:
            path = path or config.VECTOR_STORE_PATH
            
            if not os.path.exists(f"{path}.index"):
                self.logger.warning(f"Vector store not found at {path}")
                return False
            
            self.index = faiss.read_index(f"{path}.index")
            
            with open(f"{path}.pkl", 'rb') as f:
                data = pickle.load(f)
                self.chunks = data['chunks']
                self.chunk_metadata = data['metadata']
            
            self.logger.info(f"Loaded vector store from {path}")
            return True
        
        except Exception as e:
            self.logger.error(f"Error loading vector store: {str(e)}")
            return False
    
    def initialize(self, force_rebuild: bool = False):
        try:
            if not force_rebuild and self.load_vector_store():
                self.logger.info("Using existing vector store")
                return
            
            self.logger.info("Building new vector store...")
            documents = self.load_documents()
            
            if not documents:
                self.logger.warning("No documents found to build vector store")
                return
            
            chunks = self.create_chunks_from_documents(documents)
            self.build_vector_store(chunks)
            
            self.save_vector_store()
        
        except Exception as e:
            self.logger.error(f"Error initializing RAG pipeline: {str(e)}")
            raise
