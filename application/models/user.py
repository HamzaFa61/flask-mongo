from mongoengine import *


class User(Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

    def to_dict(self):
        return {
            'id': str(self.id),  # convert ObjectId to string
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name
        }
