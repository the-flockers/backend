from flask import request
from app.api.v1 import api_v1
from app.models.news import NewsArticle
from app.utils.responses import success, error


@api_v1.route("/news", methods=["GET"])
def get_news():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    pagination = (
        NewsArticle.query
        .filter_by(is_published=True)
        .order_by(NewsArticle.published_at.desc())
        .paginate(page=page, per_page=per_page, error_out=False)
    )

    return success({
        "articles": [a.to_dict() for a in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "current_page": page,
    })


@api_v1.route("/news/<int:article_id>", methods=["GET"])
def get_news_article(article_id):
    article = NewsArticle.query.filter_by(id=article_id, is_published=True).first_or_404()
    return success(article.to_dict())
