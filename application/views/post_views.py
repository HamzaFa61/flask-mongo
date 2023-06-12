from flask import Blueprint, request, Response
from json import dumps
from application.models.post import Post
from application.models.text_post import TextPost
from application.models.image_post import ImagePost
from application.models.link_post import LinkPost
from application.models.user import User
from application.models.tag import Tag
from application.models.comment import Comment
from application.shared.constants import POST_TYPES

post_blueprint = Blueprint('post_blueprint', __name__)


@post_blueprint.route('/post/create/<post_type>', methods=['POST'])
def create_post(post_type: str):
    """
    Create a new post of a specific type.

    Endpoint: /post/create/<post_type>
    Method: POST

    Parameters:
    - post_type (str): Type of the post. Allowed values: 'text', 'image', 'link'.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - post (dict): Post details if created successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Post created successfully",
        "post": {
            "title": "Example Post",
            "content": "Lorem ipsum dolor sit amet.",
            "author": "john.doe@example.com",
            "post_type": "text"
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        data: dict = request.get_json()

        if post_type not in POST_TYPES:
            raise Exception('Invalid post type')

        if post_type == 'text':
            post: TextPost = TextPost(
                title=data['title'],
                content=data['content'],
                author=User.objects(email=data['author']).first()
            ).save()

        elif post_type == 'image':
            post: ImagePost = ImagePost(
                title=data['title'],
                image_path=data['image_path'],
                author=User.objects(email=data['author']).first()
            ).save()

        elif post_type == 'link':
            post: LinkPost = LinkPost(
                title=data['title'],
                link_url=data['link_url'],
                author=User.objects(email=data['author']).first()
            ).save()
        response = {
            'message': 'Post created successfully',
            'post': post.to_dict(),
            'status': 'success',
            'status_code': 200
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')


@post_blueprint.route('/post/list', methods=['GET'])
def list_posts():
    """
    List all posts.

    Endpoint: /post/list
    Method: GET

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - posts (list): List of posts.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Posts listed successfully",
        "posts": [
            {
                "title": "Example Post",
                "content": "Lorem ipsum dolor sit amet.",
                "author": "John Doe",
                "post_type": "text"
            },
            {
                "title": "Example Post",
                "image_path": "/path/to/image.jpg",
                "author": "John Doe",
                "post_type": "image"
            }
        ],
        "status": "success",
        "status_code": 200
    }
    """
    try:
        posts: list = []
        for post in Post.objects:
            posts.append(post.to_dict())
        response = {
            'message': 'Posts listed successfully',
            'posts': posts,
            'status': 'success',
            'status_code': 200
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')


@post_blueprint.route('/post/list/<post_type>', methods=['GET'])
def list_posts_by_type(post_type: str):
    """
    List all posts of a specific type.

    Endpoint: /post/list/<post_type>
    Method: GET

    Parameters:
    - post_type (str): Type of the post. Allowed values: 'text', 'image', 'link'.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - posts (list): List of posts.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Posts listed successfully",
        "posts": [
            {
                "title": "Example Post",
                "content": "Lorem ipsum dolor sit amet.",
                "author": "John Doe",
                "post_type": "text"
            },
            {
                "title": "Example Post",
                "image_path": "/path/to/image.jpg",
                "author": "John Doe",
                "post_type": "image"
            }
        ],
        "status": "success",
        "status_code": 200
    }
    """
    try:
        posts: list = []

        if post_type not in POST_TYPES:
            raise Exception('Invalid post type')

        if post_type == 'text':
            for post in TextPost.objects:
                posts.append(post.to_dict())

        elif post_type == 'image':
            for post in ImagePost.objects:
                posts.append(post.to_dict())

        elif post_type == 'link':
            for post in LinkPost.objects:
                posts.append(post.to_dict())

        response = {
            'message': 'Posts listed successfully',
            'posts': posts,
            'status': 'success',
            'status_code': 200
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')


@post_blueprint.route('/post/update/<post_id>', methods=['PUT'])
def update_post(post_id: str):
    """
    Update an existing post.

    Endpoint: /post/update/<post_id>
    Method: PUT

    Parameters:
    - post_id (str): ID of the post to be updated.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - post (dict): Updated post details if updated successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Post updated successfully",
        "post": {
            "title": "Updated Post",
            "content": "New content",
            "author": "john.doe@example.com",
            "post_type": "text"
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        data: dict = request.get_json()

        post = Post.objects(id=post_id).first()
        if not post:
            raise Exception('Post not found')

        if 'title' in data:
            post.title = data['title']
        if 'content' in data and isinstance(post, TextPost):
            post.content = data['content']
        if 'image_path' in data and isinstance(post, ImagePost):
            post.image_path = data['image_path']
        if 'link_url' in data and isinstance(post, LinkPost):
            post.link_url = data['link_url']
        if 'author' in data:
            post.author = User.objects(email=data['author']).first()

        post.save()

        response = {
            'message': 'Post updated successfully',
            'post': post.to_dict(),
            'status': 'success',
            'status_code': 200
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')


@post_blueprint.route('/post/delete/<post_id>', methods=['DELETE'])
def delete_post(post_id: str):
    """
    Delete an existing post.

    Endpoint: /post/delete/<post_id>
    Method: DELETE

    Parameters:
    - post_id (str): ID of the post to be deleted.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - post (dict): Deleted post details if deleted successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Post deleted successfully",
        "post": {
            "title": "Example Post",
            "content": "Lorem ipsum dolor sit amet.",
            "author": "John Doe",
            "post_type": "text"
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        post = Post.objects(id=post_id).first()
        if not post:
            raise Exception('Post not found')

        post.delete()

        response = {
            'message': 'Post deleted successfully',
            'post': post.to_dict(),
            'status': 'success',
            'status_code': 200
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')


@post_blueprint.route('/post/add_tag/<post_id>/<tag_id>', methods=['PUT'])
def add_tag_to_post(post_id: str, tag_id: str):
    """
    Add a tag to a post.

    Endpoint: /post/add_tag/<post_id>/<tag_id>
    Method: PUT

    Parameters:
    - post_id (str): ID of the post.
    - tag_id (str): ID of the tag to be added.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - post (dict): Post details if tag added successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Tag added successfully",
        "post": {
            "title": "Example Post",
            "tags": [
                {
                    "name": "Example Tag"
                }
            ]
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        post = Post.objects(id=post_id).first()
        if not post:
            raise Exception('Post not found')

        tag = Tag.objects(id=tag_id).first()
        if not tag:
            raise Exception('Tag not found')

        post.tags.append(tag)
        post.save()

        response = {
            'message': 'Tag added successfully',
            'post': post.to_dict(),
            'status': 'success',
            'status_code': 200
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')


@post_blueprint.route('/post/remove_tag/<post_id>/<tag_id>', methods=['PUT'])
def remove_tag_from_post(post_id: str, tag_id: str):
    """
    Remove a tag from a post.

    Endpoint: /post/remove_tag/<post_id>/<tag_id>
    Method: PUT

    Parameters:
    - post_id (str): ID of the post.
    - tag_id (str): ID of the tag to be removed.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - post (dict): Post details if tag removed successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Tag removed successfully",
        "post": {
            "title": "Example Post",
            "tags": []
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        post = Post.objects(id=post_id).first()
        if not post:
            raise Exception('Post not found')

        tag = Tag.objects(id=tag_id).first()
        if not tag:
            raise Exception('Tag not found')

        post.tags.remove(tag)
        post.save()

        response = {
            'message': 'Tag removed successfully',
            'post': post.to_dict(),
            'status': 'success',
            'status_code': 200
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')


@post_blueprint.route('/post/add_comment/<post_id>', methods=['POST'])
def add_comment_to_post(post_id: str):
    """
    Add a comment to a post.

    Endpoint: /post/add_comment/<post_id>
    Method: POST

    Parameters:
    - post_id (str): ID of the post.

    Body:
    - name (str): Name of the commenter.
    - email (str): Email of the commenter.
    - body (str): Body of the comment.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - post (dict): Post details if comment added successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Comment added successfully",
        "post": {
            "title": "Example Post",
            "comments": [
                {
                    "name": "Example Commenter",
                    "email": "johndoe@exampleemail.com",
                    "body": "Example comment body"
                }
            ]
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        post = Post.objects(id=post_id).first()
        if not post:
            raise Exception('Post not found')

        comment = Comment(**request.json)
        post.comments.append(comment)
        post.save()

        response = {
            'message': 'Comment added successfully',
            'post': post.to_dict(),
            'status': 'success',
            'status_code': 200
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')


@post_blueprint.route('/post/remove_comment/<post_id>/<comment_id>', methods=['DELETE'])
def remove_comment_from_post(post_id: str, comment_id: str):
    """
    Remove a comment from a post.

    Endpoint: /post/remove_comment/<post_id>/<comment_id>
    Method: DELETE

    Parameters:
    - post_id (str): ID of the post.
    - comment_id (str): ID of the comment to be removed.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - post (dict): Post details if comment removed successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Comment removed successfully",
        "post": {
            "title": "Example Post",
            "comments": []
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        post = Post.objects(id=post_id).first()
        if not post:
            raise Exception('Post not found')

        comment = Comment.objects(id=comment_id).first()
        if not comment:
            raise Exception('Comment not found')

        post.comments.remove(comment)
        post.save()

        response = {
            'message': 'Comment removed successfully',
            'post': post.to_dict(),
            'status': 'success',
            'status_code': 200
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')
