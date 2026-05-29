import random
import time

def espera(min_s=1, max_s=3):
    time.sleep(random.uniform(min_s, max_s))

async def mover_mouse(page):
    await page.mouse.move(
        random.randint(100, 800),
        random.randint(100, 600),
        steps=random.randint(10, 30)
    )

async def digitar_humano(locator, texto):
    await locator.click()

    for letra in texto:
        await locator.type(
            letra,
            delay=random.randint(50, 180)
        )
