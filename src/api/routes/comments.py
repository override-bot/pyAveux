from flask import Blueprint, request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.comments import Comments, CommentSchema
from api.utils.database import db

comment_routes= Blueprint("comment_routes", __name__)

@comment_routes.route('/', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        comment_schema = CommentSchema
        comment, error = comment_schema.load(data)
        result = comment_schema.dump(comment.create()).data
        return response_with(resp.SUCCESS_201, value={"comment":result})
    except Exception as e:
        print (e)
        return response_with(resp.INVALID_INPUT_422)
        
@comment_routes.route('/', methods=['GET'])
def get_comments():
    fetched = Comments.query.all()
    comment_schema = CommentSchema(many=True)
    comments = comment_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={"comments":comments})