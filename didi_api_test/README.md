# 网约车订单接口自动化测试项目

这是一个面向测试开发实习生的学习型项目，目标是把前面学习的 Python、requests、pytest、测试用例设计、参数化、fixture、JSON 数据管理、SQL、Linux、Git 和面试表达串起来。

项目使用一个本地模拟服务来模拟网约车业务接口，不依赖真实滴滴接口。你可以在 PyCharm 里打开本项目，启动模拟服务后运行 pytest。

## 技术栈

- Python
- requests
- pytest
- pytest 参数化
- pytest fixture
- JSON 测试数据
- 本地 mock HTTP 服务

## 项目结构

```text
didi_api_test/
  common/              公共工具
    config.py          配置
    request_util.py    GET/POST 请求封装
    assertions.py      常用断言封装
    business.py        业务辅助函数
  data/                测试数据
    login_cases.json
    order_cases.json
  docs/                测试文档和学习资料
    test_cases.md
    interview_project_intro.md
    learning_checklist.md
  server/              本地模拟接口服务
    mock_server.py
  sql/                 SQL 示例
    order_queries.sql
  scripts/             辅助命令
    run_tests.ps1
    git_commands.md
    linux_commands.md
  tests/               自动化测试用例
    conftest.py
    test_login.py
    test_order.py
    test_business_utils.py
    test_http_status.py
  pytest.ini           pytest 配置
  requirements.txt     依赖
```

## 如何运行

### 1. 安装依赖

```bash
python -m pip install -r requirements.txt
```

### 2. 运行测试

现在项目已经配置了 pytest 自动启动 mock 服务，所以可以直接运行测试，不需要手动启动 server/mock_server.py。

如果你想单独观察模拟接口服务，也可以手动启动：

```bash
python server/mock_server.py
```

### 3. 运行测试

再打开一个终端：

```bash
python -m pytest -v
```

也可以只运行登录测试：

```bash
python -m pytest tests/test_login.py -v
```

只运行订单测试：

```bash
python -m pytest tests/test_order.py -v
```

## 覆盖的学习点

1. Python 函数、字典、列表、JSON 文件读取
2. requests GET / POST 请求
3. Header、Token、JSON Body
4. pytest 测试函数和 assert
5. pytest 参数化
6. pytest fixture
7. 登录接口测试
8. 订单创建、查询、取消接口测试
9. 测试用例设计
10. Bug 描述
11. SQL 查询示例
12. Linux 日志命令
13. Git 项目管理

## 简历项目描述

基于 Python + Pytest + Requests 搭建网约车订单接口自动化测试项目，使用本地 mock 服务模拟登录、创建订单、查询订单、取消订单等核心接口。项目通过 JSON 文件管理测试数据，使用 pytest 参数化覆盖正常流程、参数缺失、鉴权失败、重复取消等场景，并通过 fixture 统一维护 token 和请求头。测试中对状态码、响应字段、错误提示和订单状态流转进行断言，提升核心接口回归测试效率。

