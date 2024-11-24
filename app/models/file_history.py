from app.models import db 


class FileHistory(db.Model):
    __tablename__ = 'file_history'
    id = db.Column(db.Integer, primary_key=True)
    file_id = db.Column(db.Integer, db.ForeignKey('imported_file.id'), nullable=False)
    uid = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)

    def __repr__(self) -> str:
        return super().__repr__()
    
    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}