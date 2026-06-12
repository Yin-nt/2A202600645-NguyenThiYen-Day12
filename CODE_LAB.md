#  Code Lab: Deploy Your AI Agent to Production

> **AICB-P1 · VinUniversity 2026**  
> Thời gian: 3-4 giờ | Độ khó: Intermediate

##  Mục Tiêu

Sau khi hoàn thành lab này, bạn sẽ:
- Hiểu sự khác biệt giữa development và production
- Containerize một AI agent với Docker
- Deploy agent lên cloud platform
- Bảo mật API với authentication và rate limiting
- Thiết kế hệ thống có khả năng scale và reliable

---

##  Yêu Cầu

```bash
 Python 3.11+
 Docker & Docker Compose
 Git
 Text editor (VS Code khuyến nghị)
 Terminal/Command line
```

**Không cần:**
-  OpenAI API key (dùng mock LLM)
-  Credit card
-  Kinh nghiệm DevOps trước đó

---

##  Lộ Trình Lab

| Phần | Thời gian | Nội dung |
|------|-----------|----------|
| **Part 1** | 30 phút | Localhost vs Production |
| **Part 2** | 45 phút | Docker Containerization |
| **Part 3** | 45 phút | Cloud Deployment |
| **Part 4** | 40 phút | API Security |
| **Part 5** | 40 phút | Scaling & Reliability |
| **Part 6** | 60 phút | Final Project |

---

## Part 1: Localhost vs Production (30 phút)

###  Concepts

**Vấn đề:** "It works on my machine" — code chạy tốt trên laptop nhưng fail khi deploy.

**Nguyên nhân:**
- Hardcoded secrets
- Khác biệt về environment (Python version, OS, dependencies)
- Không có health checks
- Config không linh hoạt

**Giải pháp:** 12-Factor App principles

###  Exercise 1.1: Phát hiện anti-patterns

```bash
cd 01-localhost-vs-production/develop
```

**Nhiệm vụ:** Đọc `app.py` và tìm ít nhất 5 vấn đề.

<details>
<summary> Gợi ý</summary>

Tìm:
- API key hardcode
- Port cố định
- Debug mode
- Không có health check
- Không xử lý shutdown

</details>

###  Exercise 1.2: Chạy basic version

```bash
pip install -r requirements.txt
python app.py
```

Test:
```bash
curl http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

**Quan sát:** Nó chạy! Nhưng có production-ready không?

###  Exercise 1.3: So sánh với advanced version

```bash
cd ../production
cp .env.example .env
pip install -r requirements.txt
python app.py
```

**Nhiệm vụ:** So sánh 2 files `app.py`. Điền vào bảng:

| Feature | Basic | Advanced | Tại sao quan trọng? |
|---------|-------|----------|---------------------|
| Config | Hardcode | Env vars | ... |
| Health check |  |  | ... |
| Logging | print() | JSON | ... |
| Shutdown | Đột ngột | Graceful | ... |

###  Checkpoint 1

- [ ] Hiểu tại sao hardcode secrets là nguy hiểm
- [ ] Biết cách dùng environment variables
- [ ] Hiểu vai trò của health check endpoint
- [ ] Biết graceful shutdown là gì

---

## Part 2: Docker Containerization (45 phút)

###  Concepts

**Vấn đề:** "Works on my machine" part 2 — Python version khác, dependencies conflict.

**Giải pháp:** Docker — đóng gói app + dependencies vào container.

**Benefits:**
- Consistent environment
- Dễ deploy
- Isolation
- Reproducible builds

###  Exercise 2.1: Dockerfile cơ bản

```bash
cd ../../02-docker/develop
```

**Nhiệm vụ:** Đọc `Dockerfile` và trả lời:

1. Base image là gì?
2. Working directory là gì?
3. Tại sao COPY requirements.txt trước?
4. CMD vs ENTRYPOINT khác nhau thế nào?

###  Exercise 2.2: Build và run

```bash
# Build image
docker build -f 02-docker/develop/Dockerfile -t my-agent:develop .

