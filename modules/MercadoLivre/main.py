import os
from playwright.async_api import async_playwright
from modules.MercadoLivre.lista import ml_locators
from shared.block_pass.humanizer import espera, mover_mouse, digitar_humano
from modules.link_shortner.main import shortner
from modules.item_filter.main import item_relevante

state_path = "assets/mercadolivre_state.json"

async def mercadolivre(pesquisa):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True,args=["--disable-blink-features=AutomationControlled"])
        context = await browser.new_context(
            storage_state=state_path if os.path.exists(state_path) else None,
            user_agent=("Mozilla/5.0 (Windows NT 10.0; Win64; x64) ""AppleWebKit/537.36 (KHTML, like Gecko) ""Chrome/136.0.0.0 Safari/537.36"),
            viewport={"width": 1366, "height": 768},
            locale="pt-BR"
        )
        page = await context.new_page()
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)
        await page.goto(ml_locators["url"])
        espera(2, 4)
        await mover_mouse(page)
        search = page.get_by_role("combobox", name="Digite o que você quer")
        resultados = []
        if await search.is_visible():
            espera(1, 2)
            await digitar_humano(search, pesquisa)
            espera(1, 2)
            await search.press("Enter")
            espera(3, 5)
            cards = page.locator(ml_locators["card"])
            mostrados = 0
            if await cards.count() > 0:
                for i in range(await cards.count()):

                    if mostrados == 2:
                        break

                    try:
                        card = cards.nth(i)

                        titulo = await card.locator(
                            ml_locators["titulo"]
                        ).first.inner_text()
                        if not item_relevante(pesquisa, titulo):
                            continue

                        price_label = await card.locator(
                            ml_locators["preco"]
                        ).get_attribute("aria-label")

                        preco = (
                            price_label
                            .replace("Agora: ", "")
                            .replace(" reais com ", ",")
                            .replace(" centavos", "")
                        )

                        link = await card.locator("a.poly-component__title").get_attribute("href")
                        link = shortner(link)

                        # limpa rastreamento do Mercado Livre
                        resultado = (
                            f"🟨 MERCADO LIVRE\n\n"
                            f'<a href="{link}">{titulo}</a>\n'
                            f'💰 Preço: {preco}\n\n'
                        )

                        resultados.append(resultado)
                        mostrados += 1

                    except Exception as e:
                        print(e)
                        continue
        await context.storage_state(path=state_path)
        await context.close()
        await browser.close()
    return resultados
