from rest_framework import serializers

from information.models import Person, Food, Company


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name']


class PersonDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['name', 'age', 'address', 'phone']


class MutualFriendsDetailSerializer(serializers.BaseSerializer):
    def to_representation(self, instance):
        person_one = self.context['person_one']
        person_two = self.context['person_two']
        mutual_friends = self.context['mutual_friends']
        return {
            'person_one': PersonDetailSerializer(person_one).data,
            'person_two': PersonDetailSerializer(person_two).data,
            'mutual_friends': [PersonSerializer(person).data for person in mutual_friends],
        }

class CompanySerializer(serializers.ModelSerializer):
    employees = PersonSerializer(many=True, read_only=True)

    class Meta:
        model = Company
        fields = ['name', 'employees']


class PersonWithFoodByTypeSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    fruits = serializers.SerializerMethodField()
    vegetables = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['username', 'age', 'fruits', 'vegetables']

    @staticmethod
    def get_username(person):
        return person.name

    def get_fruits(self, person):
        return self.get_food_by_type(person, type=Food.FRUIT)

    def get_vegetables(self, person):
        return self.get_food_by_type(person, type=Food.VEGETABLE)

    @staticmethod
    def get_food_by_type(person, type):
        return [food.name for food in person.favourite_foods.filter(type=type)]


class FoodSerializer(serializers.ModelSerializer):
    class Meta:
        model = Food
        fields = ['name']