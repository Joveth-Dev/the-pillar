# from model_bakery import baker
# from rest_framework import status
# import pytest
# from publication.models import Article


# @pytest.mark.django_db
# class TestRetrieveArticle:
#     def test_get_article_list_returns_200(self, api_client):
#         response = api_client.get('/publication/articles/')

#         assert response.status_code == status.HTTP_200_OK

#     def test_get_article_detail_returns_200(self, api_client):
#         article = baker.make(Article, is_approved=True)

#         response = api_client.get(f'/publication/articles/{article.id}/')

#         assert response.status_code == status.HTTP_200_OK
#         assert response.data == {
#             "id": article.id,
#             "author": article.member.user.get_full_name(),
#             "pen_name": article.member.pen_name,
#             "issue": article.issue,
#             "category": article.category,
#             "title_or_headline": article.title_or_headline,
#             "article_images": [],
#             "body": article.body,
#             "date_published": None,
#             "date_updated": article.date_updated.isoformat().replace('+00:00', 'Z')
#         }
