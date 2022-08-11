from app.dao.model.user import User

class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        """ Возврат юзера по id """
        user = self.session.query(User).filter(User.id == uid).first()
        if user is None:
            return "", 404

        return user  #self.session.query(User).filter(User.id == uid).one()

    def get_username(self, username):
        """ Возврат юзера по имени """
        user = self.session.query(User.username, User.password, User.role).filter(User.username == username).first()
        if user is None:
            return "", 404

        return user  #self.session.query(User).filter(User.id == uid).one()


    def get_all(self):
        """ Возврат юзеров """
        return self.session.query(User).all()

    def create(self, data):
        """ Внесение в список нового юзера """
        new_user = User(**data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def update(self, update_user):
        """ Обновление данных по юзеру """
        self.session.add(update_user)
        self.session.commit()
        return update_user

    def delete(self, uid):
        """ Удаление юзера из списка по id """
        user = self.session.query(User).filter(User.id == uid).first()
        if not user:
            return "", 404
        self.session.delete(user)
        self.session.commit()
