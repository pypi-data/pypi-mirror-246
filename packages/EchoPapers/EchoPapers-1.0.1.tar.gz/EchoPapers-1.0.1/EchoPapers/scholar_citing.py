#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# @created: 14.12.2023
# @author: Aleksey Komissarov
# @contact: ad3002@gmail.com

import argparse
import logging
import os

from EchoReaper import iter_page_sources

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Extend dataset with formated citations."
    )
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        help="Input tsv file from parser stage",
        required=True,
    )
    parser.add_argument("-o", "--output", type=str, help="Output folder", required=True)

    args = parser.parse_args()

    input_file = args.input
    output_folder = args.output

    use_proxy = True
    headless = False
    stop_on_captcha = True

    url2cid = {}
    urls = []
    url2folder = {}

    with open(input_file, "r") as file:
        for line in file:
            d = line.strip().split("\t")
            if d:
                if not "https" in d[-1]:
                    continue
                urls.append(d[-1])
                data_cid = d[0]
                url2cid[d[-1]] = data_cid
                url2folder[d[-1]] = output_folder

    for ii, (url, source) in enumerate(
        iter_page_sources(
            urls,
            verbose=True,
            use_proxy=use_proxy,
            minimum_size=0,
            has_token="",
            headless=headless,
            timeout=10,
            stop_on_captcha=stop_on_captcha,
        )
    ):
        logging.info(f"Source size: {len(source)}, {ii}/{len(urls)}")
        output_folder = url2folder[url]
        if not os.path.isdir(output_folder):
            os.makedirs(output_folder)
        item_id = url2cid[url]
        output_file = os.path.join(output_folder, f"{item_id}.html")
        with open(output_file, "w") as file:
            file.write(source)
