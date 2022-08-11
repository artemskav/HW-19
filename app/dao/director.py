from app.dao.model.director import Director

class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, did):
        """ Возврат директоров по id """
        return self.session.query(Director).get(did)

    def get_all(self):
        """ Возврат всех записей директоров """
        return self.session.query(Director).all()

    def create(self, data):
        """ Внесение в список директора фильма """
        new_director = Director(**data)
        self.session.add(new_director)
        self.session.commit()
        return new_director

    def update(self, update_director):
        """ Обновление данных директора """

        self.session.add(update_director)
        self.session.commit()

        return update_director

    def delete(self, did):
        """ Удаление димректора из списка по id """
        director = self.session.query(Director).filter(Director.id == did).first()
        if not director:
            return "", 404
        self.session.delete(director)
        self.session.commit()
        return "", 204
