# Self-Host NLP Service trên Máy của Bạn

## Tổng quan

Host NLP service ngay trên máy Windows của bạn và expose ra internet qua NAT/Port Forwarding.

**Ưu điểm:**
- ✅ FREE (không tốn tiền hosting)
- ✅ Full control (2GB+ RAM tùy máy bạn)
- ✅ Không bị sleep
- ✅ Low latency (máy local)

**Nhược điểm:**
- ⚠️ Phải bật máy 24/7
- ⚠️ Tốn điện (~5-10W)
- ⚠️ Phụ thuộc internet nhà (uptime, tốc độ upload)
- ⚠️ Security risk nếu không config đúng

---

## Setup Guide (Windows)

### Bước 1: Cài đặt NLP Service như Windows Service

**1.1. Chạy script cài đặt (với quyền Administrator):**

```powershell
# Mở PowerShell as Administrator
# Chuột phải PowerShell → Run as Administrator

cd C:\Users\Thanh\Desktop\career-compass-ai

# Allow script execution
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run installer
.\install_nlp_service.ps1 -Port 8001
```

Script sẽ:
- Kiểm tra Python 3.11
- Cài đặt dependencies từ requirements.txt
- Download NSSM (Windows Service Manager)
- Tạo Windows Service "CareerCompassNLP"
- Config auto-start
- Bật Windows Firewall rule

**1.2. Verify service đang chạy:**

```powershell
# Check service status
Get-Service CareerCompassNLP

# Output:
# Status   Name                DisplayName
# ------   ----                -----------
# Running  CareerCompassNLP    Career Compass NLP Service

# View real-time logs
Get-Content nlp-service\logs\service_stdout.log -Tail 50 -Wait
```

**1.3. Test local endpoint:**

```powershell
# Health check
Invoke-WebRequest http://localhost:8001/health

# Test scoring
Invoke-WebRequest -Uri http://localhost:8001/score-cv `
  -Method POST `
  -Headers @{"Content-Type"="application/json"} `
  -Body '{"cv_text":"Python developer","jd_text":"Backend engineer","language":"en"}'
```

---

### Bước 2: Lấy IP Public của bạn

**2.1. Kiểm tra IP public:**

```powershell
# Check public IP
Invoke-WebRequest -Uri https://api.ipify.org/?format=text | Select-Object -ExpandProperty Content

# Output example: 123.45.67.89
```

**2.2. Kiểm tra IP local của máy:**

```powershell
# Get local IP
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.PrefixOrigin -eq "Dhcp"} | Select-Object IPAddress, InterfaceAlias

# Output example:
# IPAddress     InterfaceAlias
# ---------     --------------
# 192.168.1.100 Wi-Fi
```

Ghi nhớ:
- **Public IP**: `123.45.67.89` (dùng để access từ internet)
- **Local IP**: `192.168.1.100` (dùng cho port forwarding)

---

### Bước 3: Setup Port Forwarding trên Router

**3.1. Truy cập router admin:**

```
Mở browser → http://192.168.1.1 (hoặc 192.168.0.1)
Login với admin/password (thường ghi sau router)
```

**3.2. Tìm phần Port Forwarding:**

Tùy router, tìm menu:
- **"Port Forwarding"** / **"Virtual Server"**
- **"NAT"** / **"Advanced Settings"**
- **"Firewall"** → **"Port Forwarding"**

**3.3. Tạo rule mới:**

| Field | Value | Ghi chú |
|-------|-------|---------|
| Service Name | NLP-Service | Tùy đặt |
| External Port | **8001** | Port từ internet |
| Internal IP | **192.168.1.100** | IP máy của bạn |
| Internal Port | **8001** | Port NLP service |
| Protocol | **TCP** | Hoặc TCP/UDP |
| Enabled | ✅ | Active |

**Common Routers:**

**TP-Link:**
```
Advanced → NAT Forwarding → Virtual Servers → Add
- Service Port: 8001
- Internal Port: 8001
- IP Address: 192.168.1.100
- Protocol: TCP
→ Save
```

**Viettel (GPON):**
```
Application → Port Forwarding
- Name: NLP-Service
- WAN: Internet
- External Port: 8001
- Internal Host: 192.168.1.100
- Internal Port: 8001
→ Apply
```

**FPT (GPON):**
```
Advanced → NAT → Port Mapping
- External Port: 8001
- Internal Host: 192.168.1.100
- Internal Port: 8001
- Protocol: TCP
→ Add
```

**3.4. Save và reboot router** (nếu cần)

---

### Bước 4: Test Port Forwarding

**4.1. Test từ máy khác (hoặc dùng 4G/5G):**

```bash
# Từ điện thoại/máy khác (không cùng WiFi nhà)
curl http://123.45.67.89:8001/health

