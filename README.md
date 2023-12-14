# ⭐ Advent of Code 2023 🎄
[AoC 2023 webpage](https://adventofcode.com/2023)

---
### 🛠 Tools
- Language: Python 3.10.12
- IDE: PyCharm
- Package control: pip 23.3.1
- OS: Ubuntu 22.04

---

### 🏗 Setup
0. Install python3: `sudo apt install python3`
1. Install venv: `sudo apt install python3-virtualenv`
2. Create a venv: `virtualenv -p python3 aoc-env`
3. Activate the venv: `source aoc-env/bin/activate`
4. Install requirements: `pip3 install -r requirements.txt`
5. Prepare files per day: `./setup_day.sh x`, replace `x` with current day of month
6. Move into day `XY` directory: `cd XY/`
7. Run code for part `P`, day `XY`: `python3 dayXY.py P` - e.g. `python3 day01.py 2` for part 2 of day 1.
    - a) To run with example input, add any non-zero integer as a second argument, i.e. `python3 dayXY.py P 1`
    - b) Example input will be taken from `./example_input.txt` for part 1 and `example_input2.txt` for part 2

---