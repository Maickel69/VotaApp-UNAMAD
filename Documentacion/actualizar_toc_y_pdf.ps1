param(
    [Parameter(Mandatory = $true)][string]$DocxPath,
    [Parameter(Mandatory = $false)][string]$WordCraftCopyPath = "",
    [Parameter(Mandatory = $true)][string]$PdfPath
)

$ErrorActionPreference = "Stop"

# Constantes numericas WdBuiltinStyle (independientes del idioma de Office)
$wdStyleHeading1         = -2
$wdStyleHeading2         = -3
$wdStyleHeading3         = -4
$wdStyleTOC1             = -20
$wdStyleTOC2             = -21
$wdStyleTOC3             = -22
$wdStyleHyperlink        = -86
$wdStyleHyperlinkFollowed = -87

$fullDocxPath = (Resolve-Path -LiteralPath $DocxPath).Path
$fullPdfPath  = [System.IO.Path]::GetFullPath($PdfPath)
$fullCopyPath = if ([string]::IsNullOrWhiteSpace($WordCraftCopyPath)) { "" } else { [System.IO.Path]::GetFullPath($WordCraftCopyPath) }

function Set-BuiltinStyleFont {
    param(
        $Document,
        [int]$StyleId,
        [string]$FontName = "Arial",
        [double]$FontSize = 0,
        [int]$Bold = -999,
        [int]$Italic = -999
    )
    $st = $Document.Styles.Item($StyleId)
    $st.Font.Name = $FontName
    $st.Font.Color = 0 # wdColorBlack
    $st.Font.Underline = 0 # wdUnderlineNone
    if ($FontSize -gt 0) {
        $st.Font.Size = $FontSize
    }
    if ($Bold -ne -999) {
        $st.Font.Bold = $Bold
    }
    if ($Italic -ne -999) {
        $st.Font.Italic = $Italic
    }
    return $st
}

function Apply-TocAndHeadingStyles {
    param($Document)

    # Estilos de Titulos (Heading 1 / 2 / 3)
    Set-BuiltinStyleFont -Document $Document -StyleId $wdStyleHeading1 -FontName "Arial" -FontSize 13   -Bold 1 -Italic 0 | Out-Null
    Set-BuiltinStyleFont -Document $Document -StyleId $wdStyleHeading2 -FontName "Arial" -FontSize 11.5 -Bold 1 -Italic 0 | Out-Null
    Set-BuiltinStyleFont -Document $Document -StyleId $wdStyleHeading3 -FontName "Arial" -FontSize 11   -Bold 1 -Italic 0 | Out-Null

    # Estilos TOC 1 / 2 / 3
    $sToc1 = Set-BuiltinStyleFont -Document $Document -StyleId $wdStyleTOC1 -FontName "Arial" -FontSize 9.5 -Bold 1 -Italic 0
    $sToc1.ParagraphFormat.LineSpacingRule = 0 # wdLineSpaceSingle
    $sToc1.ParagraphFormat.SpaceBefore = 2
    $sToc1.ParagraphFormat.SpaceAfter = 1
    $sToc1.ParagraphFormat.LeftIndent = 0
    $sToc1.ParagraphFormat.FirstLineIndent = 0
    $sToc1.ParagraphFormat.RightIndent = 0

    $sToc2 = Set-BuiltinStyleFont -Document $Document -StyleId $wdStyleTOC2 -FontName "Arial" -FontSize 9.0 -Bold 0 -Italic 0
    $sToc2.ParagraphFormat.LineSpacingRule = 0
    $sToc2.ParagraphFormat.SpaceBefore = 0.5
    $sToc2.ParagraphFormat.SpaceAfter = 0.5
    $sToc2.ParagraphFormat.LeftIndent = 12
    $sToc2.ParagraphFormat.FirstLineIndent = 0
    $sToc2.ParagraphFormat.RightIndent = 0

    $sToc3 = Set-BuiltinStyleFont -Document $Document -StyleId $wdStyleTOC3 -FontName "Arial" -FontSize 8.5 -Bold 0 -Italic 0
    $sToc3.ParagraphFormat.LineSpacingRule = 0
    $sToc3.ParagraphFormat.SpaceBefore = 0
    $sToc3.ParagraphFormat.SpaceAfter = 0
    $sToc3.ParagraphFormat.LeftIndent = 24
    $sToc3.ParagraphFormat.FirstLineIndent = 0
    $sToc3.ParagraphFormat.RightIndent = 0

    # Estilos Hyperlink y HyperlinkFollowed en negro sin subrayado
    Set-BuiltinStyleFont -Document $Document -StyleId $wdStyleHyperlink         -FontName "Arial" | Out-Null
    Set-BuiltinStyleFont -Document $Document -StyleId $wdStyleHyperlinkFollowed -FontName "Arial" | Out-Null
}

