# from model_bakery import baker
# from rest_framework import status
# import pytest
# from university.models import Student


# @pytest.mark.django_db
# class TestRetrieveStudent:
#     def test_if_user_is_unauthorized_student_returns_401(self, api_client):
#         response = api_client.get('/university/students/me/')

#         assert response.status_code == status.HTTP_401_UNAUTHORIZED

#     def test_if_user_is_authorized_student_returns_200(self, authenticate, api_client):
#         user = authenticate()
#         student = baker.make(Student, profile=user.profile)

#         response = api_client.get('/university/students/me/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             'id': student.id,
#             'profile_id': student.profile.id,
#             'student_id': student.student_id,
#             'full_name': ',  None.',
#             'college': student.college,
#             'degree_program': student.college
#         }
