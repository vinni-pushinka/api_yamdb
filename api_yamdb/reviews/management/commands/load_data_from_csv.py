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


def obj_from_id(model, id):
    return model.objects.get(pk=id)


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
            open(
                f"{settings.BASE_DIR}/static/data/category.csv",
                encoding="utf8",
            )
        ):
            category = Category(
                id=row["id"], name=row["name"], slug=row["slug"]
            )
            category.save()
        for row in DictReader(
            open(f"{settings.BASE_DIR}/static/data/genre.csv", encoding="utf8")
        ):
            genre = Genre(id=row["id"], name=row["name"], slug=row["slug"])
            genre.save()
        for row in DictReader(
            open(
                f"{settings.BASE_DIR}/static/data/titles.csv", encoding="utf8"
            )
        ):
            titles = Title(
                id=row["id"],
                name=row["name"],
                year=row["year"],
                category=obj_from_id(Category, row["category"]),
            )
            titles.save()
        for row in DictReader(
            open(
                f"{settings.BASE_DIR}/static/data/genre_title.csv",
                encoding="utf8",
            )
        ):
            genre_title = GenreTitle(
                id=row["id"],
                title=obj_from_id(Title, row["title_id"]),
                genre=obj_from_id(Genre, row["genre_id"]),
            )
            genre_title.save()
        for row in DictReader(
            open(
                f"{settings.BASE_DIR}/static/data/review.csv", encoding="utf8"
            )
        ):
            review = Review(
                id=row["id"],
                title=obj_from_id(Title, row["title_id"]),
                text=row["text"],
                author=obj_from_id(User, row["author"]),
                score=row["score"],
                pub_date=row["pub_date"],
            )
            review.save()
        for row in DictReader(
            open(
                f"{settings.BASE_DIR}/static/data/comments.csv",
                encoding="utf8",
            )
        ):
            comments = Comment(
                id=row["id"],
                review=obj_from_id(Review, row["review_id"]),
                text=row["text"],
                author=obj_from_id(User, row["author"]),
                pub_date=row["pub_date"],
            )
            comments.save()
