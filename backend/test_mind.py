from app.mind.import_news import load_news

df = load_news("datasets/MIND/news.tsv")

print(df.head())

print(df.shape)