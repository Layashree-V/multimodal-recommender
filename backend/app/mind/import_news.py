import pandas as pd


def load_news(path):

    columns = [
        "news_id",
        "category",
        "subcategory",
        "title",
        "abstract",
        "url",
        "title_entities",
        "abstract_entities"
    ]

    df = pd.read_csv(
        path,
        sep="\t",
        names=columns
    )

    return df