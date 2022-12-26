# from model_bakery import baker
# from rest_framework import status
# import pytest
# from university.models import College


# @pytest.mark.django_db
# class TestRetrieveCollege:
#     def test_get_college_list_returns_200(self, api_client):
#         response = api_client.get('/university/colleges/')

#         assert response.status_code == status.HTTP_200_OK

#     def test_get_college_detail_returns_200(self, api_client):
#         college = baker.make(College)

#         response = api_client.get(f'/university/colleges/{college.id}/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             "id": college.id,
#             "title": college.title,
#             "courses_offered": 0
#         }
