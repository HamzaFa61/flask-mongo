from mongoengine import *
from application.models.post import Post


class ImagePost(Post):
    image_path = StringField()

    def to_dict(self):
        return {
            'id': str(self.id),  # convert ObjectId to string
            'title': self.title,
            'author': self.author.to_dict(),
            'tags': self.tags,
            'comments': self.comments,
            'image_path': self.image_path
        }
