# -*- coding: utf-8 -*-
# fmt: off
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from information.models import Company, Person
from information.serializers import (CompanySerializer,
                                     MutualFriendsDetailSerializer,
                                     PersonWithFoodByTypeSerializer)

# fmt: on


@api_view(["GET"])
def company_by_index(request, index):
    """
    Given a company, the API needs to return all their employees.
    Returns an empty list if a company doesn't have any employees.
    """
    try:
        company = Company.objects.get(index=index)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def mutual_friends_alive_with_brown_eyes(request, person_one_index, person_two_index):
    """
    Given 2 people, returns their information (Name, Age, Address, phone) and the list of their
    friends in common which have brown eyes and are still alive.
    """
    try:
        person_one = Person.objects.get(index=person_one_index)
        person_two = Person.objects.get(index=person_two_index)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        mutual_friends = Person.objects.alive_mutual_friends_brown_eyes(
            person_one, person_two
        )
        serializer = MutualFriendsDetailSerializer(
            person_one,
            context={
                "person_one": person_one,
                "person_two": person_two,
                "mutual_friends": mutual_friends,
            },
        )
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def food_for_person_by_index(request, index):
    """
    Given 1 person, returns a list of fruits and vegetables they like.
    """
    try:
        person = Person.objects.get(index=index)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = PersonWithFoodByTypeSerializer(person)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
