from app.models import db 


class ImportedFile(db.Model):
    __tablename__ = 'imported_file'
    id = db.Column(db.Integer, primary_key=True)
    f_name = db.Column(db.String, nullable=False)
    size = db.Column(db.Integer, nullable=False)

    history_relation = db.relationship('FileHistory', backref='imported_file', lazy=True)

    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}