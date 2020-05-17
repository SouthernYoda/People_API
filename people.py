from flask import make_response, abort
from config import db
from models import Person, PersonSchema


def read_all():
    """
    This function responds to a request for /api/people
    with the complete lists of people
    :return:        json string of list of people
    """
    people = Person.query.order_by(Person.lname).all()

    person_schema = PersonSchema(many=True)
    data = person_schema.dump(people)
    return data

def read_one(person_id):
    """
    This function responds to a request for /api/people/{lname}
    with one matching person from people
    :param lname:   last name of person to find
    :return:        person matching last name
    """
    person = Person.query.filter(Person.person_id == person_id).one_or_none()
    # Does the person exist in people?
    if person is not None:

        # Serialize the data for the response
        person_schema = PersonSchema()
        return person_schema.dump(person)

    # otherwise, nope not found
    else:
        abort(
            404, "Person with last name {lname} not found".format(lname=lname)
        )

def create(person):
    """
    This function creates a new person in the people structure
    based on the passed in person data
    :param person:  person to create in people structure
    :return:        201 on success, 406 on person exists
    """
    fname = person.get("fname")
    lname = person.get("lname")

    print(f"fname = {fname} and lname= {lname}")

    existing_person = (Person.query.filter(Person.fname == fname).filter(Person.lname == lname).one_or_none())

    print(f"The exising person is {existing_person}")
    print(f"Person object is {person}")

    # Can we insert this person?
    if existing_person is None:


        # Create a person instance using the schema and the passed-in person
        schema = PersonSchema()
        new_person = schema.load(person, session=db.session)

        # Add the person to the database
        db.session.add(new_person)
        db.session.commit()

        # Serialize and return the newly created person in the response
        data = schema.dump(new_person)

        return data, 201
    else:
        abort(409, f'Person {fname} {lname} exists in the data')

def update(person_id, person):
    """
    This function updates an existing person in the people structure
    :param person_id:   last name of person to update in the people structure
    :param person:  person to update
    :return:        updated person structure
    """
    # Get the person requested from the db into session
    update_person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Try to find an existing person with the sname name
    fname = person.get("fname")
    lname = person.get("lname")

    existing_person = (
        Person.query.filter(Person.fname == fname).filter(Person.lname == lname).one_or_none()
    )

    # Are we trying to find a person that does not exist?
    if update_person is None:
        abort(
            404, "Person not found for Id: {person_id}".format(person_id),
        )
    # Would our update create a duplicate of another person already existing?
    elif existing_person is not None and existing_person.person_id != person_id:
        abort (
        409, "Person {fname} {lname} exists already.".format(fname, lname)
        )
    # otherwise go ahead and update
    else:
        # Turn the passed in person into a db object
        schema = PersonSchema()
        update = schema.load(person, session=db.session)

        # Set the id to the person we want to update
        update.person_id = update_person.person_id

        # Merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # Return updated person in the response
        data = schema.dump(update_person)

        return data, 200

def delete(person_id):
    """
    This function deletes a person from the people structure
    :param lname:   last name of person to delete
    :return:        200 on successful delete, 404 if not found
    """
    # Get the person requested
    person = Person.query.filter(Person.person_id == person_id).one_or_none()

    # Did we find a person?
    if person is not None:
        db.session.delete(person)
        db.session.commit()
        return make_response(
            "Person {person_id} deleted".format(person_id=person_id), 200
        )
    else:
        abort(
            404,
            "Person not found for Id: {person_id}".format(person_id=person_id)
        )
