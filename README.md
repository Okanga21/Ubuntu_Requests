# 🖼️ Multi-Image Fetcher

A Python script that fetches images from given URLs, stores them neatly in a `Fetched_Images` folder, and applies safety checks to ensure responsible downloading.  

This tool follows **Ubuntu principles**:  
- **Community**: Connects to the wider web to fetch resources.  
- **Respect**: Handles errors gracefully without crashing.  
- **Sharing**: Organizes downloaded images for reuse.  
- **Practicality**: Provides a useful tool for saving and managing images.  

---

## 🚀 Features
- 📥 Download **one or multiple images at once** (separate URLs with spaces).  
- 🔄 **Duplicate prevention** → Identical images are skipped using SHA-256 hashing.  
- 🛡️ **Security precautions** →  
  - Only saves files with valid `image/*` MIME types.  
  - Skips files larger than 10MB (configurable).  
- 📂 Stores all images in a `Fetched_Images/` directory.  
- ⚠️ Handles errors like timeouts, connection issues, and invalid responses gracefully.  

---

## 📦 Requirements
- Python 3.7+  
- [requests](https://pypi.org/project/requests/) library  

Install dependencies:
```bash
pip install requests
