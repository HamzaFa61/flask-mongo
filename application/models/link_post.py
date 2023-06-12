from mongoengine import *
from application.models.post import Post


class LinkPost(Post):
    link_url = StringField()

    def to_dict(self):
        return {
            'id': str(self.id),  # convert ObjectId to string
            'title': self.title,
            'author': self.author.to_dict(),
            'tags': self.tags,
            'comments': self.comments,
            'link_url': self.link_url
        }
