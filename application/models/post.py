from mongoengine import *
from application.models.user import User
from application.models.comment import Comment


class Post(Document):
    title = StringField(max_length=120, required=True)
    author = ReferenceField(User, reverse_delete_rule=CASCADE)
    tags = ListField(StringField(max_length=30))
    comments = ListField(EmbeddedDocumentField(Comment))

    meta = {'allow_inheritance': True}

    def to_dict(self):
        return {
            'id': str(self.id),  # convert ObjectId to string
            'title': self.title,
            'author': self.author.to_dict(),
            'tags': self.tags,
            'comments': self.comments
        }
