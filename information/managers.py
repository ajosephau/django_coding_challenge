# -*- coding: utf-8 -*-
from typing import TYPE_CHECKING

from django.db import models
from django.db.models.query import QuerySet

if TYPE_CHECKING:
    from .models import Person


class PersonManager(models.Manager):
    def alive_mutual_friends_brown_eyes(
        self, person_one: "Person", person_two: "Person"
    ) -> QuerySet:
        return (person_one.friends.all() & person_two.friends.all()).filter(
            has_died=False, eye_colour="brown"
        )
