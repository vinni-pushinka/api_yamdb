from csv import DictReader

from django.conf import settings
from django.core.management import BaseCommand
from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)

TABLES = {
    User: "users.csv",
    Category: "category.csv",
    Genre: "genre.csv",
    Title: "titles.csv",
    Review: "review.csv",
    Comment: "comments.csv",
    GenreTitle: "genre_title.csv",
}


class Command(BaseCommand):
    """Служебная команда для загрузки данных в базу из csv."""

    help = "Load data from csv"

    def handle(self, *args, **kwargs):
        for model in TABLES:
            with open(
                f"{settings.BASE_DIR}/static/data/" + TABLES[model],
                newline="",
                encoding="utf8",
            ) as csv_file:
                objs = []
                for row in DictReader(csv_file):
                    for field in ("category", "author"):
                        if field in row:
                            row[f"{field}_id"] = row[field]
                            del row[field]
                    objs.append(model(**row))
                model.objects.bulk_create(objs)
