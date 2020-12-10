from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.utils import responses as resp
from api.models.posts import Posts, PostSchema
from api.utils.database import db
from flask import jsonify

posts_routes = Blueprint("posts_routes", __name__)
@posts_routes.route('/', methods=['POST'])
def create_post():
    try:
        data = request.get_json()
        post_schema = PostSchema
        posts, error = post_schema.load(data)
        result = post_schema.dump(posts.create()).data
        return response_with(resp.SUCCESS_201, value={"posts":result})
    except Exception as e:
        print (e)
        return response_with(resp.INVALID_INPUT_422)

@posts_routes.route('/', methods=['GET'])
def get_posts():
   fetched = Posts.query.all()
   posts_schema = PostSchema(many=True)
   posts = posts_schema.dump(fetched)
   return response_with(resp.SUCCESS_200, value={"posts":posts})

@posts_routes.route('/images/<int:post_id>', methods=['POST'])
def post_image(post_id):
    try:
        file = request.files['image']
        get_posts = Posts.query.get_or_404(post_id)
        if file and allowed_file(file.content_type):
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        get_posts.image = url_for('uploaded_file', filename= filename, _external=True)
        db.session.add(get_posts)
        db.session.commit()
        posts_schema = PostSchema
        posts = posts_schema.dump(get_posts)
        return response_with(resp.SECCESS_200, value={"posts":posts})
    except Exception as e:
        print (e)
        return response_with(resp.INVALID_INPUT_422)