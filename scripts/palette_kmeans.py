#!/usr/bin/env python3
"""palette_kmeans.py — K-means palette extraction for Omarchy themes.

Reads one or more images, extracts the dominant colors, prints hex + coverage
+ luminance per color. Feed the hero painting (or several candidates) and pick
a dark-mode base + one saturated accent from the output. Comment each color
with its source painting in colors.toml.

Usage: python3 palette_kmeans.py <image> [image ...]
Requires: pillow, numpy
"""
import sys, os
import numpy as np
from PIL import Image

def load_pixels(path, samples=2, resize=900):
    im = Image.open(path).convert('RGB')
    w, h = im.size
    pixels = []
    for s in range(samples):
        # sample different horizontal slices for multi-scene crops
        left = s * (w // samples)
        crop = im.crop((left, 0, left + w // samples, h))
        crop = crop.resize((resize, max(1, int(resize * h / w / samples))), Image.LANCZOS)
        pixels.append(np.asarray(crop, dtype=np.float32))
    return np.concatenate([p.reshape(-1, 3) for p in pixels], axis=0)

def kmeans(X, k=12, iters=25, seed=7):
    rng = np.random.default_rng(seed)
    # k-means++ style init (simplified)
    idx = rng.choice(len(X), size=k, replace=False)
    C = X[idx].copy()
    for _ in range(iters):
        labels = np.empty(len(X), dtype=np.int32)
        B = 200000
        for i in range(0, len(X), B):
            d = ((X[i:i+B, None, :] - C[None, :, :]) ** 2).sum(-1)
            labels[i:i+B] = d.argmin(1)
        for j in range(k):
            m = labels == j
            if m.any():
                C[j] = X[m].mean(0)
    counts = np.bincount(labels, minlength=k)
    return C, counts

def hexc(c):
    return '#%02x%02x%02x' % tuple(int(round(v)) for v in c)

def describe(path):
    X = load_pixels(path)
    C, counts = kmeans(X, k=12)
    order = np.argsort(-counts)
    out = []
    total = counts.sum()
    for i in order:
        c = C[i]
        lum = 0.2126*c[0] + 0.7152*c[1] + 0.0722*c[2]
        out.append((hexc(c), int(counts[i]), round(100*counts[i]/total, 1), int(lum)))
    return out

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    for path in sys.argv[1:]:
        if not os.path.exists(path):
            print(f'not found: {path}', file=sys.stderr)
            continue
        print('====', os.path.basename(path), '====')
        for h, n, pct, lum in describe(path):
            print(f'{h}  {pct:5.1f}%  lum={lum}')
