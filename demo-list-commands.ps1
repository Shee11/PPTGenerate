#!/usr/bin/env pwsh
# UCE Render CLI - List Commands Demo Script

Write-Host "`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   UCE Render CLI - Asset Listing Commands Demo           ║" -ForegroundColor Cyan
Write-Host "╚═══════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# 1. List Widgets
Write-Host "`n[1] List All Available Widgets" -ForegroundColor Yellow
Write-Host "Command: uce-render --list-widgets`n" -ForegroundColor Gray
python -m cli.uce_render --list-widgets | Select-Object -First 30

# 2. List Strategies
Write-Host "`n`n[2] List All Layout Strategies" -ForegroundColor Yellow
Write-Host "Command: uce-render --list-strategies`n" -ForegroundColor Gray
python -m cli.uce_render --list-strategies

# 3. List Themes
Write-Host "`n`n[3] List All Available Themes" -ForegroundColor Yellow
Write-Host "Command: uce-render --list-themes`n" -ForegroundColor Gray
python -m cli.uce_render --list-themes | Select-Object -First 25

# 4. List Styles
Write-Host "`n`n[4] List All Available Styles" -ForegroundColor Yellow
Write-Host "Command: uce-render --list-styles`n" -ForegroundColor Gray
python -m cli.uce_render --list-styles | Select-Object -First 25

# 5. JSON Format Demo
Write-Host "`n`n[5] JSON Format Output (Widget Types)" -ForegroundColor Yellow
Write-Host "Command: uce-render --list-widgets --format json | jq '.[].type'`n" -ForegroundColor Gray
python -m cli.uce_render --list-widgets --format json | python -m json.tool | Select-String '"type":'

Write-Host "`n`n[6] JSON Format Output (Strategy Names)" -ForegroundColor Yellow
Write-Host "Command: uce-render --list-strategies --format json | jq '.[].name'`n" -ForegroundColor Gray
python -m cli.uce_render --list-strategies --format json | python -m json.tool | Select-String '"name":'

Write-Host "`n`n╔═══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   Summary                                                 ║" -ForegroundColor Green
Write-Host "╚═══════════════════════════════════════════════════════════╝" -ForegroundColor Green

Write-Host "`nAvailable Commands:" -ForegroundColor Cyan
Write-Host "  --list-widgets      : List 8 widget types (Type, Data, Media)" -ForegroundColor White
Write-Host "  --list-strategies   : List 10 layout strategies (Bento, Swiss, Cinematic)" -ForegroundColor White
Write-Host "  --list-themes       : List 2 themes (corp_modern, minimal_dark)" -ForegroundColor White
Write-Host "  --list-styles       : List 2 styles with theme mappings" -ForegroundColor White

Write-Host "`nOutput Formats:" -ForegroundColor Cyan
Write-Host "  (default)           : Human-readable formatted output" -ForegroundColor White
Write-Host "  --format json       : Machine-readable JSON output" -ForegroundColor White

Write-Host "`nFor more information: uce-render --help`n" -ForegroundColor Gray
