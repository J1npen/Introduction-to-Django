# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class BookmarkTags(models.Model):
    pk = models.CompositePrimaryKey('bookmark_id', 'tag_id')
    bookmark = models.ForeignKey('Bookmarks', models.DO_NOTHING)
    tag = models.ForeignKey('Tags', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'bookmark_tags'
        db_table_comment = '书签与标签的关联表'


class Bookmarks(models.Model):
    url = models.CharField(max_length=2048, db_comment='网站地址')
    title = models.CharField(max_length=200, db_comment='网站标题')
    description = models.TextField(blank=True, null=True, db_comment='简要描述')
    favicon_url = models.CharField(max_length=512, blank=True, null=True, db_comment='网站图标地址')
    is_domestic = models.IntegerField(db_comment='地域：1 = 国内，0 = 国外')
    site_scale = models.CharField(max_length=10, db_comment='网站规模')
    is_active = models.IntegerField(db_comment='是否可访问')
    is_favorite = models.IntegerField(db_comment='收藏星标')
    visit_count = models.PositiveIntegerField(db_comment='点击次数')
    last_visit = models.DateTimeField(blank=True, null=True, db_comment='最近访问时间')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'bookmarks'
        db_table_comment = '网站书签'


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class Tags(models.Model):
    name = models.CharField(unique=True, max_length=50, db_comment='标签名称，如 博客、工具、AI')
    slug = models.CharField(unique=True, max_length=50, db_comment='URL 友好标识')
    color = models.CharField(max_length=7, blank=True, null=True, db_comment='标签颜色（HEX）')

    class Meta:
        managed = False
        db_table = 'tags'
        db_table_comment = '书签标签'