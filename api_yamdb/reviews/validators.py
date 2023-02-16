# from django.core.exceptions import ValidationError


# def validate_score(value):
#     """Валидатор для Review.score."""
#     MIN_SCORE: int = 1
#     MAX_SCORE: int = 10

#     if value not in range(MIN_SCORE, MAX_SCORE + 1):
#         raise ValidationError(
#             f"Оценка {value} вне допустимого диапазона!\n"
#             f"Выберите значение от {MIN_SCORE} до {MAX_SCORE}."
#         )
