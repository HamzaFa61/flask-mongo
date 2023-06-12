from mongoengine import *
from application.models.post import Post


class TextPost(Post):
    content = StringField()

    def to_dict(self):
        return {
            'id': str(self.id),  # convert ObjectId to string
            'title': self.title,
            'author': self.author.to_dict(),
            'tags': self.tags,
            'comments': self.comments,
            'content': self.content
        }
