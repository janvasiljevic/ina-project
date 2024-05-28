import fileinput
import os


def fix_names(file):
    with fileinput.FileInput(file, inplace=True, backup=".bak", encoding="utf-8") as f:
        print(next(f), end="")

        for line in f:
            if line.startswith("*"):
                print(line, end="")
                break

            line = line.replace('""', '"').replace("*", "").replace("'", "")
            line_split = line.split()

            pos = 1 if "python" in file else 6
            if len(line_split) > pos and line_split[pos].lower() in [
                "ph",
                "r",
                "q",
                "ic",
                "bc",
                "bw",
                "lc",
                "la",
                "lr",
                "phi",
                "lphi",
                "fod",
                "font",
                "url",
                "fos",
            ]:
                line_split[pos] = f"_{line_split[pos]}"

            if len(line_split) > 8:
                if line_split[8] in ['"https://github', '"http://github']:
                    line_split.remove(line_split[8])
                    line_split.remove(line_split[7])
                if line_split[8].count('"') == 3:
                    line_split[8] = line_split[8].replace('"', "")

            # :ohm:
            if len(line_split) > 8:
                if "onclick=alert(09876543)" in line_split[8]:
                    line_split[8] = line_split[8].replace('"', "")

            print(" ".join(line_split))

        for line in f:
            print(line, end="")


for file in os.listdir("."):
    if "npm" in file and file.endswith(".net"):
        print(f"Fixing {file}")
        fix_names(file)
