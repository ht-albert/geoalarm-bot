from geoalarm.app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    chat_id = db.Column(db.Integer)

    def __repr__(self):
        return '<User %r>' % self.username

    def get_or_create(self, tg_user):
        login = getattr(tg_user, 'username', None)

        if not login:
            return

        user = User.query.filter_by(login=login).first()

        return user if user else self.__create(tg_user)

    @classmethod
    def __create(cls, tg_user):
        cls.login = getattr(tg_user, 'username', None)
        cls.first_name = getattr(tg_user, 'first_name', None)
        cls.last_name = getattr(tg_user, 'last_name', None)
        cls.chat_id = getattr(tg_user, 'chat_id', None)


if __name__ == '__main__':
    db.create_all()