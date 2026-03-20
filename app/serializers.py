from rest_framework import serializers
from django.utils import timezone
from .models import Bookmarks, Tags, BookmarkTags


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['id', 'name', 'slug', 'color']


class BookmarkSerializer(serializers.ModelSerializer):
    # tag_ids（写入）/ tags（读取）：创建或更新书签时传 tag_ids: [1, 2]，PATCH 时不传则不改标签；响应里 tags 嵌套返回完整标签对象
    tags = serializers.SerializerMethodField() # SerializerMethodField: 当你需要返回一些数据库里没有直接存储、或者是需要经过复杂逻辑计算的数据时，就会用到它。
    tag_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tags.objects.all(),
        write_only=True,
        required=False,
        help_text='要关联的标签 ID 列表，传入后会替换原有全部标签',
    )

    class Meta:
        model = Bookmarks
        fields = [
            'id', 'title', 'url', 'description', 'favicon_url',
            'is_domestic', 'site_scale', 'is_active', 'is_favorite',
            'visit_count', 'last_visit', 'created_at', 'updated_at',
            'tags', 'tag_ids',
        ]
        # read_only_fields：visit_count、last_visit、created_at、updated_at 不可由客户端设置
        read_only_fields = ['visit_count', 'last_visit', 'created_at', 'updated_at']

    # 编写 SerializerMethodField 配套方法，格式为 get_ + 字段名
    # 调用 get_tags 方法的时机和位置是由 Django REST Framework (DRF) 的序列化机制 
    # 自动管理的。你不需要在代码中手动调用它，框架会在特定流程中触发它。
    # 当你在 Views.py 访问 BookmarkSerializer 的实例时
    # DRF 内部会遍历所有字段，发现 tags 是 SerializerMethodField
    # 于是它会自动寻找并执行 get_tags(user)
    def get_tags(self, obj):
        # obj 是当前正在被处理的 tags 实例
        qs = Tags.objects.filter(bookmarktags__bookmark=obj)
        return TagSerializer(qs, many=True).data

    def create(self, validated_data):
        tag_objs = validated_data.pop('tag_ids', [])
        now = timezone.now()
        validated_data.setdefault('visit_count', 0)
        validated_data.setdefault('created_at', now)
        validated_data.setdefault('updated_at', now)
        bookmark = Bookmarks.objects.create(**validated_data)
        if tag_objs:
            BookmarkTags.objects.bulk_create([
                BookmarkTags(bookmark=bookmark, tag=tag) for tag in tag_objs
            ])
        return bookmark

    def update(self, instance, validated_data):
        tag_objs = validated_data.pop('tag_ids', None)
        validated_data['updated_at'] = timezone.now()
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        # tag_ids 传了才替换，没传则保持不变（支持 PATCH 局部更新）
        if tag_objs is not None:
            BookmarkTags.objects.filter(bookmark=instance).delete()
            if tag_objs:
                BookmarkTags.objects.bulk_create([
                    BookmarkTags(bookmark=instance, tag=tag) for tag in tag_objs
                ])
        return instance
