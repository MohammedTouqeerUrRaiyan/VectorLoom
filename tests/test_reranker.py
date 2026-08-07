from src.reranker.rerank_service import RerankService

chunks = [

    {

        "text": "Salesforce is a CRM platform.",

        "document_name": "Salesforce.pdf"

    },

    {

        "text": "Apex is Salesforce programming language.",

        "document_name": "Apex.pdf"

    },

    {

        "text": "Python is a programming language.",

        "document_name": "Python.pdf"

    }

]

results = RerankService.rerank(

    "What is Salesforce?",

    chunks,

    top_k=2

)

for r in results:

    print()

    print(r["document_name"])

    print(r["rerank_score"])