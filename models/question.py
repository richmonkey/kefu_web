# -*- coding: utf-8 -*-
class Question(object):
    @classmethod
    def add(self, db, question, answer, store_id):
        sql = "INSERT INTO `question`(question, answer, store_id) VALUES(%s, %s, %s)"
        r = db.execute(sql, (question, answer, store_id))
        return r.lastrowid


    @classmethod
    def get_question_count(cls, db, store_id):
        sql = "SELECT count(*) as count FROM question WHERE store_id=%s"
        r = db.execute(sql, store_id)
        obj = r.fetchone()
        return obj['count']

    @classmethod
    def get_page_question(cls, db, store_id, offset, limit):
        sql = "SELECT id, question, answer FROM question WHERE store_id=%s LIMIT %s, %s"
        r = db.execute(sql, (store_id, offset, limit))
        return list(r.fetchall())
