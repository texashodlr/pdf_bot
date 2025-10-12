"""
This is a prebuilt PDF and scientific paper setup that looks super functional
     but I'll be building my own implementation.
"""
# pip install grobid-client
# Run the GROBID Server via Docker
# Docker run -it --rm -p 8070:8070 lfoppiano/grobid:latest

from grobid_client.grobid_client import GrobidClient
from lxml import etree

def extract_authors_from_pdf(pdf_path: str, grobid_url: str = "http://localhost:8070") -> list[dict]:
    """
    Returns a list of authors with structured fields:
    [{'given': 'First', 'family': 'Last', 'full': 'First Last', 'affiliations': [...], 'email': '...','orcid':'...'}, ...]
    """
    client = GrobidClient(config={"grobid_server": grobid_url, "batch_size": 1})
    # Ask GROBID to parse only the header (fast, and where authors live)
    tei_xml = client.process_pdf(
        service="processHeaderDocument",
        pdf_file=pdf_path,
        n=1,  # single file
        generateIDs=True,
        consolidate_header=True,   # better normalization/merging
        consolidate_citations=False,
        force=False
    )
    if not tei_xml or not tei_xml[0] or "tei" not in tei_xml[0]:
        return []

    xml = etree.fromstring(tei_xml[0]["tei"].encode("utf-8"))
    ns = {"tei": "http://www.tei-c.org/ns/1.0"}

    authors = []
    for person in xml.xpath(".//tei:teiHeader//tei:fileDesc//tei:sourceDesc//tei:biblStruct//tei:analytic//tei:author", namespaces=ns):
        # Names
        given = "".join(person.xpath(".//tei:forename/text()", namespaces=ns)).strip()
        family = "".join(person.xpath(".//tei:surname/text()", namespaces=ns)).strip()
        full = " ".join([given, family]).strip() or "".join(person.xpath(".//tei:persName//text()", namespaces=ns)).strip()

        # ORCID (if present)
        orcid = "".join(person.xpath(".//tei:idno[@type='orcid']/text()", namespaces=ns)).strip() or None

        # Email (sometimes appears under author or as note)
        email = "".join(person.xpath(".//tei:email/text()", namespaces=ns)).strip() or None

        # Affiliations
        aff_texts = []
        for aff in person.xpath(".//tei:affiliation", namespaces=ns):
            aff_texts.append(" ".join(aff.xpath(".//text()", namespaces=ns)).replace("\n", " ").strip())

        authors.append({
            "given": given or None,
            "family": family or None,
            "full": full or None,
            "affiliations": [a for a in aff_texts if a],
            "email": email,
            "orcid": orcid
        })

    # If analytic/author not present (older layouts), try fallback in header
    if not authors:
        for person in xml.xpath(".//tei:teiHeader//tei:profileDesc//tei:particDesc//tei:listPerson//tei:person", namespaces=ns):
            name = " ".join(person.xpath(".//tei:persName//text()", namespaces=ns)).strip()
            if name:
                authors.append({"given": None, "family": None, "full": name, "affiliations": [], "email": None, "orcid": None})
    return authors