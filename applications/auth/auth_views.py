from django.http import JsonResponse
import logging
import json
from app_config.settings.database import SessionLocal
from applications.auth.auth_models import ClientUser


logger= logging.getLogger('django')


# Registration route
def register(request):
    """
    Handles user registration requests.
    :param request:
    :return:
    """
    if request.method!= 'POST':
        logger.error('Request method invalid!')
        return JsonResponse({
            'error':'Invalid request method!'
        }, status=405)

    session= SessionLocal()
    try:
        try:
            data= json.loads(request.body)
        except json.JSONDecodeError:
            logger.error('Invalid JSON data!')
            return JsonResponse({
                'error':'Invalid JSON!'
            }, status=400)

        first_name= data.get('first_name')
        last_name= data.get('last_name')
        email= data.get('email')
        password= data.get('password')

        if not all([first_name, last_name, email, password]):
            return JsonResponse({
                'error':'Some required fields are empty!'
            }, status=400)


        user= session.query(ClientUser).filter_by(email=email).first()
        if user:
            return JsonResponse({
                'error':'User with this email already exists!'
            }, status=400)

        new_user= ClientUser(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=password,
        )

        session.add(new_user)
        session.commit()

        logger.info(f'Registration successful! User: {new_user.first_name} {new_user.last_name}')
        return JsonResponse({
            'message':f'Registration successful! New user: {new_user}'
        }, status=201)

    except Exception as exc:
        logger.error(f'An unexpected error occurred: {str(exc)}')
        return JsonResponse({
            'error':'An internal error occurred during user registration. Please try again later.'
        }, status=500)

    finally:
        session.close()