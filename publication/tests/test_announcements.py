# from model_bakery import baker
# from rest_framework import status
# import pytest
# from publication.models import Announcement


# @pytest.mark.django_db
# class TestRetrieveAnnouncement:
#     def test_get_announcement_list_returns_200(self, api_client):
#         response = api_client.get('/publication/announcements/')

#         assert response.status_code == status.HTTP_200_OK

#     def test_get_announcement_detail_returns_200(self, api_client):
#         announcement = baker.make(Announcement)

#         response = api_client.get(
#             f'/publication/announcements/{announcement.id}/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             "id": announcement.id,
#             "announcement_img": None,
#             "member": announcement.member.id,
#             "date_created": announcement.date_created.isoformat().replace('+00:00', 'Z')
#         }
