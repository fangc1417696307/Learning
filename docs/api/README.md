# API 契约（OpenAPI 3.1）

`openapi.yaml` 是《接口规范文档》的机器可读版本：同一套接口、同一套字段，只是换了个能被工具解析的载体。

- **docx 给人看**：评审、答辩、写报告。
- **YAML 给机器看**：生成文档页、Mock 服务、前端类型、契约测试。

两者内容必须一致，改一个就要改另一个。这是这份文件唯一的维护成本。

## 里面有什么

| 项 | 数量 | 说明 |
|---|---|---|
| 路径 | 23 | 21 条目标接口路径 + 2 条练习期遗留路径 |
| 操作 | 24 | 22 个目标接口 + 2 个已实现接口（标记 `deprecated`） |
| Schema | 54 | 请求体、响应实体、枚举 |
| 鉴权 | 全局 `bearerAuth` | 注册、登录、练习期接口单独设为 `security: []` |

响应统一为 `{code, message, data, request_id}`，见 `components.schemas.ApiEnvelope`。

## 怎么用

**1. 校验（每次改完都要跑）**

```bash
pip install openapi-spec-validator
python -c "import yaml;from openapi_spec_validator import validate;validate(yaml.safe_load(open('docs/api/openapi.yaml',encoding='utf-8')))"
```

或者用 Redocly（还能查风格问题）：

```bash
npx @redocly/cli lint docs/api/openapi.yaml
```

**2. 看文档（比翻 Word 快）**

生成一个可以直接双击打开的网页：

```bash
npx @redocly/cli@latest build-docs docs/api/openapi.yaml -o docs/api/reference.html
```

改完 YAML 想立刻看到效果，用带热重载的预览服务器：

```bash
npx @redocly/cli@1 preview-docs docs/api/openapi.yaml
# 浏览器打开 http://127.0.0.1:8080
```

必须锁 `@1`：Redocly CLI 2.x 删掉了 `preview-docs` 命令，直接跑 `@latest preview-docs`
会报 `Unknown arguments`。这是版本演进的常态——命令会消失，锁版本才可复现。

> 生成的 `reference.html` 是从 CDN 加载 Redoc 渲染器的，断网会停在 Loading。
> 要完全离线，得把渲染器内联进 HTML（约 1.5 MB）。

**3. 起 Mock，前端不用等后端**

```bash
npx @stoplight/prism-cli mock docs/api/openapi.yaml -p 4011
```

公开接口可以直接调：

```bash
curl -X POST http://127.0.0.1:4011/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"2023010101","password":"S3cure!pass"}'
```

需要登录的接口必须带令牌——Prism 会按 `security` 定义真的返回 401，**不是 mock 坏了**：

```bash
curl -H "Authorization: Bearer test-token" http://127.0.0.1:4011/api/v1/auth/me
```

实测返回（字段按 schema 生成，值没有业务意义）：

```json
{"code":1,"message":"ok","data":{"user_id":0,"username":"string","display_name":"string",
 "role":"student","major":"string","grade":"string","profile_completeness":0,
 "created_at":"2019-08-24T14:15:22Z"},"request_id":"a1b2c3d4e5f6"}
```

前端可以照着它写页面，后端写完再换真实地址，接口形状不用改。

**4. 生成前端类型（第 28 课用得上）**

```bash
npx openapi-typescript docs/api/openapi.yaml -o src/api.d.ts
```

一行手写都不用，`Profile`、`Dimension`、`RegisterRequest` 这些类型全部自动生成。

## 和 FastAPI 自动生成的 OpenAPI 什么关系

FastAPI 会从代码里推出 OpenAPI：`http://127.0.0.1:8001/openapi.json`。那是 **code-first**——有什么代码就有什么契约。

这份文件是 **spec-first**——先有契约，代码按它追。两份同时存在时必须划清边界：

- 已经实现的接口，以代码生成的为准（代码不会骗人）。
- 还没实现的接口，以这份文件为准。
- 第 18 课（鉴权）之后，建议只保留一种，否则必然漂移。

## 改这个文件的规矩

| 改动 | 是否升版本 | 说明 |
|---|---|---|
| 加字段、加接口、加可选参数 | 不需要 | 加法是安全的，老前端不受影响 |
| 改字段含义、改类型、删字段 | 必须升 `/api/v2` | 破坏性变更，前端会当场炸 |
| 改示例、改描述 | 不需要 | 但记得同步 docx |

改完跑一次 lint，再回头改《接口规范文档》和《数据库设计说明书》对应的表。