# Expected: {"status":"ok"}
```

**4.2. Dùng online tool:**

```
https://www.yougetsignal.com/tools/open-ports/

Enter:
- Remote Address: 123.45.67.89 (IP của bạn)
- Port Number: 8001

→ Click "Check"
→ Should show "Port 8001 is open"
```

**Nếu port ĐÓNG:**
- Kiểm tra Windows Firewall (bước 1)
- Kiểm tra router port forwarding config
- Kiểm tra ISP có block port không (gọi hotline)
- Thử đổi port khác (8080, 9000)

---

### Bước 5: Setup DDNS (Dynamic DNS)

**Vấn đề:** IP public thường đổi mỗi khi router restart.

**Giải pháp:** Dùng DDNS để có domain name cố định.

**5.1. Đăng ký DDNS miễn phí:**

**No-IP (Khuyến nghị):**
```
1. Đăng ký: https://www.noip.com/sign-up
2. Tạo hostname: mynlp.ddns.net
3. Confirm email
```

**DuckDNS:**
```
1. Login bằng GitHub: https://www.duckdns.org/
2. Tạo subdomain: mynlp (→ mynlp.duckdns.org)
3. Copy token
```

**5.2. Cài DDNS updater trên máy:**

**No-IP Client (Windows):**
```
1. Download: https://www.noip.com/download
2. Install No-IP DUC (Dynamic Update Client)
3. Login với account No-IP
4. Chọn hostname: mynlp.ddns.net
5. Service sẽ auto-update IP mỗi 5 phút
```

**DuckDNS (PowerShell script):**

Tạo file `update_duckdns.ps1`:
```powershell
# Replace with your token and domain
$token = "your-duckdns-token"
$domain = "mynlp"

while ($true) {
    try {
        Invoke-WebRequest "https://www.duckdns.org/update?domains=$domain&token=$token"
        Write-Host "$(Get-Date) - IP updated successfully"
    } catch {
        Write-Host "$(Get-Date) - Update failed: $_"
    }
    Start-Sleep -Seconds 300  # Update every 5 minutes
}
```

Chạy như Windows Task:
```powershell
# Create scheduled task
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File C:\path\to\update_duckdns.ps1"
$trigger = New-ScheduledTaskTrigger -AtStartup
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "DuckDNS-Updater" -Description "Update DuckDNS IP"
```

**5.3. Test DDNS:**

```powershell
# After 5 minutes
curl http://mynlp.ddns.net:8001/health
# hoặc
curl http://mynlp.duckdns.org:8001/health
```

---

### Bước 6: Update Backend Environment

**6.1. Nếu backend ở Render:**

```
Render Dashboard → career-compass-backend → Environment

Thêm/sửa:
NLP_SERVICE_URL=http://mynlp.ddns.net:8001
```

**6.2. Nếu backend local:**

Sửa `backend/.env`:
```env
NLP_SERVICE_URL=http://localhost:8001
# Hoặc nếu backend cũng muốn expose:
NLP_SERVICE_URL=http://192.168.1.100:8001
```

**6.3. Nếu backend cũng ở máy khác/cloud:**

```env
NLP_SERVICE_URL=http://123.45.67.89:8001
# Hoặc với DDNS:
NLP_SERVICE_URL=http://mynlp.ddns.net:8001
```

Save và restart backend.

---

### Bước 7: Security Hardening (Khuyến nghị)

**7.1. Thêm Basic Authentication:**

Sửa `nlp-service/app/main.py`:

```python
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets

app = FastAPI()
security = HTTPBasic()

