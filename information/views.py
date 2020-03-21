from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from information.models import Person, Company
from information.serializers import PersonWithFoodByTypeSerializer, CompanySerializer


@api_view(['GET'])
def company_by_index(request, index):
    '''
    Given a company, the API needs to return all their employees.
    Provide an empty list if a company doesn't have any employees.
    '''
    try:
        company = Company.objects.get(index=index)
    except Company.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CompanySerializer(company)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def food_for_person_by_index(request, index):
    '''
    Given 1 person, returns a list of fruits and vegetables they like.
    '''
    try:
        person = Person.objects.get(index=index)
    except Person.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = PersonWithFoodByTypeSerializer(person)
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
