# 项目运行说明

这个项目是一个 Django 本地开发项目，当前仓库使用 SQLite 数据库，静态资源位于 `static/`，开发环境下不需要额外配置 Nginx 或 MySQL。

## 1. 运行环境

- Python 3.12 及以上
- pip
- Django 6.0.2

如果你直接使用仓库里的虚拟环境，本机当前可用解释器是：

```bash
/Users/yaccyan/Desktop/Django/soccer_admin/.venv/bin/python
```

## 2. 进入项目目录

```bash
cd /Users/yaccyan/Desktop/Django/soccer_admin
```

## 3. 创建并激活虚拟环境（首次运行时）

如果你已经有可用的 `.venv`，这一节可以跳过。

```bash
python3 -m venv .venv
source .venv/bin/activate
```

## 4. 安装依赖

当前代码实际依赖很少，至少需要安装 Django：

```bash
pip install Django==6.0.2
```

如果你已经激活了仓库中的 `.venv`，通常不需要重复安装。

## 5. 初始化数据库

项目默认使用根目录下的 `db.sqlite3`。首次运行或数据库丢失时，执行：

```bash
python manage.py migrate
```

这个项目的迁移里已经包含了部分初始化数据，例如：

- 示例新闻
- 2026 赛程
- 球队数据
- 积分榜数据

## 6. 启动开发服务器

```bash
python manage.py runserver
```

启动后访问：

- 首页：http://127.0.0.1:8000/
- 管理后台：http://127.0.0.1:8000/admin/
- 购票页面：http://127.0.0.1:8000/tickets/
- 赛程页面：http://127.0.0.1:8000/schedule/
- 积分榜页面：http://127.0.0.1:8000/standings/
- 球员榜页面：http://127.0.0.1:8000/players/

## 7. 创建管理员账号（可选）

如果你要登录 Django 管理后台，先创建超级用户：

```bash
python manage.py createsuperuser
```

按提示输入用户名、邮箱和密码即可。

## 8. 推荐的完整启动流程

如果你是第一次在新环境运行，建议按下面顺序执行：

```bash
cd /Users/yaccyan/Desktop/Django/soccer_admin
python3 -m venv .venv
source .venv/bin/activate
pip install Django==6.0.2
python manage.py migrate
python manage.py runserver
```

## 9. 常用排查命令

检查 Django 配置是否正常：

```bash
python manage.py check
```

查看迁移状态：

```bash
python manage.py showmigrations
```

## 10. 当前仓库已验证状态

在当前工作区中，下面两条命令已经可以正常执行：

```bash
python manage.py check
python manage.py showmigrations
```

并且当前数据库迁移已经全部完成。