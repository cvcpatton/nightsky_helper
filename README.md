# Denver Nightsky Helper (Python, December 2025)
Python program using Skyfield (library) to calculate stargazing times and visible celestial objects with CSV export for the Denver area.  


**Tech Stack**  

* Python  
* Skyfield library  
* Data structures: Dictionaries, Lists  
* File I/O: CSV

Live Demo, added:
* Backend: Flask, SQLAlchemy
* Frontend: HTML5, CSS3, Bootstrap 5 (Jinja templates), Render
* Database: SQLite

**Features**  

* Computes sunset, dark sky, and sunrise times for Denver coordinates  
* Identifies visible planets and stars for chosen dates  
* Allows saving results to a CSV log for multi-day trip planning  
* Menu-driven interface with loops and input validation
* Web scraping moon illumination data (advanced version)

**Versions**  

* Basic version to run the program in console, available now (Oct 2025) 
* Full version using OOP and web scraping moon phases (Dec 2025)

**Live Demo 🚀** 
[Denver Nightsky Helper - Live Demo](https://cvcpatton.github.io/nightsky_helper/loading.html) (Hosted on Render)

**Potential Upgrades**  

* Modification for other location coordinates (this program defaults to Denver, Colorado, USA coordinates)  
* Weather API integration to check for cloud cover or precipitation  
* Moon phase/brightness that might interfere with viewing objects  
* Add a calendar of known celestial events such as meteor showers for additional results output

**Sample Output**  
![Sample Output](nightsky_helper_output.jpg "Sample Output")

**External Data Source**  
[Moon Illumination Data Source: isaacbernat](https://raw.githubusercontent.com/isaacbernat/moon-data/main/moon_phases_UTC_1800-2050.csv)  

**Instructor Feedback**  
"Your Nightsky Helper demonstrates excellent understanding of modular program design, function documentation, and file handling. Each core function is clearly written, properly commented, and performs a distinct, single purpose. The program structure and pseudocode flow logically from user input to output, and your testing functions show thoughtful attention to verifying correctness. This submission is organized, user-friendly, and demonstrates both technical and creative strength. Excellent job."  

Final project feedback: "Your final project is outstanding and shows a very high level of technical depth and creativity ... The separation of concerns across multiple modules shows excellent Python engineering practice. This is a highly polished project that demonstrates advanced problem solving skills, real world relevance, and strong mastery of external libraries."

**How to Run**  

```bash  
git clone https://github.com/cvcpatton/nightsky-helper.git  
cd nightsky-helper  
python nightsky-basic.py  
```
"Advanced" version instructions are in the README file in the nightsky-oop folder. 

**License**  
MIT License, Copyright (c) 2026 Catherine Patton  

This project was created as part of my programming coursework. Please do not reproduce or distribute without proper credit. For questions about use, contact me.