# Run container
docker run -p 8000:8000 my-agent:develop

# Test
curl http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "What is Docker?"}'
```

**Quan sát:** Image size là bao nhiêu?
```bash
docker images my-agent:develop
```

###  Exercise 2.3: Multi-stage build

```bash
cd ../production
```

**Nhiệm vụ:** Đọc `Dockerfile` và tìm:
- Stage 1 làm gì?
- Stage 2 làm gì?
- Tại sao image nhỏ hơn?

Build và so sánh:
```bash
docker build -t my-agent:advanced .
docker images | grep my-agent
```

###  Exercise 2.4: Docker Compose stack

**Nhiệm vụ:** Đọc `docker-compose.yml` và vẽ architecture diagram.

```bash
docker compose up
```

Services nào được start? Chúng communicate thế nào?

Test:
```bash
# Health check
curl http://localhost/health

# Agent endpoint
curl http://localhost/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain microservices"}'
```

###  Checkpoint 2

- [ ] Hiểu cấu trúc Dockerfile
- [ ] Biết lợi ích của multi-stage builds
- [ ] Hiểu Docker Compose orchestration
- [ ] Biết cách debug container (`docker logs`, `docker exec`)

---

## Part 3: Cloud Deployment (45 phút)

###  Concepts

**Vấn đề:** Laptop không thể chạy 24/7, không có public IP.

**Giải pháp:** Cloud platforms — Railway, Render, GCP Cloud Run.

**So sánh:**

| Platform | Độ khó | Free tier | Best for |
|----------|--------|-----------|----------|
| Railway | ⭐ | $5 credit | Prototypes |
| Render | ⭐⭐ | 750h/month | Side projects |
| Cloud Run | ⭐⭐⭐ | 2M requests | Production |

###  Exercise 3.1: Deploy Railway (15 phút)

```bash
cd ../../03-cloud-deployment/railway
```

**Steps:**

1. Install Railway CLI:
```bash
npm i -g @railway/cli
```

2. Login:
```bash
railway login
```

3. Initialize project:
```bash
railway init
```

4. Set environment variables:
```bash
railway variables set PORT=8000
railway variables set AGENT_API_KEY=my-secret-key
```

5. Deploy:
```bash
railway up
```

6. Get public URL:
```bash
railway domain
```

**Nhiệm vụ:** Test public URL với curl hoặc Postman.

Test:
```bash
# Health check
curl http://student-agent-domain/health

# Agent endpoint
curl http://studen-agent-domain/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": ""}'
```

###  Exercise 3.2: Deploy Render (15 phút)

```bash
cd ../render
```

**Steps:**

1. Push code lên GitHub (nếu chưa có)
2. Vào [render.com](https://render.com) → Sign up
3. New → Blueprint
4. Connect GitHub repo
5. Render tự động đọc `render.yaml`
6. Set environment variables trong dashboard
7. Deploy!

**Nhiệm vụ:** So sánh `render.yaml` với `railway.toml`. Khác nhau gì?

###  Exercise 3.3: (Optional) GCP Cloud Run (15 phút)

```bash
cd ../production-cloud-run
```

**Yêu cầu:** GCP account (có free tier).

**Nhiệm vụ:** Đọc `cloudbuild.yaml` và `service.yaml`. Hiểu CI/CD pipeline.

###  Checkpoint 3

- [ ] Deploy thành công lên ít nhất 1 platform
- [ ] Có public URL hoạt động
- [ ] Hiểu cách set environment variables trên cloud
- [ ] Biết cách xem logs

---

## Part 4: API Security (40 phút)

###  Concepts

**Vấn đề:** Public URL = ai cũng gọi được = hết tiền OpenAI.

**Giải pháp:**
1. **Authentication** — Chỉ user hợp lệ mới gọi được
2. **Rate Limiting** — Giới hạn số request/phút
3. **Cost Guard** — Dừng khi vượt budget

###  Exercise 4.1: API Key authentication

```bash
cd ../../04-api-gateway/develop
```

**Nhiệm vụ:** Đọc `app.py` và tìm:
- API key được check ở đâu?
- Điều gì xảy ra nếu sai key?
- Làm sao rotate key?

Test:
```bash
python app.py

