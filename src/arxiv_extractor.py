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
from pyvis.network import Network
import webbrowser
from pathlib import Path
import time
from collections import defaultdict
from typing import Dict, List, Iterable
import argparse


def authors_from_arxiv_id(arxiv_ids: List[str]) -> Dict[str, List[tuple[str,str]]]:
    """
    This method, given a collection of arxiv paper IDs, returns a dict.
    The return dict 'new_researchers_dict' has authors (keys): values (paper title and arxiv ID)
    example {'Joe Blow': ("Bananas and You", 9902.12345)}
    """
    client = arxiv.Client()
    search = arxiv.Search(id_list=arxiv_ids)
    out: Dict[str, List[tuple[str,str]]] = defaultdict(list)
    tic = time.perf_counter()
    for r in client.results(search):
        
        title = (r.title or "").strip()
        arxiv_id = (r.entry_id or "").split("/abs/")[-1]
        tup = (arxiv_id, title)
        for a in r.authors:
            name = getattr(a, "name", None)
            if name and tup not in out[name]:
                out[name].append(tup)
    toc = time.perf_counter()
    print(f"Paper and authors found in {toc-tic:0.4f} seconds")
    print('+'*50)
    return dict(out)

def author_paper_network(author_index, html_path="author_paper_network.html"):
    net = Network(height="800px", width="100%", bgcolor="#111", font_color="#eee",
                  notebook=False, directed=False)
    net.barnes_hut()

    for author, papers in author_index.items():
        net.add_node(
            f"a::{author}",
            label=author,
            title=f"Author: {author}",
            shape="dot",
            color="#4fc3f7",
            size=16
        )
        for arxiv_id, title in papers:
            pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            pid = f"p::{arxiv_id}"
            tooltip = f"""{title}<br><i>{arxiv_id}</i><br>
                          <a href="{pdf_url}" target="_blank" rel="noopener">Open PDF</a>"""
            net.add_node(
                pid,
                label=arxiv_id,
                title= tooltip, #f"{title}<br><i>{arxiv_id}</i>",
                shape="box",
                color="#ffcc80",
                size=12
            )
            net.add_edge(f"a::{author}", pid, color="#888", width=1)

    # Use the non-notebook template explicitly
    out = Path(html_path).resolve()
    net.write_html(str(out), open_browser=False, notebook=False)
    webbrowser.open_new_tab(out.as_uri())

def create_network():
    test_id_list = ["2412.16720","2410.21276", "2406.04093", "2312.09390", "2303.08774", "2303.01469"]
    researchers_dict = authors_from_arxiv_id(test_id_list)
    for k in researchers_dict:
        print(f"Author: {k}, {researchers_dict[k]}\n")
    author_paper_network(researchers_dict)

def main(extraction_tool: int):
    match extraction_tool:
        case 1:
            return create_network()
        case 2:
            print("Apple")
        case _:
            print("Orange")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Arxiv Knowledge and Influencer Mapper')
    parser.add_argument('extraction_tool', type=int, default=1, help='The tool you want to use')
    args = parser.parse_args()
    main(args.extraction_tool)


"""

General Test Cases:
test_id = "2510.04871"
test_id = "2509.26217"
CPUs: test_id_list = ["2508.03016", "2506.23025", "2506.09758", "2509.25853", "2509.21271", "2509.12232", "2508.20653", "2508.10481", "2509.26217"]
AI: test_id_list = ["2412.16720","2410.21276", "2406.04093", "2312.09390", "2303.08774", "2303.01469"]

"""