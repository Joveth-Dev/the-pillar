# from model_bakery import baker
# from rest_framework import status
# import pytest
# from publication.models import Issue


# @pytest.mark.django_db
# class TestRetrieveIssue:
#     def test_get_issue_list_returns_200(self, api_client):
#         response = api_client.get('/publication/issues/')

#         assert response.status_code == status.HTTP_200_OK

#     def test_get_issue_detail_returns_200(self, api_client):
#         issue = baker.make(Issue, is_approved=True)

#         response = api_client.get(f'/publication/issues/{issue.id}/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             'id': issue.id,
#             'volume_number': issue.volume_number,
#             'issue_number': issue.issue_number,
#             'category': issue.category,
#             'issue_file': None,
#             'description': None,
#             'articles_count': 0,
#             'date_published': None,
#             'date_updated': issue.date_updated.isoformat().replace('+00:00', 'Z')
#         }
