from linkup import dataset


def test_get_category():
    assert dataset.get_category(["category-news"]) == "news"
    assert dataset.get_category({"some-key": "class-category-people"}) == "people"
    assert dataset.get_category({}) == ""


def test_parse_post():
    post_data = {
        "id": "1",
        "date": "2024-12-12",
        "link": "http://www.public.fr/posts/1",
        "class_list": ["stuff", "category-news"],
        "title": {"rendered": "First news of the day"},
        "content": {"rendered": "<p>This is the first new of the day.</p>"},
    }
    pid, parsed_post = dataset.parse_post(post_data)

    assert pid == "1"
    assert parsed_post["title"] == "First news of the day"
    assert parsed_post["date"] == "2024-12-12"
    assert parsed_post["link"] == "http://www.public.fr/posts/1"
    assert parsed_post["category"] == "news"
    assert parsed_post["content"] == "This is the first new of the day."
