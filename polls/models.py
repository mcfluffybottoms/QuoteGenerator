from django.db import models
from django.core.exceptions import ValidationError
import random
from django.db.models import Sum


class Quote(models.Model):
    source = models.CharField(
        max_length=255, db_index=True, default="Unknown"
    )  # use db_index for faster lookup
    text = models.TextField(default="Unknown")
    weight = models.PositiveSmallIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return (
            f'"{self.text} -- {self.source}\n'
            f"Просмотры: {self.views}, лайки: {self.likes}, дизлайки: {self.dislikes}\n"
            f"Вес: {self.weight}"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["source", "text"], name="unique_source_text"
            )
        ]

    @classmethod
    def create(cls, source, text, weight):
        count = Quote.objects.filter(source=source).count()
        if count >= 3:
            raise ValidationError(
                f'Источник "{source}" не может иметь больше трех цитат.'
            )
        obj = cls(source=source, text=text, weight=weight)
        obj.clean_save()
        return obj

    def clean_save(self):
        self.full_clean()
        self.save()

    @staticmethod
    def increment_view(quote_id):
        Quote.objects.filter(id=quote_id).update(views=models.F("views") + 1)

    @staticmethod
    def like_quote(quote_id):
        Quote.objects.filter(id=quote_id).update(likes=models.F("likes") + 1)

    @staticmethod
    def dislike_quote(quote_id):
        Quote.objects.filter(id=quote_id).update(dislikes=models.F("dislikes") + 1)

    @staticmethod
    def set_weight(quote_id, weight):
        Quote.objects.filter(id=quote_id).update(weight=weight)

    @staticmethod
    def get_random_quote():
        total_weight = Quote.objects.all().aggregate(total=Sum("weight"))["total"]
        if not total_weight:
            return None
        r = random.randint(1, total_weight)
        cumulative = 0  # TODO: maybe remove for cycle since it's pretty slow
        for quote in Quote.objects.all():
            cumulative += quote.weight
            if cumulative >= r:
                return quote

    @staticmethod
    def get_top_quotes(order_by, num=10):
        quotes = Quote.objects.order_by(order_by)[:num]
        return quotes
