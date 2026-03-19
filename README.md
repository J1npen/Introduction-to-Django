# Introduction to Django

一个 Django 学习项目，包含书签管理和留言板两个应用。

## 项目结构

- **app/** - 书签管理，使用 MySQL 数据库
- **board/** - 留言板，使用 SQLite 数据库

## 快速开始

**1. 克隆并安装依赖**
```bash
git clone https://github.com/J1npen/Introduction-to-Django.git
cd Introduction-to-Django
pip install -r requirements.txt
```

**2. 配置本地设置**
```bash
cp mysite/local_settings.example.py mysite/local_settings.py
```
编辑 `mysite/local_settings.py`，填入你的 MySQL 连接信息。

**3. 初始化数据库**
```bash
python manage.py migrate
```

**4. 启动开发服务器**
```bash
python manage.py runserver
```

## 页面路由

| 路径 | 说明 |
|------|------|
| `/app/` | 首页 |
| `/app/bookmark` | 书签搜索 |
| `/app/get-bookmarks/` | 书签列表（JSON） |
| `/app/picrotate/` | 图片轮播 |
| `/board/` | 留言板 |
| `/admin/` | 后台管理 |

## 技术栈

- Python / Django 6.0
- MySQL（书签数据）+ SQLite（留言数据）
