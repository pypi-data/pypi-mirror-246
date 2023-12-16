#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @created: 14.12.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

import argparse
import csv
import logging
import os
import re
from dataclasses import asdict, dataclass

from bs4 import BeautifulSoup


@dataclass
class ResearchPaper:
    data_cid: str
    title: str
    authors: list
    journal: str
    year: str
    publication_info: str
    summary: str
    citation_count: int
    related_articles_url: str
    all_versions_url: str
    id2author: dict
    full_link: str = None
    pdf_link: str = None
    html_link: str = None
    citation_url: str = None
    cite_link: str = None


# Function to parse the HTML data
def parse_research_paper(html_data: str) -> ResearchPaper:
    page = BeautifulSoup(html_data, "html.parser")

    for soup in page.find_all("div", class_=["gs_r", "gs_or", "gs_scl"]):
        if not soup.find("h3", class_="gs_rt"):
            continue

        data_cid = soup["data-cid"]

        # Extract title
        title = soup.find("h3", class_="gs_rt").get_text()

        # Extract authors
        authors_ = [
            (a.get("href").split("user=")[1].split("&")[0], a.get_text())
            for a in soup.find_all("div", class_="gs_a")[0].find_all("a")
        ]
        id2author = {href: name for href, name in authors_}
        gs_a = soup.find("div", class_="gs_a").get_text().replace("\xa0", " ")

        authors = gs_a.split("-")[0]
        publication_info = "-".join(gs_a.split("-")[1:])
        authors = [x.strip() for x in authors.split(",") if x.strip()]

        # Extract publication info
        if "-" in publication_info:
            journal = publication_info.split("-")[-2].strip()
            year = journal.split(", ")[-1]
            journal = ", ".join(journal.split(", ")[:-1])

            journal = journal.strip()
            year = year.strip()
            publication_info = publication_info.split("-")[-1].strip()
        else:
            journal = None
            year = None
            publication_info = publication_info.strip()

        # Extract summary
        summary = soup.find("div", class_="gs_rs").get_text()

        # Extract citation count
        citation_url = soup.find("a", string=re.compile("Cited by"))
        citation_count = 0
        if citation_url:
            citation_url = citation_url["href"]
            citation_text = soup.find("a", string=re.compile("Cited by")).get_text()
            citation_count = int(re.search(r"\d+", citation_text).group())

        # Extract URLs for related articles and all versions
        related_articles_url = soup.find("a", string="Related articles")
        if related_articles_url:
            related_articles_url = related_articles_url["href"]
        all_versions_url = soup.find("a", string=re.compile(r"All \d+ version."))
        if all_versions_url:
            all_versions_url = all_versions_url["href"]

        # Extract URLs for full text, PDF, and HTML
        pdf_link = None
        html_link = None
        full_link = None
        cite_link = f"https://scholar.google.com/scholar?q=info:{data_cid}:scholar.google.com/&output=cite&scirp=1&hl=en"
        for a in soup.find_all("a"):
            if "[PDF]" in a.get_text():
                pdf_link = a["href"]
            if "[HTML]" in a.get_text():
                html_link = a["href"]
            if "Full View" in a.get_text():
                full_link = a["href"]

        yield ResearchPaper(
            data_cid,
            title,
            authors,
            journal,
            year,
            publication_info,
            summary,
            citation_count,
            related_articles_url,
            all_versions_url,
            id2author,
            full_link,
            pdf_link,
            html_link,
            citation_url,
            cite_link,
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse downloaded scholar articles.")
    parser.add_argument("-i", "--input", type=str, help="Input folder", required=True)
    parser.add_argument("-o", "--output", type=str, help="Output file", required=True)

    args = parser.parse_args()

    input_folder = args.input
    output_file = args.output

    dataset = []

    parsed_ids = set()

    for root, dirs, files in os.walk(input_folder):
        logging.info(f"Processing {root}")
        for file_path in files:
            file_path = os.path.join(root, file_path)

            if file_path.endswith(".html"):
                with open(file_path, "r") as file:
                    html_data = file.read()
                for research_paper in parse_research_paper(html_data):
                    if research_paper.data_cid not in parsed_ids:
                        parsed_ids.add(research_paper.data_cid)
                    else:
                        continue
                    dataset.append(research_paper)

    with open(output_file, "w") as fh:
        fieldnames = list(asdict(dataset[0]).keys())
        writer = csv.DictWriter(fh, fieldnames=fieldnames, delimiter="\t")

        writer.writeheader()

        for article in dataset:
            writer.writerow(asdict(article))
