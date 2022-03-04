# -*- coding: utf-8 -*-
from typing import Any, Dict

from django.db.models.query import QuerySet
from rest_framework import serializers

from information.models import Company, Food, Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["name"]


class PersonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ["name", "age", "address", "phone"]


class MutualFriendsDetailSerializer(serializers.BaseSerializer):
    def to_representation(self, instance: Person) -> Dict[str, Any]:
        person_one = self.context["person_one"]
        person_two = self.context["person_two"]
        mutual_friends = self.context["mutual_friends"]
        return {
            "person_one": PersonDetailSerializer(person_one).data,
            "person_two": PersonDetailSerializer(person_two).data,
            "mutual_friends": [
                PersonSerializer(person).data for person in mutual_friends
            ],
        }


class CompanySerializer(serializers.ModelSerializer):
    employees = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ["name", "employees"]


class PersonWithFoodByTypeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    fruits = serializers.SerializerMethodField()
    vegetables = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ["username", "age", "fruits", "vegetables"]

    @staticmethod
    def get_username(person: Person) -> str:
        return person.name

    def get_fruits(self, person: Person) -> QuerySet:
        return self.get_food_by_type(person, type=Food.FRUIT)

    def get_vegetables(self, person: Person) -> QuerySet:
        return self.get_food_by_type(person, type=Food.VEGETABLE)

    @staticmethod
    def get_food_by_type(person: Person, type: str) -> QuerySet:
        return person.favourite_foods.filter(type=type).values_list("name", flat=True)


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ["name"]
