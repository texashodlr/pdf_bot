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
import time
client = arxiv.Client()

def authors_from_arxiv_id(arxiv_ids: list[str]) -> list[str]:
    """
    This method, given a collection of arxiv paper IDs, returns a dict.
    The return dict 'new_researchers_dict' has authors (keys): values (paper title and arxiv ID)
    example {'Joe Blow': ("Bananas and You", 9902.12345)}
    
    """
    new_researchers_dict = {}
    print(f"Initiating paper search for these IDs...\n{arxiv_ids}\n")
    print('+'*50)
    for arxiv_id in arxiv_ids:
        print(f"Paper ID: {arxiv_id}\n")
        tic = time.perf_counter()
        paper_id = arxiv.Search(id_list=[arxiv_id])
        paper_id_results = next(client.results(paper_id))
        paper_title = str(paper_id_results.title)
        paper_authors = [a.name for a in paper_id_results.authors]
        toc = time.perf_counter()
        # print(f"Paper found: {paper_id} !")
        # print(f"\tPaper title: {paper_title}\n")
        # print(f"\tPaper authors: {paper_authors}\n")
        print(f"Paper and authors found in {toc-tic:0.4f} seconds")
        print('+'*50)
        for paper_author in paper_authors:
            new_researchers_dict[paper_author] = (arxiv_id, paper_title)
        #return [a for a in paper_id_results.authors]
    #print(f"Printing return dict...\n\n{new_researchers_dict}")
    return new_researchers_dict


# test_id = "2510.04871"
# test_id = "2509.26217"
test_id_list = ["2509.25853", "2509.21271", "2509.12232", "2508.20653", "2508.10481", "2509.26217"]
researchers_dict = authors_from_arxiv_id(test_id_list)