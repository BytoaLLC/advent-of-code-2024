from pathlib import Path
import re

def main():
    PROJECT_DIR = Path(__file__).parent

    res, valid = [0, 0], 1
    with open(PROJECT_DIR/'input.txt', 'r') as f:
        data = f.read()
        regex = r"(do\(\))|(don't\(\))|(mul\((\d+),(\d+)\))"

        for match in re.findall(regex, data):
            if match[0]:
                valid = 1
            elif match[1]:
                valid = 0
            else:
                x = int(match[3]) * int(match[4])
                res[0] += x
                res[1] += x * valid
    print(res)

if __name__=="__main__":
    main() 