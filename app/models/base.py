from app import db


class BaseModel(db.Model):

    __abstract__ = True

    def save(self):
        """
        Save a model instance
        """

        db.session.add(self)
        db.session.commit()

    def delete(self):
        """
        Deletes a model instance
        """
        db.session.delete(self)
        db.session.commit()
