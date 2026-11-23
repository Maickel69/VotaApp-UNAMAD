param(
    [Parameter(Mandatory = $true)][string]$docxPath,
    [Parameter(Mandatory = $true)][string]$pdfPath
)

$ErrorActionPreference = "Stop"

$fullDocxPath = (Resolve-Path -LiteralPath $docxPath).Path
$fullPdfPath  = [System.IO.Path]::GetFullPath($pdfPath)

$word = $null
$doc  = $null
$failed = $false

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0 # wdAlertsNone

    $doc = $word.Documents.Open($fullDocxPath, $false, $true)
    $doc.Repaginate()
    $doc.ExportAsFixedFormat($fullPdfPath, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)
    Write-Host "PDF_CONVERTED_SUCCESS"
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    $failed = $true
}
finally {
    if ($null -ne $doc) {
        try { $doc.Close($false) } catch {}
        try { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) | Out-Null } catch {}
        $doc = $null
    }
    if ($null -ne $word) {
        try { $word.Quit($false) } catch {}
        try { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null } catch {}
        $word = $null
    }
    [System.GC]::Collect()
    [System.GC]::WaitForPendingFinalizers()
}

if ($failed) {
    exit 1
}
