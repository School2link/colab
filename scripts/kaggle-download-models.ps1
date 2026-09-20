#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Downloads AI models to Kaggle one-by-one and publishes as datasets.

.DESCRIPTION
    For each model:
    1. Copies notebook to push folder with correct metadata
    2. Pushes to Kaggle (auto-executes)
    3. Polls status until complete
    4. Moves to next model

    Each notebook auto-publishes its model as a permanent Kaggle dataset.

.NOTES
    Run from: C:\xampp\htdocs\LocalContents
    Requires: Kaggle CLI configured (~/.kaggle/kaggle.json)
#>

param(
    [string]$StartFrom = "wan21",
    [switch]$SkipWan21,
    [switch]$SkipAnimatediff,
    [switch]$SkipSd15,
    [switch]$SkipBark,
    [switch]$SkipSadtalker,
    [switch]$SkipWav2lip
)

$ErrorActionPreference = "Continue"

# Configuration
$MODELS = @(
    @{ Name="wan21"; Slug="download-wan-2-1"; Notebook="download-wan21.ipynb"; Dataset="kingtechie/wan21-model"; Size="6.5GB"; HF="Wan-AI/Wan2.1-T2V-1.3B" }
    @{ Name="animatediff"; Slug="download-animatediff"; Notebook="download-animatediff.ipynb"; Dataset="kingtechie/animatediff-model"; Size="3.5GB"; HF="guoyww/animatediff" }
    @{ Name="sd15"; Slug="download-sd15"; Notebook="download-sd15.ipynb"; Dataset="kingtechie/sd15-model"; Size="3.2GB"; HF="runwayml/stable-diffusion-v1-5" }
    @{ Name="bark"; Slug="download-bark"; Notebook="download-bark.ipynb"; Dataset="kingtechie/bark-model"; Size="4.5GB"; HF="suno/bark" }
    @{ Name="sadtalker"; Slug="download-sadtalker"; Notebook="download-sadtalker.ipynb"; Dataset="kingtechie/sadtalker-model"; Size="2.5GB"; HF="camenduru/SadTalker" }
    @{ Name="wav2lip"; Slug="download-wav2lip"; Notebook="download-wav2lip.ipynb"; Dataset="kingtechie/wav2lip-model"; Size="1.5GB"; HF="numz/wav2lip_studio-0.2" }
)

$ROOT_DIR = $PSScriptRoot | Split-Path -Parent
$PUSH_DIR = Join-Path $ROOT_DIR "kaggle-push"
$COLAB_DIR = Join-Path $ROOT_DIR "colab"

# Track results
$Results = @()

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  Fako Online - Kaggle Model Downloader" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Models to download: $($MODELS.Count)" -ForegroundColor Yellow
Write-Host ""

foreach ($model in $MODELS) {
    # Check skip flags
    $skipVar = "Skip$($model.Name.Substring(0,1).ToUpper() + $model.Name.Substring(1))"
    if ($SkipWan21 -and $model.Name -eq "wan21") { continue }
    if ($SkipAnimatediff -and $model.Name -eq "animatediff") { continue }
    if ($SkipSd15 -and $model.Name -eq "sd15") { continue }
    if ($SkipBark -and $model.Name -eq "bark") { continue }
    if ($SkipSadtalker -and $model.Name -eq "sadtalker") { continue }
    if ($SkipWav2lip -and $model.Name -eq "wav2lip") { continue }

    Write-Host "`n--------------------------------------------" -ForegroundColor Cyan
    Write-Host "  Model: $($model.Name) ($($model.Size))" -ForegroundColor White
    Write-Host "  Dataset: $($model.Dataset)" -ForegroundColor Gray
    Write-Host "  HuggingFace: $($model.HF)" -ForegroundColor Gray
    Write-Host "--------------------------------------------" -ForegroundColor Cyan

    # Step 1: Create kernel-metadata.json
    $kernelMeta = @{
        id = "fako-online/$($model.Slug)"
        title = "Fako Online - Download $($model.Name)"
        code_file = $model.Notebook
        language = "python"
        kernel_type = "notebook"
        is_private = $true
        enable_gpu = $false
        enable_tpu = $false
        enable_internet = $true
        dataset_sources = @()
        kernel_sources = @()
        competition_sources = @()
        model_sources = @()
    }
    $kernelMeta | ConvertTo-Json -Depth 10 | Set-Content (Join-Path $PUSH_DIR "kernel-metadata.json") -Force

    # Step 2: Copy notebook to push folder
    $notebookSrc = Join-Path $COLAB_DIR $model.Notebook
    $notebookDst = Join-Path $PUSH_DIR $model.Notebook
    Copy-Item $notebookSrc $notebookDst -Force
    Write-Host "`n  [1/4] Notebook copied to push folder" -ForegroundColor Green

    # Step 3: Push to Kaggle (auto-executes)
    Write-Host "  [2/4] Pushing to Kaggle..." -ForegroundColor Yellow
    $pushOutput = kaggle kernels push -p $PUSH_DIR 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "  ERROR: Push failed!" -ForegroundColor Red
        $Results += @{ Model=$model.Name; Status="FAILED"; Error="Push failed" }
        continue
    }
    Write-Host "  Pushed successfully!" -ForegroundColor Green

    # Step 4: Poll status
    Write-Host "  [3/4] Waiting for completion..." -ForegroundColor Yellow
    $maxWait = 1800  # 30 minutes max
    $elapsed = 0
    $kernelSlug = "fako-online/$($model.Slug)"

    while ($elapsed -lt $maxWait) {
        Start-Sleep -Seconds 60
        $elapsed += 60
        $status = kaggle kernels status $kernelSlug 2>&1
        $minutes = [math]::Floor($elapsed / 60)
        Write-Host "  [$minutes min] $status" -ForegroundColor Gray

        if ($status -match "complete") {
            Write-Host "  Completed!" -ForegroundColor Green
            $Results += @{ Model=$model.Name; Status="SUCCESS"; Dataset=$model.Dataset }
            break
        }
        elseif ($status -match "error" -or $status -match "failed") {
            Write-Host "  FAILED!" -ForegroundColor Red
            $Results += @{ Model=$model.Name; Status="FAILED"; Error=$status }
            break
        }
    }

    if ($elapsed -ge $maxWait) {
        Write-Host "  TIMEOUT after 30 minutes!" -ForegroundColor Red
        $Results += @{ Model=$model.Name; Status="TIMEOUT" }
    }

    # Step 5: Brief pause between models
    Write-Host "  [4/4] Waiting 10s before next model..." -ForegroundColor Gray
    Start-Sleep -Seconds 10
}

# Summary
Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  SUMMARY" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan

$success = ($Results | Where-Object { $_.Status -eq "SUCCESS" }).Count
$failed = ($Results | Where-Object { $_.Status -ne "SUCCESS" }).Count

Write-Host "  Successful: $success / $($Results.Count)" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "  Failed: $failed / $($Results.Count)" -ForegroundColor Red
}

Write-Host "`n  Datasets:" -ForegroundColor Yellow
foreach ($r in $Results) {
    $color = if ($r.Status -eq "SUCCESS") { "Green" } else { "Red" }
    Write-Host "    $($r.Model): $($r.Status)" -ForegroundColor $color
}

Write-Host "`n============================================" -ForegroundColor Cyan
Write-Host "  Done!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
