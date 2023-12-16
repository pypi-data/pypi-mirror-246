#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @created: 14.12.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

import argparse
import logging
import os
import random
import re
import string

from EchoReaper import iter_page_sources
from sympy import N

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrap scholar article citations.")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Article id that should be analyzed",
        required=True,
    )
    parser.add_argument("-o", "--output", type=str, help="Output folder", required=True)
    parser.add_argument("-p", "--proxy", type=str, help="Proxy string", default=None)
    parser.add_argument(
        "-t",
        "--token",
        type=str,
        help="Token to check scrapping. It should be present in the page source. It should be part of paper title",
        required=True,
    )
    parser.add_argument("-s", "--start_year", type=int, help="Start year", default=None)
    parser.add_argument("-e", "--end_year", type=int, help="End year", default=None)

    args = parser.parse_args()
    input_id = args.input
    output_folder = args.output
    has_token = args.token
    def_proxy = args.proxy
    start_year = args.start_year
    end_year = args.end_year

    use_proxy = True
    headless = False
    stop_on_captcha = True
    stop_no_token = '<b style="display:block;margin-left:53px">Next</b>'
    max_pages = 20
    max_papers = 1000
    output_folder_prefix = "google%s"
    output_folder_prefix = "trseeker%s"

    starting_url = (
        "https://scholar.google.com/scholar?hl=en&as_sdt=2005&cites=%s&scipsc=&num=%s"
        % (input_id, max_pages)
    )

    if start_year:
        starting_url += "&as_ylo=%s" % start_year
    if end_year:
        starting_url += "&as_yhi=%s" % end_year

    url2folder = {}
    urls = []

    url = starting_url + "&start=%s"

    for i in range(0, max_papers, max_pages):
        urls.append(url % i)
        url2folder[url % i] = output_folder

    prefix = "".join(
        random.choice(string.ascii_lowercase + string.digits) for _ in range(5)
    )

    for ii, (url, source) in enumerate(
        iter_page_sources(
            urls,
            verbose=True,
            use_proxy=use_proxy,
            def_proxy=def_proxy,
            minimum_size=0,
            has_token=has_token,
            headless=headless,
            timeout=10,
            stop_on_captcha=stop_on_captcha,
        )
    ):
        logging.info(f"Source size: {len(source)}, {ii}/{len(urls)}")
        output_folder = url2folder[url]
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)
        item_id = url.split("=")[-1]
        output_file = os.path.join(output_folder, f"{prefix}_{item_id}.html")
        with open(output_file, "w") as file:
            file.write(source)
        if not stop_no_token in source:
            logging.info("No more results")
            break
