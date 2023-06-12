from mongoengine import *
from application.models.post import Post


class Tag(Document):
    name = StringField(max_length=120, required=True)
    posts = ListField(ReferenceField(Post, reverse_delete_rule=CASCADE))

    def to_dict(self):
        return {
            'id': str(self.id),  # convert ObjectId to string
            'name': self.name,
            'posts': self.posts
        }