function Update-AllFieldsPass {
    param($Document, $TocObject)

    $Document.Repaginate()
    if ($null -ne $TocObject) {
        $TocObject.Update()
    }
    $Document.Fields.Update() | Out-Null

    foreach ($tbl in $Document.Tables) {
        foreach ($cell in $tbl.Range.Cells) {
            if ($cell.Range.Fields.Count -gt 0) {
                $cell.Range.Fields.Update() | Out-Null
            }
        }
    }

    foreach ($sec in $Document.Sections) {
        foreach ($hf in $sec.Headers) {
            if ($hf.Range.Fields.Count -gt 0) {
                $hf.Range.Fields.Update() | Out-Null
            }
            foreach ($htbl in $hf.Range.Tables) {
                foreach ($hcell in $htbl.Range.Cells) {
                    if ($hcell.Range.Fields.Count -gt 0) {
                        $hcell.Range.Fields.Update() | Out-Null
                    }
                }
            }
        }
        foreach ($hf in $sec.Footers) {
            if ($hf.Range.Fields.Count -gt 0) {
                $hf.Range.Fields.Update() | Out-Null
            }
            foreach ($ftbl in $hf.Range.Tables) {
                foreach ($fcell in $ftbl.Range.Cells) {
                    if ($fcell.Range.Fields.Count -gt 0) {
                        $fcell.Range.Fields.Update() | Out-Null
                    }
                }
            }
        }
    }

    $Document.Repaginate()
}

$word = $null
$doc  = $null
$toc  = $null
$failed = $false

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $word.DisplayAlerts = 0 # wdAlertsNone

    $doc = $word.Documents.Open($fullDocxPath, $false, $false)

    # Buscar marcador [[TOC_INTERACTIVO_WORD]]
    $findRange = $doc.Content.Duplicate
    $findObj = $findRange.Find
    $findObj.ClearFormatting()
    $found = $findObj.Execute("[[TOC_INTERACTIVO_WORD]]")
    if (-not $found) {
        throw "No se encontro el marcador [[TOC_INTERACTIVO_WORD]] en $fullDocxPath"
    }
    $findRange.Text = ""

    # Configurar estilos antes de generar el TOC para fijar alturas de linea definitivas
    Apply-TocAndHeadingStyles -Document $doc

    # Insertar TOC nativo interactivo (niveles 1..3, hipervinculos activos, puntos guia)
    $toc = $doc.TablesOfContents.Add($findRange, $true, 1, 3, $false, "", $true, $true, "", $true, $true, $true)
    $toc.TabLeader = 1 # wdTabLeaderDots

    # Reaplicar estilos tras crear el TOC
    Apply-TocAndHeadingStyles -Document $doc

    # Dos pasadas completas de repaginacion y actualizacion de TOC + PAGEREF + headers/footers
    Update-AllFieldsPass -Document $doc -TocObject $toc
    Update-AllFieldsPass -Document $doc -TocObject $toc

    # Reaplicar Arial negro sin subrayado directamente sobre el rango del TOC y estilos Hyperlink (sin desvincular campos)
    $toc.Range.Font.Name = "Arial"
    $toc.Range.Font.Color = 0
    $toc.Range.Font.Underline = 0
    Set-BuiltinStyleFont -Document $doc -StyleId $wdStyleHyperlink         -FontName "Arial" | Out-Null
    Set-BuiltinStyleFont -Document $doc -StyleId $wdStyleHyperlinkFollowed -FontName "Arial" | Out-Null

    $doc.Repaginate()
    $doc.Save()

    # Exportar PDF con marcadores de encabezados (CreateBookmarks = 1 -> wdExportCreateHeadingBookmarks)
    $doc.ExportAsFixedFormat($fullPdfPath, 17, $false, 0, 0, 1, 1, 0, $true, $true, 1, $true, $true, $false)
    Write-Host "TOC_AND_PDF_UPDATED_SUCCESS"
}
catch {
    [Console]::Error.WriteLine("ERROR: $($_.Exception.Message)")
    $failed = $true
}
finally {
    if ($null -ne $toc) {
        try { [System.Runtime.InteropServices.Marshal]::ReleaseComObject($toc) | Out-Null } catch {}
        $toc = $null
    }
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

# Copiar DOCX sincronizado DESPUES de cerrar Microsoft Word
if (-not [string]::IsNullOrWhiteSpace($fullCopyPath)) {
    Copy-Item -LiteralPath $fullDocxPath -Destination $fullCopyPath -Force
    Write-Host "WORDCRAFT_COPY_SYNCED: $fullCopyPath"
}
