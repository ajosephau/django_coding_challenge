from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from information.models import Person
from information.serializers import PersonWithFoodByTypeSerializer


@api_view(['GET'])
def food_for_person_by_id(request, index):
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
