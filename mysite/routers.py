class AppRouter:
    """
    让 'app' 的所有模型使用 MySQL，其余使用默认 SQLite
    """
    APP_LABEL = 'app'
    DB_NAME = 'mysql_db'

    def db_for_read(self, model, **hints):
        if model._meta.app_label == self.APP_LABEL:
            return self.DB_NAME
        return None   # None 表示交给下一个 router 或用 default

    def db_for_write(self, model, **hints):
        if model._meta.app_label == self.APP_LABEL:
            return self.DB_NAME
        return None

    def allow_relation(self, obj1, obj2, **hints):
        # 不允许跨数据库建立外键关系
        if obj1._meta.app_label == self.APP_LABEL or \
           obj2._meta.app_label == self.APP_LABEL:
            return obj1._meta.app_label == obj2._meta.app_label
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label == self.APP_LABEL:
            return db == self.DB_NAME   # app 只迁移到 mysql_db
        return db == 'default'          # 其他只迁移到 default