#  Không có key
curl http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'

#  Có key
curl http://localhost:8000/ask -X POST \
  -H "X-API-Key: secret-key-123" \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello"}'
```

###  Exercise 4.2: JWT authentication (Advanced)

```bash
cd ../production
```

**Nhiệm vụ:** 
1. Đọc `auth.py` — hiểu JWT flow
2. Lấy token:
```bash
python app.py

curl http://localhost:8000/token -X POST \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "secret"}'
```

3. Dùng token để gọi API:
```bash
TOKEN="<token_từ_bước_2>"
curl http://localhost:8000/ask -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"question": "Explain JWT"}'
```

###  Exercise 4.3: Rate limiting

**Nhiệm vụ:** Đọc `rate_limiter.py` và trả lời:
- Algorithm nào được dùng? (Token bucket? Sliding window?)
- Limit là bao nhiêu requests/minute?
- Làm sao bypass limit cho admin?

Test:
```bash
# Gọi liên tục 20 lần
for i in {1..20}; do
  curl http://localhost:8000/ask -X POST \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"question": "Test '$i'"}'
  echo ""
done
```

Quan sát response khi hit limit.

###  Exercise 4.4: Cost guard

**Nhiệm vụ:** Đọc `cost_guard.py` và implement logic:

```python
def check_budget(user_id: str, estimated_cost: float) -> bool:
    """
    Return True nếu còn budget, False nếu vượt.
    
    Logic:
    - Mỗi user có budget $10/tháng
    - Track spending trong Redis
    - Reset đầu tháng
    """
    # TODO: Implement
    pass
```

<details>
<summary> Solution</summary>

```python
import redis
from datetime import datetime

r = redis.Redis()

def check_budget(user_id: str, estimated_cost: float) -> bool:
    month_key = datetime.now().strftime("%Y-%m")
    key = f"budget:{user_id}:{month_key}"
    
    current = float(r.get(key) or 0)
    if current + estimated_cost > 10:
        return False
    
    r.incrbyfloat(key, estimated_cost)
    r.expire(key, 32 * 24 * 3600)  # 32 days
    return True
```

</details>

###  Checkpoint 4

- [ ] Implement API key authentication
- [ ] Hiểu JWT flow
- [ ] Implement rate limiting
- [ ] Implement cost guard với Redis

---

## Part 5: Scaling & Reliability (40 phút)

###  Concepts

**Vấn đề:** 1 instance không đủ khi có nhiều users.

**Giải pháp:**
1. **Stateless design** — Không lưu state trong memory
2. **Health checks** — Platform biết khi nào restart
3. **Graceful shutdown** — Hoàn thành requests trước khi tắt
4. **Load balancing** — Phân tán traffic

###  Exercise 5.1: Health checks

```bash
cd ../../05-scaling-reliability/develop
```

**Nhiệm vụ:** Implement 2 endpoints:

```python
@app.get("/health")
def health():
    """Liveness probe — container còn sống không?"""
    # TODO: Return 200 nếu process OK
    pass

@app.get("/ready")
def ready():
    """Readiness probe — sẵn sàng nhận traffic không?"""
    # TODO: Check database connection, Redis, etc.
    # Return 200 nếu OK, 503 nếu chưa ready
    pass
```

<details>
<summary> Solution</summary>

```python
@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/ready")
def ready():
    try:
        # Check Redis
        r.ping()
        # Check database
        db.execute("SELECT 1")
        return {"status": "ready"}
    except:
        return JSONResponse(
            status_code=503,
            content={"status": "not ready"}
        )
