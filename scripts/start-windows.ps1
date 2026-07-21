$ErrorActionPreference = "Stop"
Set-Location (Join-Path $PSScriptRoot "..")

docker compose up -d --build

Write-Output "Backend:  http://localhost:8000"
Write-Output "Frontend: http://localhost:3000"
