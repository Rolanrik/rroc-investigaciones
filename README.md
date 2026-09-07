# rroc-investigaciones

Investigaciones nocturnas automatizadas de **Rroc** (objetivo: IA independiente).

## Como funciona
- Cada noche a las 00:00 (-05) GitHub Actions ejecuta `investigar.py`.
- Usa Groq (`openai/gpt-oss-120b`, gratis) y guarda el resultado en `resultados/AAAA-MM-DD.md`.
- Ejecucion manual: pestana Actions → "Investigacion nocturna Rroc" → Run workflow (puedes dar un tema).

## Configuracion inicial (una sola vez)
1. **Workflow:** crea el archivo `.github/workflows/nightly.yml` con el contenido de `workflows/nightly.yml` (Add file → Create new file en la web; luego puedes borrar la carpeta `workflows/`).
2. **Secret:** Settings → Secrets and variables → Actions → New repository secret. Nombre: `GROQ_API_KEY`, valor: tu key de https://console.groq.com/keys.
3. Listo. La proxima madrugada corre solo.

Minutos gratis: repo publico = ilimitado.
