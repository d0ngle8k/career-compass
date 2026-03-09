# Install script for NLP Service as Windows Service
# Run this with Administrator privileges

param(
    [Parameter(Mandatory=$false)]
    [int]$Port = 8001
)

Write-Host "=== Career Compass NLP Service - Windows Service Installer ===" -ForegroundColor Cyan
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    exit 1
}

# Define paths
$ServiceName = "CareerCompassNLP"
$ServiceDisplayName = "Career Compass NLP Service"
$ServiceDescription = "Python FastAPI service for CV/JD scoring with ML models"
$ProjectRoot = $PSScriptRoot
$NlpServiceDir = Join-Path $ProjectRoot "nlp-service"
$PythonExe = "python"
$StartScript = Join-Path $NlpServiceDir "start_service.py"

Write-Host "Project Root: $ProjectRoot" -ForegroundColor Gray
Write-Host "NLP Service Dir: $NlpServiceDir" -ForegroundColor Gray
Write-Host "Port: $Port" -ForegroundColor Gray
Write-Host ""

# Step 1: Check Python installation
Write-Host "[1/6] Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = & $PythonExe --version 2>&1
    Write-Host "Found: $pythonVersion" -ForegroundColor Green
    if ($pythonVersion -notmatch "Python 3\.(10|11|12)") {
        Write-Host "WARNING: Python 3.10, 3.11, or 3.12 recommended" -ForegroundColor Yellow
    }
} catch {
    Write-Host "ERROR: Python not found. Install Python 3.11 from https://python.org" -ForegroundColor Red
    exit 1
}

# Step 2: Install dependencies
Write-Host "[2/6] Installing Python dependencies..." -ForegroundColor Yellow
Push-Location $NlpServiceDir
try {
    & $PythonExe -m pip install --upgrade pip
    & $PythonExe -m pip install -r requirements.txt
    Write-Host "Dependencies installed successfully" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to install dependencies: $_" -ForegroundColor Red
    Pop-Location
    exit 1
}
Pop-Location

# Step 3: Create start script
Write-Host "[3/6] Creating start script..." -ForegroundColor Yellow
$StartScriptContent = @"
import sys
import os
import uvicorn
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('nlp_service.log'),
        logging.StreamHandler()
    ]
)

if __name__ == "__main__":
    logging.info("Starting Career Compass NLP Service...")
    logging.info(f"Port: $Port")
    logging.info(f"Working directory: {os.getcwd()}")
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=$Port,
        log_level="info",
        access_log=True
    )
"@

Set-Content -Path $StartScript -Value $StartScriptContent -Encoding UTF8
Write-Host "Start script created: $StartScript" -ForegroundColor Green

# Step 4: Install NSSM (Non-Sucking Service Manager)
Write-Host "[4/6] Installing NSSM (Service Manager)..." -ForegroundColor Yellow
$nssmUrl = "https://nssm.cc/release/nssm-2.24.zip"
$nssmZip = Join-Path $env:TEMP "nssm.zip"
$nssmDir = Join-Path $env:TEMP "nssm-2.24"
$nssmExe = Join-Path $nssmDir "win64\nssm.exe"

if (-not (Test-Path $nssmExe)) {
    Write-Host "Downloading NSSM..." -ForegroundColor Gray
    Invoke-WebRequest -Uri $nssmUrl -OutFile $nssmZip
    Expand-Archive -Path $nssmZip -DestinationPath $env:TEMP -Force
    Write-Host "NSSM downloaded and extracted" -ForegroundColor Green
} else {
    Write-Host "NSSM already downloaded" -ForegroundColor Green
}

# Step 5: Stop and remove existing service if exists
Write-Host "[5/6] Checking for existing service..." -ForegroundColor Yellow
$existingService = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
if ($existingService) {
    Write-Host "Stopping existing service..." -ForegroundColor Yellow
    & $nssmExe stop $ServiceName
    Start-Sleep -Seconds 2
    Write-Host "Removing existing service..." -ForegroundColor Yellow
    & $nssmExe remove $ServiceName confirm
    Start-Sleep -Seconds 2
    Write-Host "Existing service removed" -ForegroundColor Green
}

# Step 6: Install and configure service
Write-Host "[6/6] Installing Windows Service..." -ForegroundColor Yellow

# Install service
& $nssmExe install $ServiceName $PythonExe "$StartScript"
& $nssmExe set $ServiceName AppDirectory $NlpServiceDir
& $nssmExe set $ServiceName DisplayName $ServiceDisplayName
& $nssmExe set $ServiceName Description $ServiceDescription
& $nssmExe set $ServiceName Start SERVICE_AUTO_START

# Set log files
$LogDir = Join-Path $NlpServiceDir "logs"
if (-not (Test-Path $LogDir)) {
    New-Item -ItemType Directory -Path $LogDir | Out-Null
}
& $nssmExe set $ServiceName AppStdout (Join-Path $LogDir "service_stdout.log")
& $nssmExe set $ServiceName AppStderr (Join-Path $LogDir "service_stderr.log")
& $nssmExe set $ServiceName AppRotateFiles 1
& $nssmExe set $ServiceName AppRotateBytes 10485760  # 10MB

Write-Host ""
Write-Host "=== Service Installed Successfully! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Service Name: $ServiceName" -ForegroundColor Cyan
Write-Host "Display Name: $ServiceDisplayName" -ForegroundColor Cyan
Write-Host "Port: $Port" -ForegroundColor Cyan
Write-Host "Logs: $LogDir" -ForegroundColor Cyan
Write-Host ""
Write-Host "To start the service, run:" -ForegroundColor Yellow
Write-Host "  Start-Service $ServiceName" -ForegroundColor White
Write-Host ""
Write-Host "To check status:" -ForegroundColor Yellow
Write-Host "  Get-Service $ServiceName" -ForegroundColor White
Write-Host ""
Write-Host "To view logs:" -ForegroundColor Yellow
Write-Host "  Get-Content '$LogDir\service_stdout.log' -Tail 50 -Wait" -ForegroundColor White
Write-Host ""
Write-Host "Starting service now..." -ForegroundColor Yellow
Start-Service $ServiceName
Start-Sleep -Seconds 3

$status = Get-Service $ServiceName
if ($status.Status -eq 'Running') {
    Write-Host "✓ Service is running!" -ForegroundColor Green
} else {
    Write-Host "✗ Service failed to start. Check logs in $LogDir" -ForegroundColor Red
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Configure Windows Firewall (see below)" -ForegroundColor White
Write-Host "2. Setup port forwarding on your router" -ForegroundColor White
Write-Host "3. Configure DDNS (if you have dynamic IP)" -ForegroundColor White
Write-Host ""

# Configure Windows Firewall
Write-Host "Would you like to configure Windows Firewall now? (Y/N)" -ForegroundColor Yellow
$response = Read-Host
if ($response -eq 'Y' -or $response -eq 'y') {
    Write-Host "Adding firewall rule..." -ForegroundColor Yellow
    New-NetFirewallRule -DisplayName "Career Compass NLP Service" `
        -Direction Inbound `
        -Protocol TCP `
        -LocalPort $Port `
        -Action Allow `
        -Profile Any `
        -ErrorAction SilentlyContinue
    Write-Host "✓ Firewall rule added for port $Port" -ForegroundColor Green
}
