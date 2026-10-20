# Animated evidence package

Six offline, data-backed animations are available as interactive HTML and as square and portrait video export targets: RC circuit, second-order chemistry, Newton cooling, Snell refraction, paired mutation campaign, and a bounded formal typecheck control. The distinct 3D flow clip is illustrative context only. All assets are local drafts; none have been uploaded.

The shared scene renderer consumes `manifest.json`, which is generated from the selected evidence records and includes their SHA-256 hashes. Standalone HTML files inline the renderer and evidence data, so they work offline. The canvases distinguish analytic reconstructions from recorded solver checkpoints where applicable. Attribution: **Cristian Guerra · QA Automation · Medellín, Colombia · @criguex**.

## Build and test

From the repository root:

```sh
python3 animations/build.py
python3 -m unittest discover -s animations -p 'test_*.py'
```

The existing Remotion adapter registers `RC`, `Chemistry`, `Cooling`, `Snell`, `Campaign`, `Formal` plus a `Vertical` variant of each. With the existing pinned video dependencies installed, render for example:

```sh
cd video
npx remotion render src/animations-entry.tsx RC ../media/animations/rc.mp4
npx remotion render src/animations-entry.tsx RCVertical ../media/animations/rc-vertical.mp4
```

Repeat with the other composition IDs. GIFs can be derived from reviewed MP4 exports with FFmpeg, for example:

```sh
ffmpeg -i media/animations/rc.mp4 -vf 'fps=12,scale=540:-1:flags=lanczos,palettegen' -y /tmp/rc-palette.png
ffmpeg -i media/animations/rc.mp4 -i /tmp/rc-palette.png -lavfi 'fps=12,scale=540:-1:flags=lanczos[x];[x][1:v]paletteuse' -loop 0 media/animations/rc.gif
```

The portrait composition places the square visual inside a 1080×1920 canvas with a title and attribution safe area. These are export dimensions, not a guarantee that every platform accepts every encoding. Check current platform requirements before adapting or uploading: [TikTok](https://support.tiktok.com/en/using-tiktok/creating-videos/creator-tools-on-tiktok), [YouTube Shorts](https://support.google.com/youtube/answer/12779649), [YouTube video uploads](https://support.google.com/youtube/answer/1722171), [LinkedIn](https://www.linkedin.com/help/linkedin/answer/a551346), and [X](https://help.x.com/en/using-x/x-videos). No upload has occurred; autoplay behavior is platform-controlled. MP4/GIF preserve the animation but not HTML controls; standalone HTML retains playback and seek controls.

See [index.html](index.html) for the local gallery and [publication.json](publication.json) for unposted copy and asset paths.
