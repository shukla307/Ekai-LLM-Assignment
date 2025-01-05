import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from datetime import datetime
import json
from typing import List, Dict, Optional

load_dotenv()

class PDFDocumentManager:
    def __init__(self, persist_directory: str = "./pdf_store"):
        """Initialize the PDF document manager."""
        self.persist_directory = persist_directory
        self.embeddings = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2"
        )
        self.vector_store = None
        self.metadata_store = {}
        self.initialize_store()

    def initialize_store(self):
        """Initialize or load the vector store."""
        if os.path.exists(self.persist_directory):
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )
            # Load metadata if exists
            if os.path.exists(f"{self.persist_directory}/metadata.json"):
                with open(f"{self.persist_directory}/metadata.json", 'r') as f:
                    self.metadata_store = json.load(f)
        else:
            os.makedirs(self.persist_directory)
            self.vector_store = Chroma(
                persist_directory=self.persist_directory,
                embedding_function=self.embeddings
            )

    def store_pdf(self, pdf_path: str, metadata: Dict):
        """Store a PDF with its metadata."""
        # Load PDF
        loader = PyPDFLoader(pdf_path)
        documents = loader.load()
        
        # Split documents into chunks
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=100
        )
        splits = text_splitter.split_documents(documents)
        
        # Add metadata to each split
        for split in splits:
            split.metadata.update({
                'date': metadata.get('date', datetime.now().isoformat()),
                'version_tag': metadata.get('version_tag', 'v1.0'),
                'security_tag': metadata.get('security_tag', 'Public'),
                'source': pdf_path
            })
        
        # Store in vector store  [search easily]
        self.vector_store.add_documents(splits)
        
        # Storing the  metadata
        doc_id = os.path.basename(pdf_path)
        self.metadata_store[doc_id] = metadata

    def retrieve_by_date(self, target_date: str, security_clearance: Optional[str] = None) -> List[Dict]:
        """Retrieve documents closest to the target date."""
        target_dt = datetime.fromisoformat(target_date)
        
        # Get all documents using similarity search
        results = self.vector_store.similarity_search("", k=100)  # Get up to 100 documents
        
        if security_clearance:
            results = [doc for doc in results if self._check_security_access(
                doc.metadata['security_tag'], 
                security_clearance
            )]
        
        # Sorting results by date proximity and version tag
        sorted_docs = sorted(
            results,
            key=lambda x: (
                abs((datetime.fromisoformat(x.metadata['date']) - target_dt).days),
                x.metadata['version_tag']
            )
        )
        
        return sorted_docs

    def _check_security_access(self, doc_security: str, user_clearance: str) -> bool:
        """Check if user has appropriate security clearance."""
        security_levels = {
            'Public': 0,
            'Confidential': 1,
            'Restricted': 2,
            'Top Secret': 3
        }
        return security_levels.get(user_clearance, 0) >= security_levels.get(doc_security, 0)







# import os
# from dotenv import load_dotenv
# from langchain_community.document_loaders import PyPDFLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain_community.vectorstores import Chroma
# from langchain_community.embeddings import HuggingFaceEmbeddings
# from datetime import datetime
# import json
# from typing import List, Dict, Optional

# # Load environment variables
# load_dotenv()

# 