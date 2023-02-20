from csv import DictReader
from django.conf import settings
from django.core.management import BaseCommand

from reviews.models import (
    Category,
    Comment,
    Genre,
    GenreTitle,
    Review,
    Title,
    User,
)


# def get_path(file_name):
#     return f'{settings.BASE_DIR}/static/data/{file_name}.csv'


class Command(BaseCommand):
    help = "load people from csv"

    def handle(self, *args, **options):
        for row in DictReader(
            open(f"{settings.BASE_DIR}/static/data/users.csv", encoding="utf8")
        ):
            users = User(
                id=row["id"],
                username=row["username"],
                email=row["email"],
                role=row["role"],
                bio=row["bio"],
                first_name=row["first_name"],
                last_name=row["last_name"],
            )
            users.save()
        for row in DictReader(
            open("static/data/category.csv", encoding="utf8")
        ):
            category = Category(
                id=row["id"], name=row["name"], slug=row["slug"]
            )
            category.save()
        for row in DictReader(open("static/data/genre.csv", encoding="utf8")):
            genre = Genre(id=row["id"], name=row["name"], slug=row["slug"])
            genre.save()
        for row in DictReader(open("static/data/titles.csv", encoding="utf8")):
            titles = Title(
                id=row["id"],
                name=row["name"],
                year=row["year"],
                category=row["category"],
            )
            titles.save()
        for row in DictReader(
            open("static/data/genre_title.csv", encoding="utf8")
        ):
            genre_title = GenreTitle(
                id=row["id"],
                title_id=row["title_id"],
                genre_id=row["genre_id"],
            )
            genre_title.save()
        for row in DictReader(open("static/data/review.csv", encoding="utf8")):
            review = Review(
                id=row["id"],
                title=row["title_id"],
                text=row["text"],
                author=row["author"],
                score=["score"],
                pub_date=["pub_date"],
            )
            review.save()
        for row in DictReader(
            open("static/data/comments.csv", encoding="utf8")
        ):
            comments = Comment(
                id=row["id"],
                review=row["review_id"],
                text=row["text"],
                author=row["author"],
                pub_date=["pub_date"],
            )
            comments.save()