```

</details>

###  Exercise 5.2: Graceful shutdown

**Nhiệm vụ:** Implement signal handler:

```python
import signal
import sys

def shutdown_handler(signum, frame):
    """Handle SIGTERM from container orchestrator"""
    # TODO:
    # 1. Stop accepting new requests
    # 2. Finish current requests
    # 3. Close connections
    # 4. Exit
    pass

signal.signal(signal.SIGTERM, shutdown_handler)
```

Test:
```bash
python app.py &
PID=$!

# Gửi request
curl http://localhost:8000/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Long task"}' &

# Ngay lập tức kill
kill -TERM $PID

# Quan sát: Request có hoàn thành không?
```

###  Exercise 5.3: Stateless design

```bash
cd ../production
```

**Nhiệm vụ:** Refactor code để stateless.

**Anti-pattern:**
```python
#  State trong memory
conversation_history = {}

@app.post("/ask")
def ask(user_id: str, question: str):
    history = conversation_history.get(user_id, [])
    # ...
```

**Correct:**
```python
#  State trong Redis
@app.post("/ask")
def ask(user_id: str, question: str):
    history = r.lrange(f"history:{user_id}", 0, -1)
    # ...
```

Tại sao? Vì khi scale ra nhiều instances, mỗi instance có memory riêng.

###  Exercise 5.4: Load balancing

**Nhiệm vụ:** Chạy stack với Nginx load balancer:

```bash
docker compose up --scale agent=3
```

Quan sát:
- 3 agent instances được start
- Nginx phân tán requests
- Nếu 1 instance die, traffic chuyển sang instances khác

Test:
```bash
# Gọi 10 requests
for i in {1..10}; do
  curl http://localhost/ask -X POST \
    -H "Content-Type: application/json" \
    -d '{"question": "Request '$i'"}'
done

# Check logs — requests được phân tán
docker compose logs agent
```

###  Exercise 5.5: Test stateless

```bash
python test_stateless.py
```

Script này:
1. Gọi API để tạo conversation
2. Kill random instance
3. Gọi tiếp — conversation vẫn còn không?

###  Checkpoint 5

- [ ] Implement health và readiness checks
- [ ] Implement graceful shutdown
- [ ] Refactor code thành stateless
- [ ] Hiểu load balancing với Nginx
- [ ] Test stateless design

---

## Part 6: Final Project (60 phút)

###  Objective

Build một production-ready AI agent từ đầu, kết hợp TẤT CẢ concepts đã học.

###  Requirements

**Functional:**
- [ ] Agent trả lời câu hỏi qua REST API
- [ ] Support conversation history
- [ ] Streaming responses (optional)

**Non-functional:**
- [ ] Dockerized với multi-stage build
- [ ] Config từ environment variables
- [ ] API key authentication
- [ ] Rate limiting (10 req/min per user)
- [ ] Cost guard ($10/month per user)
- [ ] Health check endpoint
- [ ] Readiness check endpoint
- [ ] Graceful shutdown
- [ ] Stateless design (state trong Redis)
- [ ] Structured JSON logging
- [ ] Deploy lên Railway hoặc Render
- [ ] Public URL hoạt động

### 🏗 Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Nginx (LB)     │
└──────┬──────────┘
       │
       ├─────────┬─────────┐
       ▼         ▼         ▼
   ┌──────┐  ┌──────┐  ┌──────┐
   │Agent1│  │Agent2│  │Agent3│
   └───┬──┘  └───┬──┘  └───┬──┘
       │         │         │
       └─────────┴─────────┘
                 │
                 ▼
           ┌──────────┐
           │  Redis   │
           └──────────┘
```

###  Step-by-step

#### Step 1: Project setup (5 phút)

```bash
mkdir my-production-agent
cd my-production-agent

# Tạo structure
mkdir -p app
touch app/__init__.py
touch app/main.py
touch app/config.py
touch app/auth.py
touch app/rate_limiter.py
touch app/cost_guard.py
touch Dockerfile
touch docker-compose.yml
touch requirements.txt
touch .env.example
touch .dockerignore
```

