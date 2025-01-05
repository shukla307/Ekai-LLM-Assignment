from pdf_manager import PDFDocumentManager
import os
from dotenv import load_dotenv

def main():
    print("Starting the program...")
    
    print("Initializing PDFDocumentManager...")
    try:
        manager = PDFDocumentManager()
        print("Manager initialized successfully!")
    except Exception as e:
        print(f"Error initializing manager: {str(e)}")
        return

    # Check if PDF exists
    pdf_path = r"C:\Users\shiva\Downloads\Assignment.pdf"
    print(f"Checking if PDF exists at: {pdf_path}")
    if not os.path.exists(pdf_path):
        print(f"ERROR: PDF not found at {pdf_path}")
        return
    else:
        print("PDF file found!")

    # Store the PDF with metadata
    metadata_v1 = {
        "date": "2023-01-01",
        "version_tag": "v1.0",
        "security_tag": "Public"
    }
    
    print("Attempting to store PDF...")
    try:
        manager.store_pdf(pdf_path, metadata_v1)
        print("PDF stored successfully!")
    except Exception as e:
        print(f"Error storing PDF: {str(e)}")
        return

    print("\nAttempting to retrieve documents...")
    try:
        results = manager.retrieve_by_date("2023-03-08", security_clearance="Confidential")
        print(f"Found {len(results)} documents")
        
        if results:
            doc = results[0]  # Get the first result
            print("\nFirst document details:")
            print(f"Date: {doc.metadata['date']}")
            print(f"Version: {doc.metadata['version_tag']}")
            print(f"Security: {doc.metadata['security_tag']}")
            print(f"Content preview: {doc.page_content[:200]}...")
        else:
            print("No documents found matching the criteria")
            
    except Exception as e:
        print(f"Error retrieving documents: {str(e)}")

if __name__ == "__main__":
    main()




# from pdf_manager import PDFDocumentManager
# import os
# from dotenv import load_dotenv

# def main():
#     print("Starting the program...")
    
#     # Check if .env file exists and OPENAI_API_KEY is set
#     print("Checking environment setup...")
#     load_dotenv()
#     api_key = os.getenv('OPENAI_API_KEY')
#     if not api_key:
#         print("ERROR: OPENAI_API_KEY not found in .env file!")
#         return
#     else:
#         print("API key found!")

#     # Initialize the manager
#     print("Initializing PDFDocumentManager...")
#     try:
#         manager = PDFDocumentManager()
#         print("Manager initialized successfully!")
#     except Exception as e:
#         print(f"Error initializing manager: {str(e)}")
#         return

#     # Check if PDF exists
#     pdf_path = r"C:\Users\shiva\Downloads\Assignment.pdf"
#     print(f"Checking if PDF exists at: {pdf_path}")
#     if not os.path.exists(pdf_path):
#         print(f"ERROR: PDF not found at {pdf_path}")
#         return
#     else:
#         print("PDF file found!")

#     # Store the PDF with metadata
#     metadata_v1 = {
#         "date": "2023-01-01",
#         "version_tag": "v1.0",
#         "security_tag": "Public"
#     }
    
#     print("Attempting to store PDF...")
#     try:
#         manager.store_pdf(pdf_path, metadata_v1)
#         print("PDF stored successfully!")
#     except Exception as e:
#         print(f"Error storing PDF: {str(e)}")
#         return

#     print("\nAttempting to retrieve documents...")
#     try:
#         results = manager.retrieve_by_date("2023-03-08", security_clearance="Confidential")
#         print(f"Found {len(results)} documents")
        
#         for doc in results[:1]:
#             print("\nDocument details:")
#             print(f"Date: {doc.metadata['date']}")
#             print(f"Version: {doc.metadata['version_tag']}")
#             print(f"Security: {doc.metadata['security_tag']}")
#             print(f"Content preview: {doc.page_content[:100]}...")
#     except Exception as e:
#         print(f"Error retrieving documents: {str(e)}")

# if __name__ == "__main__":
#     main()




