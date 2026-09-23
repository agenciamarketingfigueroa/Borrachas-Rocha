$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing

Add-Type -ReferencedAssemblies 'System.Drawing.dll' -TypeDefinition @'
using System;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Imaging;
using System.IO;

public static class BrandLogoBackground
{
    private static bool IsBackground(Color color)
    {
        if (color.A == 0) return true;
        int min = Math.Min(color.R, Math.Min(color.G, color.B));
        int max = Math.Max(color.R, Math.Max(color.G, color.B));
        return min >= 216 && max - min <= 50;
    }

    public static int Remove(string path)
    {
        string temporary = path + ".transparent.png";
        int changed = 0;

        using (Bitmap source = new Bitmap(path))
        using (Bitmap result = source.Clone(
            new Rectangle(0, 0, source.Width, source.Height),
            PixelFormat.Format32bppArgb))
        {
            int width = source.Width;
            int height = source.Height;
            bool[] visited = new bool[width * height];
            Queue<int> pending = new Queue<int>();

            Action<int, int> enqueue = (x, y) =>
            {
                int index = y * width + x;
                if (visited[index]) return;
                visited[index] = true;
                if (IsBackground(source.GetPixel(x, y))) pending.Enqueue(index);
            };

            for (int x = 0; x < width; x++)
            {
                enqueue(x, 0);
                enqueue(x, height - 1);
            }
            for (int y = 0; y < height; y++)
            {
                enqueue(0, y);
                enqueue(width - 1, y);
            }

            while (pending.Count > 0)
            {
                int index = pending.Dequeue();
                int x = index % width;
                int y = index / width;
                if (source.GetPixel(x, y).A != 0)
                {
                    result.SetPixel(x, y, Color.Transparent);
                    changed++;
                }
                if (x > 0) enqueue(x - 1, y);
                if (x + 1 < width) enqueue(x + 1, y);
                if (y > 0) enqueue(x, y - 1);
                if (y + 1 < height) enqueue(x, y + 1);
            }

            // The PDF extraction left a few isolated colored pixels beside some marks.
            Array.Clear(visited, 0, visited.Length);
            for (int start = 0; start < visited.Length; start++)
            {
                if (visited[start]) continue;
                visited[start] = true;
                if (result.GetPixel(start % width, start / width).A == 0) continue;

                List<int> component = new List<int>();
                pending.Enqueue(start);
                while (pending.Count > 0)
                {
                    int current = pending.Dequeue();
                    component.Add(current);
                    int x = current % width;
                    int y = current / width;
                    for (int dy = -1; dy <= 1; dy++)
                    for (int dx = -1; dx <= 1; dx++)
                    {
                        int nextX = x + dx;
                        int nextY = y + dy;
                        if (nextX < 0 || nextX >= width || nextY < 0 || nextY >= height) continue;
                        int next = nextY * width + nextX;
                        if (visited[next]) continue;
                        visited[next] = true;
                        if (result.GetPixel(nextX, nextY).A > 0) pending.Enqueue(next);
                    }
                }
                if (component.Count >= 12) continue;
                foreach (int pixel in component)
                {
                    result.SetPixel(pixel % width, pixel / width, Color.Transparent);
                    changed++;
                }
            }

            result.Save(temporary, ImageFormat.Png);
        }

        File.Copy(temporary, path, true);
        File.Delete(temporary);
        return changed;
    }
}
'@

$logoDirectory = Join-Path $PSScriptRoot '..\assets\img\montadoras'
Get-ChildItem -LiteralPath $logoDirectory -Filter '*.png' | ForEach-Object {
    $pixels = [BrandLogoBackground]::Remove($_.FullName)
    Write-Output ('{0}: {1} pixels de fundo removidos' -f $_.Name, $pixels)
}