#### Step 2: Config management (10 phút)

**File:** `app/config.py`

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # TODO: Define all config
    # - PORT
    # - REDIS_URL
    # - AGENT_API_KEY
    # - LOG_LEVEL
    # - RATE_LIMIT_PER_MINUTE
    # - MONTHLY_BUDGET_USD
    pass

settings = Settings()
```

#### Step 3: Main application (15 phút)

**File:** `app/main.py`

```python
from fastapi import FastAPI, Depends, HTTPException
from .config import settings
from .auth import verify_api_key
from .rate_limiter import check_rate_limit
from .cost_guard import check_budget

app = FastAPI()

@app.get("/health")
def health():
    # TODO
    pass

@app.get("/ready")
def ready():
    # TODO: Check Redis connection
    pass

@app.post("/ask")
def ask(
    question: str,
    user_id: str = Depends(verify_api_key),
    _rate_limit: None = Depends(check_rate_limit),
    _budget: None = Depends(check_budget)
):
    # TODO: 
    # 1. Get conversation history from Redis
    # 2. Call LLM
    # 3. Save to Redis
    # 4. Return response
    pass
```

#### Step 4: Authentication (5 phút)

**File:** `app/auth.py`

```python
from fastapi import Header, HTTPException

def verify_api_key(x_api_key: str = Header(...)):
    # TODO: Verify against settings.AGENT_API_KEY
    # Return user_id if valid
    # Raise HTTPException(401) if invalid
    pass
```

#### Step 5: Rate limiting (10 phút)

**File:** `app/rate_limiter.py`

```python
import redis
from fastapi import HTTPException

r = redis.from_url(settings.REDIS_URL)

def check_rate_limit(user_id: str):
    # TODO: Implement sliding window
    # Raise HTTPException(429) if exceeded
    pass
```

#### Step 6: Cost guard (10 phút)

**File:** `app/cost_guard.py`

```python
def check_budget(user_id: str):
    # TODO: Check monthly spending
    # Raise HTTPException(402) if exceeded
    pass
```

#### Step 7: Dockerfile (5 phút)

```dockerfile
# TODO: Multi-stage build
# Stage 1: Builder
# Stage 2: Runtime
```

#### Step 8: Docker Compose (5 phút)

```yaml
# TODO: Define services
# - agent (scale to 3)
# - redis
# - nginx (load balancer)
```

#### Step 9: Test locally (5 phút)

```bash
docker compose up --scale agent=3

# Test all endpoints
curl http://localhost/health
curl http://localhost/ready
curl -H "X-API-Key: secret" http://localhost/ask -X POST \
  -H "Content-Type: application/json" \
  -d '{"question": "Hello", "user_id": "user1"}'
```

#### Step 10: Deploy (10 phút)

```bash
# Railway
railway init
railway variables set REDIS_URL=...
railway variables set AGENT_API_KEY=...
railway up

