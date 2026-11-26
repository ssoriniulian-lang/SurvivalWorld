from pathlib import Path
import re, subprocess, json
html=Path('/mnt/data/SurvivalWorld.html').read_text()
assert '<title>Survival World' in html
assert html.count('<script type="module">') == 1
ids=re.findall(r'id="([^"]+)"',html)
assert len(ids)==len(set(ids)), 'duplicate IDs'
required=['spawnZombie','collect','attack','craft','placeBuild','save','load','eat','startChallenge','startContest','duelPractice','dayTime','totalGathered','missionIndex','cameraYaw','cameraPitch','lookPointer','pointermove','camOffset']
for token in required: assert token in html, f'missing implementation marker: {token}'
for el in ['stick','collect','hit','place','craftAxe','craftBandage','craftWall','craftDoor','craftChest','craftFire','save','load','eat','challenge','contest','duel']:
 assert el in ids, f'missing control id: {el}'
module=re.search(r'<script type="module">(.*?)</script>',html,re.S).group(1)
Path('/mnt/data/SurvivalWorld-check.mjs').write_text(module)
subprocess.run(['node','--check','/mnt/data/SurvivalWorld-check.mjs'],check=True)
print(json.dumps({'html_bytes':len(html.encode()),'script_chars':len(module),'unique_dom_ids':len(ids),'js_parse':'PASS','static_feature_assertions':'PASS'},indent=2))