# Set credentials (hoặc đọc từ env)
VALID_USERNAME = "nlp-admin"
VALID_PASSWORD = "your-secure-password"

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, VALID_USERNAME)
    correct_password = secrets.compare_digest(credentials.password, VALID_PASSWORD)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

# Protect all endpoints
@app.get("/health")
async def health(username: str = Depends(verify_credentials)):
    return {"status": "ok"}

@app.post("/score-cv")
async def score_cv(request: ScoreCvRequest, username: str = Depends(verify_credentials)):
    # ... existing code
```

Update backend request with auth:
```rust
// In backend config
NLP_SERVICE_URL=http://nlp-admin:your-secure-password@mynlp.ddns.net:8001
```

**7.2. Dùng HTTPS (Advanced):**

Options:
- **Cloudflare Tunnel** (free, khuyến nghị)
- **Nginx reverse proxy + Let's Encrypt**
- **Ngrok** (có free tier)

---

## Service Management Commands

```powershell
# Start service
Start-Service CareerCompassNLP

# Stop service
Stop-Service CareerCompassNLP

# Restart service
Restart-Service CareerCompassNLP

# Check status
Get-Service CareerCompassNLP

# View logs (real-time)
Get-Content nlp-service\logs\service_stdout.log -Tail 50 -Wait

# View error logs
Get-Content nlp-service\logs\service_stderr.log -Tail 50

# Uninstall service
# (Run as Administrator)
sc.exe delete CareerCompassNLP
```

---

## Troubleshooting

### Service không start

```powershell
# Check event logs
Get-EventLog -LogName Application -Source CareerCompassNLP -Newest 10

# Check Python path
Get-Command python | Select-Object Path

# Reinstall dependencies
cd nlp-service
python -m pip install -r requirements.txt --force-reinstall
```

### Port forwarding không hoạt động

1. **Check Windows Firewall:**
   ```powershell
   Get-NetFirewallRule -DisplayName "Career Compass NLP Service"
   ```

2. **Check router firewall:**
   - Vào router admin → tắt firewall tạm (test)

3. **Check ISP blocking:**
   - Một số ISP block port 8001
   - Thử port khác: 8080, 9000, 8888
   - Hoặc gọi ISP yêu cầu mở port

4. **Test local first:**
   ```powershell
   # Từ máy khác cùng WiFi
   curl http://192.168.1.100:8001/health
   ```

### IP public bị đổi

- Dùng DDNS (No-IP, DuckDNS) như bước 5
- Hoặc upgrade ISP lên Static IP (~50k/tháng)

### Service chạy chậm

```powershell
# Check RAM usage
Get-Process python | Select-Object WorkingSet

# Should be ~1.5-2GB when models loaded
```

---

## Alternative: Cloudflare Tunnel (HTTPS miễn phí)

Nếu không muốn port forwarding, dùng Cloudflare Tunnel:

```powershell
# Install cloudflared
winget install Cloudflare.cloudflared

# Login
cloudflared tunnel login

# Create tunnel
cloudflared tunnel create nlp-service

# Run tunnel
cloudflared tunnel --url http://localhost:8001 run nlp-service
```

→ Cloudflare sẽ cho domain: `https://nlp-service-xxxxx.trycloudflare.com`

---

## Cost Comparison

| Method | Setup | Monthly Cost | Uptime | Speed |
|--------|-------|--------------|--------|-------|
| **Self-host** | 30 min | $2-3 điện | 99%* | Fastest |
| **Koyeb** | 10 min | $0 | 99% | Medium |
| **Render Paid** | 5 min | $25 | 99.9% | Fast |

*Phụ thuộc internet nhà và điện

---

## Monitoring

**Setup uptime monitoring:**

1. **UptimeRobot** (free):
   - https://uptimerobot.com
   - Add monitor: `http://mynlp.ddns.net:8001/health`
   - Alert qua email nếu down

2. **Healthchecks.io**:
   - https://healthchecks.io
   - Ping endpoint mỗi 5 phút

**Check logs định kỳ:**
```powershell
# Daily log summary
Get-Content nlp-service\logs\service_stdout.log | Select-String "ERROR|WARNING" | Select-Object -Last 20
```
