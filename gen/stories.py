import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(__file__))
from render import BG, BOX, OR, PU, WH, GR, B, R, M, wrap, draw_lines
from content import HANDLE

# Stories 1080x1920. t: tip | prompt | teaser | cta
STORIES = [
 ("2026-10-14", {"t": "tip", "tag": "TRUCO DEL DÍA", "title": "Pega el contexto antes de pedir nada", "sub": "Qué vendes, a quién, qué le preocupa y cómo hablas. La IA deja de sonar genérica."}),
 ("2026-10-15", {"t": "teaser", "title": "Hoy a las 20:00", "sub": "Por qué la IA puede escribirte un mes de contenido (y por qué casi nadie lo consigue)."}),
 ("2026-10-16", {"t": "prompt", "tag": "PROMPT GRATIS", "title": "Ideas que tu cliente sí quiere leer", "code": "Haz una lista de las 25 preguntas que más se hace [CLIENTE] antes de comprar [PRODUCTO]. Ordénalas de más a menos urgente."}),
 ("2026-10-17", {"t": "tip", "tag": "DATO", "title": "Tienes 1,5 segundos", "sub": "Es lo que tarda alguien en decidir si para el scroll. Escribe 20 ganchos y quédate con el mejor."}),
 ("2026-10-18", {"t": "cta", "title": "Mañana es el último día a 9 €", "sub": "160 prompts, calendario de 30 días y 50 ganchos."}),
 ("2026-10-19", {"t": "cta", "title": "Último día a 9 €", "sub": "Esta noche sube a 17 €. Descarga inmediata."}),
 ("2026-10-20", {"t": "prompt", "tag": "PROMPT GRATIS", "title": "Desmonta mitos de tu sector", "code": "Identifica 10 mitos o creencias falsas que [CLIENTE] tiene sobre [PROBLEMA] y cómo desmontar cada uno en un post."}),
 ("2026-10-21", {"t": "tip", "tag": "TRUCO DEL DÍA", "title": "Pide formato, no ideas", "sub": "«Carrusel de 8 diapositivas, la 1 es el gancho» funciona mucho mejor que «dame ideas»."}),
 ("2026-10-22", {"t": "teaser", "title": "Hoy a las 20:00", "sub": "5 cambios para que la IA escriba como tú y no como un robot."}),
 ("2026-10-23", {"t": "prompt", "tag": "PROMPT GRATIS", "title": "Humor que conecta", "code": "Crea un guion tipo POV («POV: eres [CLIENTE] y...») con humor sobre [PROBLEMA]."}),
 ("2026-10-24", {"t": "tip", "tag": "CHECKLIST", "title": "Antes de publicar", "sub": "¿La primera línea para el scroll? ¿Habla de un problema de tu cliente? ¿Dice qué hacer ahora?"}),
 ("2026-10-25", {"t": "prompt", "tag": "PROMPT GRATIS", "title": "Recicla lo que ya tienes", "code": "Convierte este texto largo [PEGA TEXTO, BLOG O NOTA DE VOZ TRANSCRITA] en 7 piezas de contenido distintas para [RED]."}),
 ("2026-10-26", {"t": "teaser", "title": "Halloween es el sábado", "sub": "Hoy a las 20:00: 3 prompts para aprovecharlo aunque no vendas disfraces."}),
 ("2026-10-27", {"t": "tip", "tag": "TRUCO DEL DÍA", "title": "Números concretos, no redondos", "sub": "«37 clientas» es más creíble que «muchas clientas». Pídele a la IA ganchos con cifras exactas."}),
 ("2026-10-28", {"t": "prompt", "tag": "PROMPT GRATIS", "title": "Vídeos sin enseñar la cara", "code": "Dame 10 ideas de vídeos sin mostrar la cara para [NEGOCIO]."}),
 ("2026-10-29", {"t": "cta", "title": "Todo esto sale de un PDF", "sub": "160 prompts en 8 categorías. Funciona con la IA gratis."}),
 ("2026-10-30", {"t": "teaser", "title": "Noviembre en una tarde", "sub": "Hoy a las 20:00, el método en 4 pasos. Black Friday incluido."}),
]

def story(s):
    W, H = 1080, 1920
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.ellipse((W - 380, -300, W + 220, 300), fill=OR)
    d.ellipse((-140, H - 520, 220, H - 160), fill=PU)
    X, TW = 80, W - 160
    y = 420
    if s.get("tag"):
        f = B(34); bw = d.textlength(s["tag"], font=f)
        d.rounded_rectangle((X, y, X + bw + 50, y + 70), radius=10, fill=OR)
        d.text((X + 25, y + 15), s["tag"], font=f, fill=WH); y += 130
    y = draw_lines(d, X, y, wrap(d, s["title"], B(84), TW), B(84), WH, 100) + 40
    if s["t"] == "prompt":
        cl = wrap(d, s["code"], M(40), TW - 80)
        d.rounded_rectangle((X - 10, y, W - X + 10, y + 80 + len(cl) * 58), radius=22, fill=BOX)
        y = draw_lines(d, X + 30, y + 40, cl, M(40), (230, 230, 240), 58) + 80
        d.text((X, y), "Guárdalo y pruébalo hoy", font=B(42), fill=OR)
    else:
        y = draw_lines(d, X, y, wrap(d, s["sub"], R(48), TW), R(48), GR, 66) + 60
        if s["t"] == "cta":
            d.rounded_rectangle((X, y, W - X, y + 130), radius=20, fill=OR)
            bt = "Enlace en el perfil"; f = B(50)
            d.text(((W - d.textlength(bt, font=f)) / 2, y + 35), bt, font=f, fill=WH)
    d.text(((W - d.textlength(HANDLE, font=B(34))) / 2, H - 130), HANDLE, font=B(34), fill=GR)
    return im

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for date, s in STORIES:
        story(s).save(os.path.join(out, f"story-{date}.png"))
    print(len(STORIES))
