# Prepara para o site os 33 recortes transparentes usados na revisão 02 do PDF.
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$source = Join-Path $root 'output/catalogo-pu-2026-por-montadora/revisao-02/recortes'
$destination = Join-Path $root ('assets/img/Pe' + [char]0x00E7 + 'as de PU/recortes')

Add-Type -ReferencedAssemblies 'System.Drawing' -TypeDefinition @'
using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Runtime.InteropServices;

public static class SiteCutout {
    public static void Prepare(string source, string target) {
        using (var image = new Bitmap(source)) {
            var area = new Rectangle(0, 0, image.Width, image.Height);
            var pixels = image.LockBits(area, ImageLockMode.ReadOnly, PixelFormat.Format32bppArgb);
            var bytes = new byte[Math.Abs(pixels.Stride) * image.Height];
            Marshal.Copy(pixels.Scan0, bytes, 0, bytes.Length);
            image.UnlockBits(pixels);

            int left = image.Width, top = image.Height, right = -1, bottom = -1;
            for (int y = 0; y < image.Height; y++) {
                for (int x = 0; x < image.Width; x++) {
                    if (bytes[y * pixels.Stride + x * 4 + 3] > 12) {
                        if (x < left) left = x;
                        if (x > right) right = x;
                        if (y < top) top = y;
                        if (y > bottom) bottom = y;
                    }
                }
            }
            if (right < left || bottom < top) throw new Exception("Imagem sem produto visível: " + source);

            int width = right - left + 1, height = bottom - top + 1;
            int margin = Math.Max(2, (int)Math.Round(Math.Max(width, height) * .04));
            var crop = Rectangle.FromLTRB(Math.Max(0, left - margin), Math.Max(0, top - margin),
                Math.Min(image.Width, right + margin + 1), Math.Min(image.Height, bottom + margin + 1));
            double scale = Math.Min(1, 900.0 / Math.Max(crop.Width, crop.Height));
            int targetWidth = (int)Math.Round(crop.Width * scale);
            int targetHeight = (int)Math.Round(crop.Height * scale);
            using (var output = new Bitmap(targetWidth, targetHeight, PixelFormat.Format32bppArgb))
            using (var graphics = Graphics.FromImage(output)) {
                graphics.Clear(Color.Transparent);
                graphics.CompositingMode = CompositingMode.SourceCopy;
                graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
                graphics.PixelOffsetMode = PixelOffsetMode.HighQuality;
                graphics.DrawImage(image, new Rectangle(0, 0, targetWidth, targetHeight), crop, GraphicsUnit.Pixel);
                output.Save(target, ImageFormat.Png);
            }
        }
    }
}
'@

$files = @(Get-ChildItem -LiteralPath $source -File -Filter '*.png')
if ($files.Count -ne 33) { throw "Esperadas 33 fotos; encontradas $($files.Count)." }
New-Item -ItemType Directory -Path $destination -Force | Out-Null
foreach ($file in $files) {
    [SiteCutout]::Prepare($file.FullName, (Join-Path $destination $file.Name))
}
Write-Output "Preparadas $($files.Count) fotos em $destination"
