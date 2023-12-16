# EchoPapers
EchoPapers: Discover and analyze the impact of academic papers through citation tracking and advanced analytics

## Introduction

EchoPapers is a powerful tool designed to discover and analyze the impact of academic papers. It achieves this through advanced citation tracking and analytics. With EchoPapers, researchers, students, and academics can gain valuable insights into the reach and influence of various academic papers. This can aid in literature reviews, research direction, and understanding the progression of thought in a particular field. 

The tool leverages Python scripts to scrape data from Google Scholar, parse the information, and provide a comprehensive analysis of the citation data. This includes `scholar_citing.py` for handling citation data, `scholar_parser.py` for parsing research paper information, and `scholar_scraper.py` for scraping data from Google Scholar.

Stay tuned for more updates and features that will enhance your academic research experience.

To use tools you need working proxy. You can use [Webshare](https://www.webshare.io/?referral_code=85dooepk9q5o) proxy service. It's free in the basic plan and easy to use.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install EchoPaper.

```bash
pip install EchoPaper
```

Or you can install from source:

```
git clone https://github.com/ad3002/EchoPaper.git
cd EchoPaper
python setup.py install
```

## Usage

```bash
cd EchoPapers/EchoPapers

python3 scholar_scraper.py python3.11 scholar_scraper.py -i 3632164375966858166 -o ~/cases/repeatscout -t genomes -p user:password@127.0.0.1:8279 -s 2017 -e 2018

python3 scholar_parser.py -i ~/cases/repeatscout -o ~/cases/repeatscout.tsv

python3 scholar_citing.py -i ~/cases/repeatscout.tsv -o ~/cases/repeatscout_citing
```

Don't use without proxy. Google will ban you by IP address.

If you see a captcha, you need to solve it manually. After that, the script will continue to work when you press Enter twice in command line.

## Dataset description

The dataset contains the following fields:

1. `data_cid`: A unique identifier for the research paper.
2. `title`: The title of the research paper.
3. `authors`: The authors of the research paper.
4. `journal`: The journal in which the research paper was published.
5. `year`: The year the research paper was published.
6. `publication_info`: Additional publication information.
7. `summary`: A summary of the research paper.
8. `citation_count`: The number of times the research paper has been cited.
9. `related_articles_url`: A URL to related articles.
10. `all_versions_url`: A URL to all versions of the research paper.
11. `id2author`: A mapping of author IDs to author names.
12. `full_link`: A link to the full text of the research paper.
13. `pdf_link`: A link to a PDF version of the research paper.
14. `html_link`: A link to an HTML version of the research paper.
15. `citation_url`: A URL to the citations of the research paper.
16. `cite_link`: A link to cite the research paper.