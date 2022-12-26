# from model_bakery import baker
# from rest_framework import status
# import pytest


# @pytest.mark.django_db
# class TestRetrieveProfile:
#     def test_if_user_is_unauthorized_profile_returns_401(self, api_client):
#         response = api_client.get('/userprofile/profiles/me/')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_if_user_is_authorized_profile_returns_200(self, authenticate, api_client):
#         user = authenticate()

#         response = api_client.get('/userprofile/profiles/me/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             "id": user.profile.id,
#             "user_id": user.id,
#             "profile_image": user.profile.profile_image,
#             "birth_date": user.profile.birth_date,
#             "sex": user.profile.sex,
#             "city": user.profile.city,
#             "state_or_province": user.profile.state_or_province,
#             "zip_code": user.profile.zip_code,
#             "country": user.profile.country,
#             "is_student": user.profile.is_student
#         }
