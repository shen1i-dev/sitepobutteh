<#
PowerShell helper to ensure Docker Desktop is installed/running and then run docker compose.
Usage: Run this script in project root as Administrator or normal user.
#>

function Write-Info($msg){ Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Warn($msg){ Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Err($msg){ Write-Host "[ERROR] $msg" -ForegroundColor Red }

# 1) Check docker CLI
$dockerCmd = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerCmd) {
    Write-Warn "Docker CLI not found in PATH."
    # Try winget install if available
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Info "Attempting to install Docker Desktop via winget (requires administrative privileges)..."
        try {
            Start-Process -FilePath winget -ArgumentList 'install', '--id', 'Docker.DockerDesktop', '-e' -Wait -NoNewWindow
            Write-Info "winget installation finished. Please start Docker Desktop if it did not start automatically."
        } catch {
            Write-Err "winget install failed: $_"
            Write-Info "Please install Docker Desktop manually: https://www.docker.com/get-started"
            exit 1
        }
    } else {
        Write-Err "winget not available. Please install Docker Desktop manually: https://www.docker.com/get-started"
        exit 1
    }
} else {
    Write-Info "Docker CLI found: $($dockerCmd.Path)"
}

# 2) Start Docker Desktop if not running (try known install path)
function Start-DockerDesktopIfNeeded {
    $proc = Get-Process -Name 'Docker Desktop' -ErrorAction SilentlyContinue
    if ($proc) { Write-Info "Docker Desktop process is running."; return }
    # Try common install locations
    $paths = @("$Env:ProgramFiles\Docker\Docker\Docker Desktop.exe", "$Env:ProgramFiles(x86)\Docker\Docker\Docker Desktop.exe")
    $started = $false
    foreach ($p in $paths) {
        if (Test-Path $p) {
            Write-Info "Starting Docker Desktop from: $p"
            Start-Process -FilePath $p
            $started = $true
            break
        }
    }
    if (-not $started) {
        Write-Warn "Could not find Docker Desktop executable automatically. If Docker was installed via WSL/other method, please start Docker Desktop or the Docker daemon manually."
    }
}

Start-DockerDesktopIfNeeded

# 3) Wait for docker daemon to be ready
$timeoutSec = 180
$interval = 3
$elapsed = 0
Write-Info "Waiting for Docker daemon to be available (timeout ${timeoutSec}s)..."
while ($elapsed -lt $timeoutSec) {
    try {
        $info = docker info --format '{{json .}}' 2>$null
        if ($LASTEXITCODE -eq 0) { Write-Info "Docker daemon is ready."; break }
    } catch { }
    Start-Sleep -Seconds $interval
    $elapsed += $interval
    Write-Host -NoNewline '.'
}

if ($elapsed -ge $timeoutSec) {
    Write-Err "Timed out waiting for Docker daemon. Ensure Docker Desktop is running and try again."; exit 1
}

# 4) Run docker compose up
Write-Info "Building and starting services with docker compose..."
$composeCmd = Get-Command 'docker' -ErrorAction SilentlyContinue
if (-not $composeCmd) { Write-Err "docker command not found after installation."; exit 1 }

# Use 'docker compose' if supported, else fallback to docker-compose
$useDockerCompose = $false
try { docker compose version > $null 2>&1; if ($LASTEXITCODE -eq 0) { $useDockerCompose = $true } } catch { }

if ($useDockerCompose) {
    docker compose up -d --build
} else {
    # try docker-compose
    $dc = Get-Command docker-compose -ErrorAction SilentlyContinue
    if ($dc) {
        docker-compose up -d --build
    } else {
        Write-Err "Neither 'docker compose' nor 'docker-compose' is available. Install Docker Desktop with Compose support."; exit 1
    }
}

# 5) Show status and recent logs
Write-Info "Services status:"
if ($useDockerCompose) { docker compose ps } else { docker-compose ps }

Write-Info "Showing last 200 lines of web service logs:"
if ($useDockerCompose) { docker compose logs --tail 200 web } else { docker-compose logs --tail 200 web }

Write-Info "Done. If containers started, open http://localhost:5000 or check the logs above."