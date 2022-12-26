# from model_bakery import baker
# from rest_framework import status
# import pytest
# from university.models import DegreeProgram


# @pytest.mark.django_db
# class TestRetrieveDegreeProgram:
#     def test_get_degree_programs_list_returns_200(self, api_client):
#         response = api_client.get('/university/degree_programs/')

#         assert response.status_code == status.HTTP_200_OK

#     def test_get_degree_programs_detail_returns_200(self, api_client):
#         degree_program = baker.make(DegreeProgram)

#         response = api_client.get(
#             f'/university/degree_programs/{degree_program.id}/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             "id": degree_program.id,
#             "title": degree_program.title,
#             "college_name": degree_program.college.title
#         }
