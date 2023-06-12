from flask import (
    Blueprint,
    Response,
    request,
)
from application.models.tag import Tag
from json import dumps

tag_blueprint = Blueprint('tag_blueprint', __name__)


@tag_blueprint.route('/tag/create', methods=['POST'])
def create_tag():
    """
    Create a new tag.

    Endpoint: /tag/create
    Method: POST

    Parameters:
    - name (str): Name of the tag.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - tag (dict): Created tag details if created successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (201 for success, 500 for error).

    Example:
    {
        "message": "Tag created successfully",
        "tag": {
            "name": "Example Tag"
        },
        "status": "success",
        "status_code": 201
    }
    """
    try:
        data: dict = request.get_json()

        if 'name' not in data:
            raise Exception('Tag name not provided')

        tag = Tag(name=data['name'])
        tag.save()

        response = {
            'message': 'Tag created successfully',
            'tag': tag.to_dict(),
            'status': 'success',
            'status_code': 201
        }
    except Exception as e:
        response = {
            'message': str(e),
            'status': 'error',
            'status_code': 500
        }
    return Response(response=dumps(response), status=response['status_code'], mimetype='application/json')


@tag_blueprint.route('/tag/list', methods=['GET'])
def list_tags():
    """
    List all tags.

    Endpoint: /tag/list
    Method: GET

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - tags (list): List of tags.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Tags listed successfully",
        "tags": [
            {
                "name": "Example Tag"
            }
        ],
        "status": "success",
        "status_code": 200
    }
    """
    try:
        tags = []
        for tag in Tag.objects:
            tags.append(tag.to_dict())

        response = {
            'message': 'Tags listed successfully',
            'tags': tags,
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


@tag_blueprint.route('/tag/update/<tag_id>', methods=['PUT'])
def update_tag(tag_id: str):
    """
    Update an existing tag.

    Endpoint: /tag/update/<tag_id>
    Method: PUT

    Parameters:
    - tag_id (str): ID of the tag to be updated.
    - name (str): New name of the tag.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - tag (dict): Updated tag details if updated successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Tag updated successfully",
        "tag": {
            "name": "Updated Tag"
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        data: dict = request.get_json()

        tag = Tag.objects(id=tag_id).first()
        if not tag:
            raise Exception('Tag not found')

        if 'name' in data:
            tag.name = data['name']

        tag.save()

        response = {
            'message': 'Tag updated successfully',
            'tag': tag.to_dict(),
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


@tag_blueprint.route('/tag/delete/<tag_id>', methods=['DELETE'])
def delete_tag(tag_id: str):
    """
    Delete an existing tag.

    Endpoint: /tag/delete/<tag_id>
    Method: DELETE

    Parameters:
    - tag_id (str): ID of the tag to be deleted.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - tag (dict): Deleted tag details if deleted successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "Tag deleted successfully",
        "tag": {
            "name": "Example Tag"
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        tag = Tag.objects(id=tag_id).first()
        if not tag:
            raise Exception('Tag not found')

        tag.delete()

        response = {
            'message': 'Tag deleted successfully',
            'tag': tag.to_dict(),
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
