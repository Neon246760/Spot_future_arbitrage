from pathlib import Path

current_path = Path(__file__)
program_path = current_path.parent.parent.parent


if __name__ == '__main__':
    print(program_path)