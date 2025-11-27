# ActionVFX-Sample-Player

ActionVFX-Sample-Player is a lightweight technical demo that showcases how to interact with the **public ActionVFX API** to fetch thumbnails, load metadata, and play video clips inside a simple interface built with **PySide6 (Qt)** and **OpenCV**.

This project is **not** part of the official ActionVFX plugin and contains **no internal or proprietary logic**.  
Instead, it serves as a public-facing example that demonstrates how a basic VFX media browser or asset viewer can be structured.

---

## 🎯 Features

- Fetches product data from the **public ActionVFX API**
- Displays clip thumbnails in a horizontal gallery
- Loads preview images on selection
- Plays MP4 video directly from remote URLs using OpenCV
- Clean and simple **PySide6** UI
- Playback controls (Play, Pause, Stop)
- Extensible structure suitable for more advanced tools

---

## 📦 Requirements

Install the dependencies:

```bash
pip install PySide6 opencv-python
