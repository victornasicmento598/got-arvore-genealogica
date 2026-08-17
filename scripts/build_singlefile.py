import base64, io, json, os
from PIL import Image
os.chdir("/home/user/got/site")

def enc(path, maxw, q):
    im = Image.open(path).convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height*maxw/im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=q, optimize=True, progressive=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

data = json.load(open("data.json"))
ids = sorted({n["id"] for t in data["tabs"] for n in t["nodes"]})
T = {p: enc("img/t/%s.jpg" % p, 150, 66) for p in ids if os.path.exists("img/t/%s.jpg" % p)}
F = {p: enc("img/f/%s.jpg" % p, 400, 58) for p in ids if os.path.exists("img/f/%s.jpg" % p)}
mb = lambda o: len(json.dumps(o, separators=(",", ":"))) / 1e6
print("thumbs %d (%.1f MB)  fulls %d (%.1f MB)" % (len(T), mb(T), len(F), mb(F)))

html = open("index.html").read(); css = open("style.css").read(); js = open("app.js").read()

subs = [
  ("""'<figure><img loading="lazy" src="img/t/' + n.id + '.jpg" alt="'""",
   """'<figure><img loading="lazy" src="' + window.__T__[n.id] + '" alt="'"""),
  ('''"img/f/" + n.id + ".jpg"''', '''window.__F__[n.id]'''),
  # preserva o callback .then(function (d) {  — só troca a origem dos dados
  ('''fetch("data.json").then(function (r) { return r.json(); }).then(function (d) {''',
   '''Promise.resolve(window.__DATA__).then(function (d) {'''),
]
for old, new in subs:
    assert js.count(old) == 1, "nao achei: %s" % old[:60]
    js = js.replace(old, new)
assert "img/t/" not in js and "img/f/" not in js and "data.json" not in js

boot = ("<script>window.__DATA__=" + json.dumps(data, separators=(",", ":")) +
        ";window.__T__=" + json.dumps(T, separators=(",", ":")) +
        ";window.__F__=" + json.dumps(F, separators=(",", ":")) + ";</script>")
out = html.replace('<link rel="stylesheet" href="style.css">', "<style>\n" + css + "\n</style>")
assert "style.css" not in out
out = out.replace('<script src="app.js"></script>', boot + "\n<script>\n" + js + "\n</script>")
assert 'src="app.js"' not in out and "__DATA__" in out
open("/home/user/got/arvore-westeros.html", "w").write(out)
print("bytes: %.1f MB" % (os.path.getsize("/home/user/got/arvore-westeros.html") / 1e6))
