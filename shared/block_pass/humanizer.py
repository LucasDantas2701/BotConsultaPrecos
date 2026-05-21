import random
import time



def espera(min_s=1, max_s=3):
    time.sleep(random.uniform(min_s, max_s))


def mover_mouse(page):
    page.mouse.move(
        random.randint(100, 800),
        random.randint(100, 600),
        steps=random.randint(10, 30)
    )


def digitar_humano(locator, texto):
    locator.click()

    for letra in texto:
        locator.type(letra, delay=random.randint(50, 180))
