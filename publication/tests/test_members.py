# from model_bakery import baker
# from rest_framework import status
# import pytest
# from publication.models import Member


# @pytest.mark.django_db
# class TestRetrieveMember:
#     def test_get_member_list(self, api_client):
#         response = api_client.get('/publication/members/')

#         assert response.status_code == status.HTTP_200_OK

#     def test_get_member_detail(self, api_client):
#         member = baker.make(Member, pen_name='dummy')

#         response = api_client.get(f'/publication/members/{member.id}/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             'id': member.id,
#             'profile': '',
#             'full_name': ',  None.',
#             'pen_name': member.pen_name,
#             'current_position': None
#         }
