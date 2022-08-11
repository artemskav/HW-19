from app.dao.model.genre import Genre

class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, gid):
        """ Возврат жанров по id """
        return self.session.query(Genre).filter(Genre.id == gid).one()

    def get_all(self):
        """ Возврат всех жанров """
        return self.session.query(Genre).all()

    def create(self, data):
        """ Внесение в список жанра фильма """
        new_genre = Genre(**data)
        self.session.add(new_genre)
        self.session.commit()
        return new_genre

    def update(self, update_genre):
        """ Обновление данных директора """

        self.session.add(update_genre)
        self.session.commit()

        return update_genre

    def delete(self, did):
        """ Удаление димректора из списка по id """
        genre = self.session.query(Genre).filter(Genre.id == did).first()
        if not genre:
            return "", 404
        self.session.delete(genre)
        self.session.commit()
        return "Ok", 204
