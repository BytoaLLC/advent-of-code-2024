from pathlib import Path

def part_one(set1, set2):

    set3 = []

    for i in range(len(set1)):
        set3.append(abs(set2[i]-set1[i]))

    return sum(set3)


def part_two(set1, set2):

    set3 = []

    for i in set1:
        set3.append(len([thing for thing, x in enumerate(set2) if x == i])*i)

    return sum(set3)


def main():
    
    PROJECT_DIR = Path(__file__).parent
    set1 = []
    set2 = []

    with open(PROJECT_DIR/'input.txt', 'r') as file:
        for line in file:
            set1.append(int(line.split()[0]))
            set2.append(int(line.split()[1]))
    set1 = sorted(set1)
    set2 = sorted(set2)

    print(part_one(set1, set2))
    print(part_two(set1, set2))

if __name__=="__main__":
    main()