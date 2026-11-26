from pathlib import Path
from html.parser import HTMLParser
import re, subprocess, json

ROOT = Path(__file__).resolve().parent
html = (ROOT / 'index.html').read_text(encoding='utf-8')
assert '<title>Survival World' in html
assert html.count('<script type="module">') == 1

class IdParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.ids=[]
    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key == 'id': self.ids.append(value)

parser=IdParser(); parser.feed(html)
assert len(parser.ids) == len(set(parser.ids)), 'duplicate DOM IDs'

module=re.search(r'<script type="module">(.*?)</script>', html, re.S).group(1)
check_file=ROOT / 'SurvivalWorld-check.mjs'
check_file.write_text(module, encoding='utf-8')
subprocess.run(['node','--check',str(check_file)],check=True)

required = [
    'makeHumanoid', 'animateRig', 'spawnZombie', 'collect', 'attack', 'craft',
    'placeBuild', 'depositResources', 'withdrawResources', 'save', 'load',
    'startChallenge', 'startContest', 'duelPractice', 'cameraYaw', 'cameraPitch',
    'pointermove', 'localRecords', 'storedResources', 'placedBuilds', 'survivalSeconds'
]
for token in required:
    assert token in html, f'missing feature marker: {token}'

required_ids = [
    'stick','collect','hit','place','craftAxe','craftSpear','craftBandage',
    'craftWall','craftDoor','craftChest','craftFire','save','load','eat',
    'deposit','withdraw','cosmetic','challenge','contest','duel'
]
for item in required_ids:
    assert item in parser.ids, f'missing control: {item}'

# Guard the touch camera path against undefined PointerEvent movementX/Y.
touch_branch = re.search(r"if\(e\.pointerType==='touch'\)\{(.*?)\}else\{dx=e\.movementX", html, re.S)
assert touch_branch and 'clientX-lookLastX' in touch_branch.group(1)
assert 'e.movementX*lookSensitivity' not in html

# Ensure save/load persists the state needed by the current local prototype.
for token in ['placedBuilds:placedBuilds.map', 'storedResources', 'collected:objects.map', 'cameraYaw,cameraPitch']:
    assert token in html, f'missing persistence field: {token}'

print(json.dumps({
    'html_bytes': len(html.encode('utf-8')),
    'embedded_module_chars': len(module),
    'unique_dom_ids': len(parser.ids),
    'javascript_syntax': 'PASS',
    'feature_assertions': 'PASS',
    'touch_camera_regression_check': 'PASS',
    'save_load_static_check': 'PASS'
}, ensure_ascii=False, indent=2))
