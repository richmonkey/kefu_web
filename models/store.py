# -*- coding: utf-8 -*-
import logging

class Store(object):
    @classmethod
    def set_store_name(cls, rds, store_id, name):
        key = "stores_%d"%store_id
        rds.hset(key, "name", name)

    @classmethod
    def create_store(cls, db, name, group_id, developer_id):
        sql = "INSERT INTO store(name, group_id, developer_id) VALUES(%s, %s, %s)"
        r = db.execute(sql, (name, group_id, developer_id))
        store_id = r.lastrowid
        db.commit()
        return store_id

    @classmethod
    def delete_store(cls, db, store_id, group_id):
        db.begin()

        sql = "DELETE FROM `group` WHERE id=%s"
        r = db.execute(sql, group_id)
        logging.debug("rows:%s", r.rowcount)

        sql = "DELETE FROM group_member WHERE group_id=%s"
        r = db.execute(sql, group_id)
        logging.debug("delete group rows:%s", r.rowcount)

        sql = "DELETE FROM store WHERE id=%s"
        r = db.execute(sql, store_id)
        logging.debug("delete store rows:%s", r.rowcount)

        db.commit()

    @classmethod
    def set_mode(cls, db, store_id, mode):
        sql = "UPDATE store SET mode=%s WHERE id=%s"
        r = db.execute(sql, (mode, store_id))
        return r.rowcount

    @classmethod
    def get_store(cls, db, store_id):
        sql = "SELECT id, name FROM store WHERE id=%s"
        r = db.execute(sql, store_id)
        obj = r.fetchone()
        return obj
        
    @classmethod
    def get_store_gid(cls, db, store_id):
        sql = "SELECT group_id FROM store WHERE id=%s"
        r = db.execute(sql, store_id)
        obj = r.fetchone()
        gid = obj['group_id']
        return gid

    @classmethod
    def get_stores(cls, db, developer_id):
        sql = "SELECT id, name FROM store WHERE developer_id=%s"
        r = db.execute(sql, developer_id)
        return list(r.fetchall())

    @classmethod
    def get_store_count(cls, db, developer_id):
        sql = "SELECT count(*) as count FROM store WHERE developer_id=%s"
        r = db.execute(sql, developer_id)
        obj = r.fetchone()
        return obj['count']

    @classmethod
    def get_page_stores(cls, db, developer_id, offset, row_count):
        sql = "SELECT id, name FROM store WHERE developer_id=%s LIMIT %s, %s"
        r = db.execute(sql, (developer_id, offset, row_count))
        return list(r.fetchall())
        
