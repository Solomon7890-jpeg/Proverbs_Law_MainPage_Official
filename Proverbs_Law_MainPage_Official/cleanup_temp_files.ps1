# Cleanup temporary RovoDev files
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ProVerBs - Cleaning Temporary Files" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$rootPath = Split-Path -Parent $MyInvocation.MyCommand.Path | Split-Path -Parent

# Find all tmp_rovodev_ files
$tempFiles = Get-ChildItem -Path $rootPath -Filter "tmp_rovodev_*" -File -Recurse

Write-Host "Found $($tempFiles.Count) temporary files:" -ForegroundColor Yellow
Write-Host ""

foreach ($file in $tempFiles) {
    Write-Host "  - $($file.Name)" -ForegroundColor Gray
}

Write-Host ""
$confirm = Read-Host "Delete these files? (Y/N)"

if ($confirm -eq "Y" -or $confirm -eq "y") {
    foreach ($file in $tempFiles) {
        try {
            Remove-Item $file.FullName -Force
            Write-Host "✅ Deleted: $($file.Name)" -ForegroundColor Green
        } catch {
            Write-Host "❌ Failed to delete: $($file.Name)" -ForegroundColor Red
        }
    }
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "✅ Cleanup Complete!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
} else {
    Write-Host "Cleanup cancelled." -ForegroundColor Yellow
}

Write-Host ""
pause
