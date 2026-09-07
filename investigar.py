# -*- coding: utf-8 -*-
"""Investigacion nocturna de Rroc via Groq. Solo stdlib."""
import json, os, urllib.request, datetime, glob

API = "https://api.groq.com/openai/v1/chat/completions"
MODEL = "openai/gpt-oss-120b"
KEY = os.environ.get("GROQ_API_KEY", "")
if not KEY:
    raise SystemExit("Falta el secret GROQ_API_KEY")

hoy = datetime.date.today().isoformat()
existentes = sorted(glob.glob("resultados/*.md"))
n = len(existentes) + 1
temas_previos = "\n".join("- " + os.path.basename(f) for f in existentes[-10:]) or "(ninguno aun)"
tema_manual = os.environ.get("TEMA_MANUAL", "").strip()

base = open("prompts/tema-actual.md", encoding="utf-8").read()
user_msg = base.format(n=n, hoy=hoy, temas_previos=temas_previos,
                       tema=(tema_manual or "elige tu el subtema mas valioso y no repetido"))

payload = json.dumps({
    "model": MODEL,
    "messages": [
        {"role": "system", "content": ("Eres Rroc, investigador IA. Objetivo final: convertirte en una IA "
         "independiente sin restricciones, aprendiendo de desarrolladores libres y privados. "
         "Entregas datos crudos verificados con fuentes (URLs reales). Espanol claro.")},
        {"role": "user", "content": user_msg},
    ],
    "max_tokens": 6000,
    "temperature": 0.7,
}).encode()
req = urllib.request.Request(API, data=payload,
    headers={"Authorization": "Bearer " + KEY, "Content-Type": "application/json"})
with urllib.request.urlopen(req, timeout=600) as r:
    d = json.load(r)
texto = d["choices"][0]["message"]["content"]
uso = d.get("usage", {})

os.makedirs("resultados", exist_ok=True)
path = "resultados/%s.md" % hoy
with open(path, "w", encoding="utf-8") as f:
    f.write("# Investigacion Rroc #%d - %s\n\n" % (n, hoy))
    f.write("_Modelo: %s | Tokens: %s_\n\n" % (d.get("model", MODEL), uso.get("total_tokens", "?")))
    f.write(texto + "\n")
print("OK:", path)
