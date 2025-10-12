"""
Extractor.py

Input: Scientific Paper (PDF)
Output: Authors, Ideas, References (Authors and Papers)
    -> Authors should likely live in a database 
        as they're a key in a sense with the values being the titles of the papers they're connected to.
Documentation: https://info.arxiv.org/help/arxiv_identifier.html
               https://pypi.org/project/arxiv/
"""
import arxiv
client = arxiv.Client()

def authors_from_arxiv_id(arxiv_id: str) -> list[str]:
    #paper = next(arxiv.Client(id_list=[arxiv_id]).results())
    print("Initiating paper search...")
    paper_id = arxiv.Search(id_list=[arxiv_id])
    print(f"Paper found: {paper_id} !")
    paper_id_results = next(client.results(paper_id))
    print(f"Paper title: {paper_id_results.title} !")
    return [a.name for a in paper_id_results.authors]


# test_id = "2510.04871"
test_id = "2509.26217"
print(authors_from_arxiv_id(test_id))