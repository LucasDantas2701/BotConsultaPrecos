import os
from playwright.async_api import async_playwright
from modules.Amazon.lista import amazon_locators
from shared.block_pass.humanizer import espera, mover_mouse, digitar_humano

state_path = "assets/amazon_state.json"

async def amazon(pesquisa):
    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )
        context = await browser.new_context(
            storage_state=state_path if os.path.exists(state_path) else None,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768},
            locale="pt-BR"
        )
        page = await context.new_page()
        await page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)
        await page.goto(amazon_locators["url"])
        espera(2, 4)
        await mover_mouse(page)
        search = page.get_by_role("searchbox", name="Pesquisar Amazon.com.br")
        resultados = []
        if await search.is_visible():
            espera(1, 2)
            await digitar_humano(search, pesquisa)
            espera(1, 2)
            await search.press("Enter")
            espera(3, 5)
            cards = page.locator(amazon_locators["card"])
            mostrados = 0
            if await cards.count() > 0:
                for i in range(await cards.count()):
                    if mostrados == 2:
                        break
                    try:
                        card = cards.nth(i)
                        titulo = await card.locator(amazon_locators["titulo"]).first.inner_text()
                        preco = await card.locator(amazon_locators["preco"]).first.inner_text()
                        link = await card.locator(amazon_locators["link"]).first.get_attribute("href")
                        if not titulo or not preco or not link:
                            continue
                        if link.startswith("/"):
                            link = amazon_locators["url"] + link
                        resultado = (
                            f"🟦 AMAZON\n\n"
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