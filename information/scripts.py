from decimal import Decimal

import dateutil.parser

from information.models import Company, Food, Tag, Person


def import_company_json(company_json_obj):
    """
    Imports a list of company JSON objects as specified by the Paranuara government
    """

    issue_list = []
    num_companies_created = 0

    if not isinstance(company_json_obj, list):
        raise TypeError("Requires a list input")

    for company in company_json_obj:
        index = company.get('index')
        name = company.get('company')
        if not index and not (index == 0):
            issue_list.append(f"Company: {company} missing 'index' key.")
        elif not name:
            issue_list.append(f"Company: {company} missing 'company' key.")
        else:
            if Company.objects.filter(index=index, name=name).exists():
                issue_list.append(f"Company: {company} already exists.")
            else:
                Company.objects.create(index=index, name=name)
                num_companies_created += 1

    return issue_list, num_companies_created


def import_people_json(people_json_obj):
    """
    Imports a list of people JSON objects as specified by the Paranuara government
    """

    issue_list = []
    num_people_created = 0

    if not isinstance(people_json_obj, list):
        raise TypeError("Requires a list input")

    friend_dict = {}

    for person in people_json_obj:
        index = person.get('index')
        name = person.get('name')
        id = person.get('_id')
        guid = person.get('guid')
        has_died = person.get('has_died')
        balance = person.get('balance')
        picture = person.get('picture')
        age = person.get('age')
        eye_color = person.get('eyeColor')
        gender = person.get('gender')
        company_id = person.get('company_id')
        email = person.get('email')
        phone = person.get('phone')
        address = person.get('address')
        about = person.get('about')
        registered = person.get('registered')
        greeting = person.get('greeting')
        tags = person.get('tags')
        friends = person.get('friends')
        favouriteFood = person.get('favouriteFood')
        if not index and not (index == 0):
            issue_list.append(f"Person: {person} missing 'index' key.")
        elif not name:
            issue_list.append(f"Company: {person} missing 'company' key.")
        elif not id:
            issue_list.append(f"Company: {person} missing 'id' key.")
        elif not guid:
            issue_list.append(f"Company: {person} missing 'guid' key.")
        elif not balance:
            issue_list.append(f"Company: {person} missing 'balance' key.")
        elif not picture:
            issue_list.append(f"Company: {person} missing 'picture' key.")
        elif not age:
            issue_list.append(f"Company: {person} missing 'age' key.")
        elif not eye_color:
            issue_list.append(f"Company: {person} missing 'eye_color' key.")
        elif not gender:
            issue_list.append(f"Company: {person} missing 'gender' key.")
        elif not company_id:
            issue_list.append(f"Company: {person} missing 'company_id' key.")
        elif not email:
            issue_list.append(f"Company: {person} missing 'email' key.")
        elif not phone:
            issue_list.append(f"Company: {person} missing 'phone' key.")
        elif not address:
            issue_list.append(f"Company: {person} missing 'address' key.")
        elif not about:
            issue_list.append(f"Company: {person} missing 'about' key.")
        elif not registered:
            issue_list.append(f"Company: {person} missing 'registered' key.")
        elif not greeting:
            issue_list.append(f"Company: {person} missing 'greeting' key.")
        elif not tags:
            issue_list.append(f"Company: {person} missing 'tags' key.")
        elif not friends:
            issue_list.append(f"Company: {person} missing 'friends' key.")
        elif not favouriteFood:
            issue_list.append(f"Company: {person} missing 'favouriteFood' key.")
        else:
            if Person.objects.filter(index=index).exists():
                issue_list.append(f"Person: {person} already exists.")
            else:
                balance_decimal = Decimal(balance.replace('$', '').replace(',', ''))
                if gender == 'male':
                    gender_as_enum = Person.MALE
                elif gender == 'female':
                    gender_as_enum = Person.FEMALE
                else:
                    gender_as_enum = Person.NOT_SPECIFIED

                company = Company.objects.get(index=(company_id - 1))

                person = Person.objects.create(index=index,
                                               name=name,
                                               id=id,
                                               guid=guid,
                                               has_died=has_died,
                                               balance=balance_decimal,
                                               picture=picture,
                                               age=age,
                                               eye_colour=eye_color,
                                               gender=gender_as_enum,
                                               email=email,
                                               phone_number=phone,
                                               address=address,
                                               about=about,
                                               registered=dateutil.parser.parse(registered),
                                               company=company
                                               )

                friend_dict[index] = friends

                # create tags links
                for tag in tags:
                    tag_obj, created = Tag.objects.get_or_create(name=tag)
                    person.tags.add(tag_obj)
                    person.save()

                # create food links
                for food in favouriteFood:
                    if food in ["apple","banana","orange","strawberry"]:
                        type = Food.FRUIT
                    elif food in ["beetroot","carrot","celery","cucumber"]:
                        type = Food.VEGETABLE
                    else:
                        raise RuntimeError(f"Cannot classify {food} as {Food.TYPE_CHOICES}")
                    food_obj, created = Food.objects.get_or_create(name=food, type=type)
                    person.favourite_foods.add(food_obj)
                    person.save()

                num_people_created += 1

    # populate friends link now that all people are saved.
    for person_index in friend_dict.keys():
        person = Person.objects.get(index=person_index)
        for friend_index in friend_dict[person_index]:
            friend = Person.objects.get(index=friend_index['index'])
            person.friends.add(friend)
            person.save()

    return issue_list, num_people_created
