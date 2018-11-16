from geoalarm.app import db


class Users(db.Model):
    WAIT_LOCATION = 0
    WAIT_LIVE = 1
    TRACING = 2

    id = db.Column(db.Integer, primary_key=True)
    login = db.Column(db.String(80), unique=True, nullable=True)
    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    chat_id = db.Column(db.Integer)
    status = db.Column(db.Integer, default=WAIT_LOCATION)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)

    def __repr__(self):
        return '<User %r>' % self.username

    def get_or_create(self, tg_user):
        self.login = getattr(tg_user, 'username', None)
        if not self.login:
            raise AttributeError

        user = Users.query.filter_by(login=self.login).first()
        return user if user else self.__create(tg_user)

    def set_point(self, lat, lon):
        self.lat, self.lon = lat, lon
        db.session.add(self)
        db.session.commit()

    def set_status(self, status):
        self.status = status
        db.session.add(self)
        db.session.commit()

    def __create(self, tg_user):
        self.login = getattr(tg_user, 'username', None)
        self.first_name = getattr(tg_user, 'first_name', None)
        self.last_name = getattr(tg_user, 'last_name', None)
        self.chat_id = getattr(tg_user, 'id', None)
        if not all([self.login, self.chat_id]):
            raise AttributeError

        db.session.add(self)
        db.session.commit()
        return self
