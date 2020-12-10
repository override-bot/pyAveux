from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from api.models.comments import CommentSchema

class Posts(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    createdAt = db.Column(db.DateTime, server_default=db.func.now())
    category = db.Column(db.String(100))
    post = db.Column(db.Text)
    image = db.Column(db.String(100), nullable=True)
    comments = db.relationship('Comments', backref='Posts', cascade="all, delete-orphan")

    def __init__(self, name, createdAt, category, post, comments=[]):
        self.name = name
        self.createdAt = createdAt
        self.category = category
        self.post = post
        self.image = image
        self.comments = comments
    
    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class PostSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Posts
        sqla_session = db.session
    
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    createdAt = fields.String(dump_only=True)
    category = fields.String(required=True)
    posts = fields.String(required=True)
    image = fields.String(dump_only=True)
    comments = fields.Nested(CommentSchema, many=True, only=['name', 'time', 'comment', 'id'])
