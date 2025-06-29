# 🕸️ PyHttrack — Mirror Your Favorite Web to Your Computer!

PyHttrack is a lightweight and powerful Python tool that allows you to download entire websites directly to your local computer for offline access, archive, or content analysis. Inspired by the legendary HTTrack, PyHttrack comes with a modern approach, is easily customizable, and can be integrated in various automated workflows.

![Image](https://github.com/user-attachments/assets/4eeb7a42-48b2-4c00-81bd-274abd7bbe75)

### 🔍 Top Features:

- 🌐 Download Full Website - HTML, CSS, JS, images and other media directly to local directory.
- ⚙️ Flexible Configuration - Specify crawl depth, file extensions, domain limits and more.
- 🖥️ Simple CLI Interface - Run and monitor processes with easy-to-understand commands.
- 📁 Organized Directory Structure - Keeps the original structure of the site for an identical offline experience.
- 🧩 Easy to Customize - Suitable for developers, researchers, and digital archivists.

### 🛠️ Use Case:

- Save important site documentation before going offline
- Perform local SEO crawling & analysis
- Learn to build a site from real examples
- Backup personal content or public blogs

## 🚀 Get Started

### Installation

```bash
pip install -r requirements.txt
```

### Configuration

Edit the web.json file and add the url of the website you want to download, for example the following :

```json
["https://example.com/xxx/xxx"]
```

or download many websites

```json
[
  "https://example.com/xxx/xxx",
  "https://example.com/xxx/xxx",
  "https://example.com/xxx/xxx"
]
```

### Start Download

Run the following command to start the download :

```bash
python pyhttrack.py
```

## 📥 Latest Release

[Click here](https://github.com/riodevnet/PyHttrack/releases/latest) to get the latest version of PyHttrack.

## 🤝 Contribution

Contributions are very welcome!. Please feel free to fork this repo, create an issue, or submit a pull request for new features or performance improvements 🚀
