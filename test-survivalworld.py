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

# Execute the actual collision helper extracted from the game's embedded module.
helper_start = module.index('const collisionRects=[];')
helper_end = module.index('const buildingMaterials=', helper_start)
collision_helper = module[helper_start:helper_end]
collision_test = ROOT / 'SurvivalWorld-collision-test.mjs'
collision_test.write_text(collision_helper + r'''
// Mock the collision rectangles of a 10x10 house with a 1.15m front doorway.
const w=10,d=10,t=.32,doorW=1.15;
addCollider(0,-d/2,w,t); addCollider(-w/2+t/2,0,t,d); addCollider(w/2-t/2,0,t,d);
const sideW=(w-doorW)/2;addCollider(-doorW/2-sideW/2,d/2,sideW,t);addCollider(doorW/2+sideW/2,d/2,sideW,t);
if(collidesAt(0,5,.38))throw new Error('doorway is blocked');
if(!collidesAt(4.9,0,.38))throw new Error('side wall collision missing');
const actor={position:{x:0,z:6}};moveWithCollision(actor,0,-2,.38);if(actor.position.z>=5.6)throw new Error('actor could not move through doorway');
const trapped={position:{x:4.7,z:0}};moveWithCollision(trapped,.5,0,.38);if(trapped.position.x>4.7)throw new Error('actor walked through solid wall');
''',encoding='utf-8')
subprocess.run(['node',str(collision_test)],check=True)

required = [
    'makeHumanoid', 'animateRig', 'spawnZombie', 'collect', 'attack', 'craft',
    'placeBuild', 'depositResources', 'withdrawResources', 'save', 'load',
    'addCollider', 'collidesAt', 'moveWithCollision', 'doorW', 'staticColliderCount',
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

assert 'if(py-hh/2<2.0)addCollider' in html, 'upper doorway lintel must not block the entrance'
assert 'moveWithCollision(player' in html and 'moveWithCollision(zz.mesh' in html, 'player/zombie collision-aware movement missing'
assert 'wall(-doorW/2-sideW/2' in html and 'wall(doorW/2+sideW/2' in html, 'door opening is not split into walk-through wall segments'

print(json.dumps({
    'html_bytes': len(html.encode('utf-8')),
    'embedded_module_chars': len(module),
    'unique_dom_ids': len(parser.ids),
    'javascript_syntax': 'PASS',
    'feature_assertions': 'PASS',
    'touch_camera_regression_check': 'PASS',
    'save_load_static_check': 'PASS',
    'building_collision_and_doorway_static_check': 'PASS',
    'collision_helper_runtime_unit_test': 'PASS'
}, ensure_ascii=False, indent=2))
