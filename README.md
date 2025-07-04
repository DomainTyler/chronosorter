
# ChronoSorter

[![Version](https://img.shields.io/badge/version-1.0-blue?style=for-the-badge)]()
[![License: MIT](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)]()
[![Platform](https://img.shields.io/badge/platform-Windows-blue?style=for-the-badge&logo=windows)]()
[![Made with Love](https://img.shields.io/badge/Made%20with-%E2%9D%A4%EF%B8%8F-red?style=for-the-badge)]()

ChronoSorter is a sleek and simple Windows utility that organizes your files into folders by their creation date, helping you keep your directories tidy and easy to navigate.

---

## 💡 Usage

1. Run `chronosorter.exe`.  
2. Click **Select Folder** to pick the folder you want to organize.  
3. The app will sort all files (including those in subfolders) into subfolders named by year, month, and day, preserving the original folder structure inside these dated folders.  
4. Optionally, you can **Undo** the last sorting to revert changes.

---

## 🛠️ Features

- Organizes files by their **creation date** into `Year/Month/Day` folders.  
- Recursively sorts all files in selected folder and its subfolders.  
- Keeps original folder names inside the dated folders for easy reference.  
- Undo option to revert the last sorting operation.  
- Modern, sleek light/dark mode interface with toggle.  
- Minimal dependencies and easy to use.

---

## ⚙️ Requirements

- Windows 10 or later.  
- No Python installation required (packed as standalone executable).  
- Runs natively on Windows PCs.

---

## 🧰 Development & Contribution

Want to improve or customize ChronoSorter?

- Clone the repo and modify the Python source (`chronosorter.py`).  
- Use [PyInstaller](https://www.pyinstaller.org/) to rebuild the executable:

```bash
pyinstaller --noconsole --onefile --windowed chronosorter.py
```

- Open a pull request or suggest features on GitHub.

---

## 🆘 Support

- For help or issues, please open an issue on the GitHub repository.  
- Feature requests and bug reports are welcome.

---

## 📜 License

This project is licensed under the MIT License.

---

<p align="center">Made with ❤️ by <a href="https://github.com/YourGitHubUsername">Your Name</a></p>
