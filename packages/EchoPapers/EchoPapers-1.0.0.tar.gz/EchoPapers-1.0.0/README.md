# EchoPapers
EchoPapers: Discover and analyze the impact of academic papers through citation tracking and advanced analytics

## Introduction

EchoPapers is a powerful tool designed to discover and analyze the impact of academic papers. It achieves this through advanced citation tracking and analytics. With EchoPapers, researchers, students, and academics can gain valuable insights into the reach and influence of various academic papers. This can aid in literature reviews, research direction, and understanding the progression of thought in a particular field. 

The tool leverages Python scripts to scrape data from Google Scholar, parse the information, and provide a comprehensive analysis of the citation data. This includes `scholar_citing.py` for handling citation data, `scholar_parser.py` for parsing research paper information, and `scholar_scraper.py` for scraping data from Google Scholar.

Stay tuned for more updates and features that will enhance your academic research experience.

To use tools you need working proxy. You can use [Webshare](https://www.webshare.io/?referral_code=85dooepk9q5o) proxy service. It's free in the basic plan and easy to use.

## Installation

```bash
pip install EchoRepear

git clone https://github.com/ad3002/EchoPapers.git
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