# Hoặc Render
# Push lên GitHub → Connect Render → Deploy
```

###  Validation

Chạy script kiểm tra:

```bash
cd 06-lab-complete
python check_production_ready.py
```

Script sẽ kiểm tra:
-  Dockerfile exists và valid
-  Multi-stage build
-  .dockerignore exists
-  Health endpoint returns 200
-  Readiness endpoint returns 200
-  Auth required (401 without key)
-  Rate limiting works (429 after limit)
-  Cost guard works (402 when exceeded)
-  Graceful shutdown (SIGTERM handled)
-  Stateless (state trong Redis, không trong memory)
-  Structured logging (JSON format)

###  Grading Rubric

| Criteria | Points | Description |
|----------|--------|-------------|
| **Functionality** | 20 | Agent hoạt động đúng |
| **Docker** | 15 | Multi-stage, optimized |
| **Security** | 20 | Auth + rate limit + cost guard |
| **Reliability** | 20 | Health checks + graceful shutdown |
| **Scalability** | 15 | Stateless + load balanced |
| **Deployment** | 10 | Public URL hoạt động |
| **Total** | 100 | |

---

##  Hoàn Thành!

Bạn đã:
-  Hiểu sự khác biệt dev vs production
-  Containerize app với Docker
-  Deploy lên cloud platform
-  Bảo mật API
-  Thiết kế hệ thống scalable và reliable

###  Next Steps

1. **Monitoring:** Thêm Prometheus + Grafana
2. **CI/CD:** GitHub Actions auto-deploy
3. **Advanced scaling:** Kubernetes
4. **Observability:** Distributed tracing với OpenTelemetry
5. **Cost optimization:** Spot instances, auto-scaling

###  Resources

- [12-Factor App](https://12factor.net/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)

---

##  Q&A

**Q: Tôi không có credit card, có thể deploy không?**  
A: Có! Railway cho $5 credit, Render có 750h free tier.

**Q: Mock LLM khác gì với OpenAI thật?**  
A: Mock trả về canned responses, không gọi API. Để dùng OpenAI thật, set `OPENAI_API_KEY` trong env.

**Q: Làm sao debug khi container fail?**  
A: `docker logs <container_id>` hoặc `docker exec -it <container_id> /bin/sh`

**Q: Redis data mất khi restart?**  
A: Dùng volume: `volumes: - redis-data:/data` trong docker-compose.

**Q: Làm sao scale trên Railway/Render?**  
A: Railway: `railway scale <replicas>`. Render: Dashboard → Settings → Instances.

---

**Happy Deploying! **

---

# Đáp Án Bài Tập

## Part 1: Localhost vs Production

### Exercise 1.1: Các anti-pattern trong bản develop

1. API key được hardcode trong source code, dễ bị lộ khi commit hoặc chia sẻ.
2. Port `8000` được hardcode, không tương thích với port do cloud platform cấp.
3. Chạy với debug/reload mode, vừa tốn tài nguyên vừa có thể làm lộ thông tin lỗi.
4. Không có endpoint health check để platform phát hiện tiến trình bị lỗi.
5. Không xử lý graceful shutdown khi nhận `SIGTERM`.
6. Dùng `print()` thay vì structured logging nên khó tìm kiếm và giám sát log.
7. Cấu hình không lấy từ environment variables.
8. Thiếu validation và error handling phù hợp cho production.

### Exercise 1.3: So sánh basic và advanced

| Feature | Basic | Advanced | Tại sao quan trọng? |
|---------|-------|----------|---------------------|
| Config | Hardcode | Environment variables | Cho phép đổi cấu hình theo môi trường mà không sửa code hoặc rebuild |
| Health check | Không có | Có `/health` | Cloud platform biết ứng dụng còn hoạt động để restart khi cần |
| Logging | `print()` | Structured JSON logging | Dễ tìm kiếm, tổng hợp và phân tích bằng hệ thống logging |
| Shutdown | Đột ngột | Graceful shutdown | Cho request đang xử lý hoàn thành trước khi tiến trình dừng |
| Validation | Hạn chế | Pydantic models | Chặn dữ liệu không hợp lệ trước khi vào business logic |
| Security | Secret hardcode | Secret từ environment | Tránh đưa thông tin bí mật vào source control |

Health check là endpoint nhẹ dùng để báo trạng thái của ứng dụng. Graceful
shutdown là quá trình ngừng nhận request mới, hoàn thành request đang chạy,
đóng connection rồi mới thoát.

## Part 2: Docker Containerization

### Exercise 2.1: Dockerfile cơ bản

1. Base image là `python:3.11-slim`.
2. Working directory là `/app`.
3. `requirements.txt` được copy trước source code để tận dụng Docker layer cache.
   Khi code thay đổi nhưng dependencies không đổi, Docker không phải cài lại thư viện.
4. `CMD` cung cấp lệnh mặc định và dễ bị ghi đè khi chạy container.
   `ENTRYPOINT` xác định executable chính; arguments truyền khi `docker run`
   thường được nối vào sau entrypoint.

Kích thước image thực tế phụ thuộc Docker version, base-image version và cache
tại thời điểm build; kiểm tra bằng `docker images my-agent:develop`.

### Exercise 2.3: Multi-stage build

- Stage 1 (`builder`) cài compiler và dependencies, sau đó tạo các package cần thiết.
- Stage 2 (`runtime`) chỉ copy package đã cài và source code cần để chạy ứng dụng.
- Image nhỏ hơn vì compiler, header, cache và các công cụ build không xuất hiện
  trong runtime image.

### Exercise 2.4: Docker Compose stack

Các service được start:

- `nginx`: nhận request từ client và làm reverse proxy/load balancer.
- `agent`: chạy FastAPI AI agent.
- `redis`: lưu state dùng chung giữa các agent instance.

Luồng giao tiếp:

```text
Client -> Nginx -> Agent instance(s) -> Redis
```

Các container giao tiếp qua Docker network bằng service name như `agent` và
`redis`; chỉ Nginx cần publish port ra máy host.

## Part 3: Cloud Deployment

### Exercise 3.1: Railway

Railway build ứng dụng theo cấu hình trong `railway.toml`, inject environment
variables và cung cấp public domain. Sau deploy cần kiểm tra `/health`, `/ready`
và `/ask`; endpoint `/ask` phải gửi API key hợp lệ.

### Exercise 3.2: Railway và Render

| Nội dung | `railway.toml` | `render.yaml` |
|----------|----------------|---------------|
| Platform | Railway | Render |
| Mục đích | Cấu hình build/deploy của một Railway service | Blueprint mô tả một hoặc nhiều Render services |
| Environment variables | Thường đặt bằng CLI/dashboard | Có thể khai báo trong `envVars` |
| Health check | `healthcheckPath` | `healthCheckPath` |
| Secret | Đặt bằng Railway variables | `sync: false` hoặc `generateValue: true` |

### Exercise 3.3: Cloud Run CI/CD

`cloudbuild.yaml` mô tả pipeline build image, push image lên registry và deploy.
`service.yaml` mô tả Cloud Run service như container image, port, environment,
resource limits và scaling. Khi source thay đổi, pipeline tạo image mới rồi cập
nhật revision của Cloud Run.

## Part 4: API Security

### Exercise 4.1: API key authentication

- API key được đọc từ header `X-API-Key` và so sánh với key cấu hình.
- Nếu thiếu hoặc sai key, API trả về HTTP `401 Unauthorized`.
- Để rotate key: tạo key mới, cập nhật secret/environment variable trên platform,
  restart hoặc redeploy service, cập nhật client rồi vô hiệu hóa key cũ.

Không nên ghi API key vào source code hoặc log.

### Exercise 4.2: JWT flow

1. Client gửi username/password đến endpoint cấp token.
2. Server xác thực và ký JWT chứa user ID, role và thời gian hết hạn.
3. Client gửi `Authorization: Bearer <token>` trong các request tiếp theo.
4. Server kiểm tra chữ ký và expiry rồi lấy user/role từ payload.

JWT authentication là stateless vì server không cần lưu từng token session.

### Exercise 4.3: Rate limiting

- Bản production trong `04-api-gateway` dùng sliding-window dựa trên timestamps.
- User thường được giới hạn `10 requests/minute`; admin là `100 requests/minute`.
- Admin không hoàn toàn bypass, nhưng dùng limiter có ngưỡng cao hơn.
- Khi vượt limit, API trả HTTP `429 Too Many Requests` cùng `Retry-After`.

### Exercise 4.4: Cost guard

Cost guard kiểm tra chi phí hiện tại trước khi gọi LLM, ghi nhận chi phí sau khi
gọi và trả HTTP `402` khi user vượt budget. Trong final project, spending được
lưu trong Redis theo key dạng `budget:<user_id>:<YYYY-MM>` và có TTL để tự hết hạn.

## Part 5: Scaling & Reliability

### Exercise 5.1: Health checks

- `/health` là liveness probe: trả `200` nếu process vẫn sống.
- `/ready` là readiness probe: kiểm tra dependency như Redis; trả `503` nếu
  instance chưa thể nhận traffic.

Không nên thực hiện kiểm tra chậm hoặc quá nặng trong liveness probe.

### Exercise 5.2: Graceful shutdown

Khi nhận `SIGTERM`, ứng dụng đánh dấu không ready để load balancer ngừng gửi
request mới. Uvicorn chờ request đang chạy hoàn thành trong thời gian timeout,
lifespan shutdown đóng các connection rồi tiến trình mới thoát.

### Exercise 5.3: Stateless design

State trong memory chỉ tồn tại trên một instance. Khi load balancer chuyển request
sang instance khác hoặc instance bị restart, state đó sẽ mất. Lưu conversation
history trong Redis giúp mọi instance đọc cùng dữ liệu và có thể scale ngang.

### Exercise 5.4: Load balancing

Khi chạy `docker compose up --scale agent=3`, Docker tạo ba agent container.
Nginx gửi request theo cơ chế round-robin đến service `agent`. Nếu một instance
không phản hồi, `proxy_next_upstream` cho phép thử instance khác.

### Exercise 5.5: Stateless test

Test đạt yêu cầu khi conversation vẫn tồn tại sau khi một agent instance bị dừng
và request tiếp theo được xử lý bởi instance khác. Điều này chứng minh state nằm
trong Redis thay vì memory của agent.

## Part 6: Final Project

Final project trong thư mục `06-lab-complete` đã triển khai:

- REST API và conversation history lưu trong Redis.
- API key authentication.
- Redis sliding-window rate limit `10 requests/minute/user`.
- Redis monthly cost guard `$10/user`.
- `/health`, `/ready` và graceful shutdown.
- Structured JSON logging.
- Multi-stage Dockerfile chạy bằng non-root user.
- Docker Compose gồm Nginx, các agent instance và Redis có persistent volume.
- Railway và Render deployment configuration.

Chạy local:

```bash
cd 06-lab-complete
docker compose up --build --scale agent=3
curl http://localhost:8000/health
curl http://localhost:8000/ready
curl -X POST http://localhost:8000/ask \
  -H "X-API-Key: dev-key-change-me" \
  -H "Content-Type: application/json" \
  -d '{"question":"Hello","user_id":"user1"}'
