# from rest_framework import status
# import pytest

# # AAA (Arrange, Act, Assert)


# @pytest.fixture
# def create_user(api_client):
#     def do_create_user(user):
#         return api_client.post('/auth/users/', user)
#     return do_create_user


# @pytest.fixture
# def get_user(api_client):
#     def do_get_user(user):
#         api_client.login(username=user.username, password=user.password)
#         return api_client.get(f'/auth/users/{user.id}/')
#     return do_get_user


# @pytest.mark.django_db
# class TestCreateUser:
#     def test_if_data_is_invalid_returns_400(self, create_user):
#         response = create_user({'username': ''})

#         assert response.status_code == status.HTTP_400_BAD_REQUEST
#         assert response.data['username'] is not None

#     def test_if_data_is_valid_returns_201(self, create_user):
#         response = create_user({
#             'username': 'dummyuser',
#             'password': 'ILoveDjango',
#             'email': 'dummy@domain.com'
#         })

#         assert response.status_code == status.HTTP_201_CREATED
#         assert response.data['id'] > 0


# @pytest.mark.django_db
# class TestRetrieveUser:
#     def test_if_user_is_unauthorized_returns_401(self, api_client):
#         response = api_client.get('/auth/users/1/')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_if_user_is_authorized_returns_200(self, authenticate, get_user):
#         user = authenticate()

#         response = get_user(user)

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             'email': user.email,
#             'id': user.id,
#             'username': user.username
#         }

#     def test_if_current_user_is_unauthorized_returns_401(self, api_client):
#         response = api_client.get('/auth/users/me/')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_if_current_user_is_authorized_returns_200(self, authenticate, api_client):
#         user = authenticate()

#         response = api_client.get('/auth/users/me/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             "id": user.id,
#             "username": user.username,
#             "email": user.email,
#             "last_name": user.last_name,
#             "first_name": user.first_name,
#             "middle_initial": user.middle_initial
#         }
