from flask import Blueprint, request, Response
from json import dumps
from application.models.user import User

user_blueprint = Blueprint('user_blueprint', __name__)


@user_blueprint.route('/user/create', methods=['POST'])
def create_user():
    """
    Create a new user.

    Endpoint: /user/create
    Method: POST

    Parameters:
    - email (str): Email of the user.
    - first_name (str): First name of the user.
    - last_name (str): Last name of the user.

    Returns:
    A JSON response containing the following fields:
    - message (str): Success or error message.
    - user (dict): User details if created successfully.
    - status (str): Status of the operation ('success' or 'error').
    - status_code (int): HTTP status code (200 for success, 500 for error).

    Example:
    {
        "message": "User created successfully",
        "user": {
            "email": "john.doe@example.com",
            "first_name": "John",
            "last_name": "Doe"
        },
        "status": "success",
        "status_code": 200
    }
    """
    try:
        data: dict = request.get_json()
        user: User = User(
            email=data['email'],
            first_name=data['first_name'],
            last_name=data['last_name']
        ).save()
        response = {
            'message': 'User created successfully',
            'user': user.to_dict(),
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
