import json
import os
from pathlib import Path
from core.grade import parse_grade


if __name__ == "__main__":
    if not os.path.exists('result'):
        os.mkdir('result')

    with open('result/grade.json', 'w') as f:
        f.write(json.dumps(parse_grade()))
