
param([string]$docxPath, [string]$pdfPath)
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    # 17 is wdFormatPDF
    $doc.SaveAs([ref]$pdfPath, [ref]17)
    $doc.Close()
    Write-Host "PDF_CONVERTED_SUCCESS"
} catch {
    Write-Host "ERROR: $($_.Exception.Message)"
} finally {
    $word.Quit()
}
