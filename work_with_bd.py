from bd import DB


class WorkWithDB:

    def __init__(self):
        self.db = DB()

    def get_dish(self, dish):
        request = ('SELECT * FROM cookforcardendb.dishes '
                   f'WHERE nameDish =  {dish};')
        return self.db.make_request(request)

    def get_id_dish(self, dish):
        request = ('SELECT id FROM cookforcardendb.dishes '
                   f'WHERE nameDish =  {dish};')
        return self.db.make_request(request)

    def get_dishes(self):
        request = 'SELECT * FROM cookforcardendb.dishes '
        return self.db.make_request(request)

    def post_dish(self, nameDish, compound, recipe):
        request = ("INSERT INTO cookforcardendb.dishes "
                   "(nameDish, compound, recipe, datecreate, datechange) "
                   f"VALUES('{nameDish}', '{compound}', '{recipe}', now(), now());")
        return self.db.make_request(request)

    def get_count_one_porion(self, dish):
        request = ("SELECT id, countCompound, Dishes_id, datacreate, datechange "
                   "FROM cookforcardendb.countforone where Dishes_id =  "
                   f"(SELECT id FROM cookforcardendb.dishes where nameDish='{dish}');")
        return self.db.make_request(request)

    def post_count_one_portion(self, dish, portion):
        request = ("INSERT INTO cookforcardendb.countforone (countCompound, Dishes_id, datacreate, datechange) "
                   "VALUES("
                   f"'{portion}', (SELECT id FROM cookforcardendb.dishes where nameDish='{dish}'), now(), now());")
        return self.db.make_request(request)

    def post_count_pepole(self, count_people, dish):
        request = ("INSERT INTO cookforcardendb.historydish (countPeople, datecreate, Dishes_id) "
                   f"VALUES({count_people}, now(), (SELECT id FROM cookforcardendb.dishes where nameDish='{dish}')); ")
        return self.db.make_request(request)


if __name__ == '__main__':
    try:
        db = WorkWithDB()
        data = db.post_count_one_portion('2', '22')
        r = db.get_dishes()
        print(r)
    finally:
        db.db.close
