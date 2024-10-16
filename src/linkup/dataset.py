import json
import logging
import os
import pathlib
from typing import Optional, Union

import requests
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(levelname)s - %(message)s")

PAGES_BASE_URL = "https://www.{site}.fr/wp-json/wp/v2/posts?page={page}&per_page=100"
USER_AGENT = "Mozilla/5.0"


def retrieve_posts(site_name: str, max_pages: int = 10) -> None:
    output_folder = pathlib.Path(os.getenv("OUTPUT_FOLDER", "outputs")) / site_name
    output_folder.mkdir(parents=True, exist_ok=True)

    def loop_cond(a: int) -> bool:
        if max_pages >= 0:
            cond = a < max_pages
        else:
            cond = True
        return cond

    i = 0
    posts_count = 0
    while loop_cond(i):
        i += 1
        page_posts = {}
        posts_data = fetch_page_posts(site_name, i)
        if not posts_data:
            break
        for post_data in posts_data:
            pid, parsed_post = parse_post(post_data)
            page_posts[pid] = parsed_post

        articles_output = output_folder / f"articles_{i}.json"
        articles_output.write_text(json.dumps(page_posts, indent=4))
        posts_count += len(page_posts)

    logging.info(f"Num posts retrieved: {(posts_count)}")


def fetch_page_posts(site_name: str, page: int) -> Optional[list]:
    pages_url = PAGES_BASE_URL.format(site=site_name, page=page)
    try:
        response = requests.get(pages_url, headers={"User-Agent": USER_AGENT})
        response.raise_for_status()
        logging.info(f"Fetched {pages_url}")
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Fetch failed for {pages_url}: {e}")
        return None


def parse_post(post_data: dict) -> Union[str, dict]:
    pid = post_data.get("id")
    date = post_data.get("date")
    link = post_data.get("link")
    category = get_category(post_data.get("class_list", []))
    title = post_data.get("title", {}).get("rendered")

    raw_content = post_data.get("content", {}).get("rendered", "")
    soup = BeautifulSoup(raw_content, "html.parser")
    content = soup.get_text(strip=True)

    return pid, {
        "content": content,
        "title": title,
        "date": date,
        "link": link,
        "category": category,
    }


def get_category(class_list: Union[list[str], dict[str, str]]) -> str:
    cat_section = ""
    if isinstance(class_list, dict):
        for value in class_list.values():
            if "category" in value.lower():
                cat_section = value
                break

    elif isinstance(class_list, list):
        for e in class_list:
            if "category" in e.lower():
                cat_section = e
                break

    return cat_section.split("-")[-1]
