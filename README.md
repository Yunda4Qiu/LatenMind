
# LatentMind

LatentMind 是一个“前后端分离”的小型交互实验：

- **后端（FastAPI）**：提供 API（默认 `http://127.0.0.1:8001`）
- **前端（纯静态 HTML/JS）**：通过 `fetch()` 调用后端 API

## 1) 启动后端（API）

在你的 conda 环境里启动（你当前环境是 `appenv313`）：

```bash
cd backend
conda activate appenv313
uvicorn app:app --reload --port 8001
```

验证：

- 打开 `http://127.0.0.1:8001/docs` 能看到 Swagger UI
- 打开 `http://127.0.0.1:8001/` 只会返回 JSON（这是正常的，因为它是 API 服务）

## 2) 启动前端（静态页面）

重要：**不要直接双击打开 `frontend/index.html`（file://）**。浏览器会因为安全策略导致请求失败，看起来像“按钮没反应”。

任选其一：

### 方案 A：用 Python 起一个静态服务器（推荐）

```bash
cd frontend
python3 -m http.server 5500
```

然后打开：

- `http://127.0.0.1:5500/index.html`

### 方案 B：VS Code Live Server

用 Live Server 打开 `frontend/index.html`（端口一般是 `5500`）。

## 3) 在浏览器里怎么玩

1. 打开前端页面：`http://127.0.0.1:5500/index.html`
2. 点击 **Start Experiment**
3. 点击 **Action 0/1/2** 进行回合操作
4. 到第 20 回合会出现 **View report** 按钮（不会强制跳转），你可以查看报告后再返回继续游戏

## 常见问题排查

### 1) 点按钮没反应

优先检查浏览器开发者工具：

- Chrome: View → Developer → Developer Tools → Console / Network

常见原因：

- 前端是用 `file://` 打开的（请用上面的静态服务器方式）
- 后端没启动，或端口不一致（后端应是 `8001`）

### 2) CORS 报错

后端已允许 `localhost/127.0.0.1` 任意端口用于本地开发；如果你改了域名或用别的设备访问，需要相应调整 CORS。