```

Kiểm tra production readiness:

```bash
python check_production_ready.py
```

Kết quả hiện tại: `20/20 checks passed (100%)`.

### Step 10: Kết quả deploy Render

- Public URL: <https://twoa202600645-nguyenthiyen-day12.onrender.com>
- API documentation: <https://twoa202600645-nguyenthiyen-day12.onrender.com/docs>
- Thời điểm kiểm tra: `2026-06-12`

Kết quả kiểm tra public deployment:

| Kiểm tra | Kết quả |
|----------|---------|
| `GET /health` | HTTP `200`, trả `{"status":"ok"}` |
| `GET /ready` | HTTP `200`, trả `{"status":"ready"}` |
| `POST /ask` không có API key | HTTP `401 Unauthorized` |
| Public URL hoạt động | Đạt |
| API key authentication | Đạt |
| Render deployment | Đạt |

Lệnh kiểm tra deployment:

```powershell
$URL = "https://twoa202600645-nguyenthiyen-day12.onrender.com"
$API_KEY = "<AGENT_API_KEY được cấu hình trên Render>"

curl.exe "$URL/health"
curl.exe "$URL/ready"

curl.exe -X POST "$URL/ask" `
  -H "X-API-Key: $API_KEY" `
  -H "Content-Type: application/json" `
  -d '{\"question\":\"What is production deployment?\",\"user_id\":\"user1\"}'
```
