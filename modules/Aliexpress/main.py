import os
from playwright.async_api import async_playwright
from modules.Aliexpress.lista import aliexpress_locators
from shared.block_pass.humanizer import espera, mover_mouse, digitar_humano
state_path = "assets/aliexpress_state.json"

async def aliexpress(pesquisa):
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
        await page.goto(aliexpress_locators["url"])
        espera(2, 4)
        await mover_mouse(page)
        popup = page.locator(".pop-close-btn")
        cookies = page.get_by_text("Não permitir")
        if await popup.is_visible():
            await popup.click()
            espera(1, 2)
        if await cookies.is_visible():
            await cookies.click()
            espera(1, 2)
        search = page.get_by_role("searchbox",name="Você pode digitar o nome de")
        resultados = []
        if await search.is_visible():
            espera(1, 2)
            await digitar_humano(search, pesquisa)
            espera(1, 2)
            await search.press("Enter")
            espera(3, 5)
            cards = page.locator(aliexpress_locators["card"])
            mostrados = 0
            if await cards.count() > 0:
                for i in range(await cards.count()):
                    if mostrados == 2:
                        break
                    try:
                        card = cards.nth(i)
                        titulo =  await card.locator(aliexpress_locators["titulo"]).inner_text()
                        preco =  await card.locator(aliexpress_locators["preco"]).inner_text()
                        link =  await card.get_attribute("href")
                        if not titulo or not preco or not link:
                            continue
                        if link.startswith("//"):
                            link = aliexpress_locators["url"] + link
                        elif link.startswith("/"):
                            link = "https://pt.aliexpress.com" + link
                        resultado = (
                            f"🟥 ALIEXPRESS\n\n"
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