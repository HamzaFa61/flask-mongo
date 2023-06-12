from mongoengine import *


class Comment(EmbeddedDocument):
    content = StringField()
    name = StringField(max_length=120)

    def to_dict(self):
        return {
            'id': str(self.id),  # convert ObjectId to string
            'content': self.content,
            'name': self.name
        }
