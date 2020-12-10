from api.utils.database import db
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields

class Comments(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    time = db.Column(db.DateTime, server_default=db.func.now())
    comment = db.Column(db.Text)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __init__(self, name, time, comment, post_id=None):
        self.name = name
        self.time = time
        self.comment = comment
        self.post_id = post_id

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

class CommentSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Comments
        sqla_session = db.session
    id = fields.Number(dump_only=True)
    name = fields.String(required=True)
    time = fields.String(dump_only=True)
    comment = fields.String(required=True)
    post_id = fields.Integer()