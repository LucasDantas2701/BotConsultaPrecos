import os
from playwright.sync_api import sync_playwright
from shared.block_pass.humanizer import espera, mover_mouse, digitar_humano
state_path = "assets/amazon_state.json"
def run(pesquisa):

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=False,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )
        context = browser.new_context(
            storage_state=state_path if os.path.exists(state_path) else None,
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768},
            locale="pt-BR"
        )

        page = context.new_page()

        # remove webdriver
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            })
        """)

        page.goto("https://www.amazon.com.br",)
        espera(2, 4)
        mover_mouse(page)
        search = page.get_by_role("searchbox", name="Pesquisar Amazon.com.br")

        if search.is_visible():
            espera(1, 2)
            digitar_humano(search, pesquisa)
            espera(1, 2)
            search.press("Enter")
            espera(3, 5)
            print("Buscando produtos...\n")

            # cards dos produtos
            cards = page.locator('div[role="listitem"][data-asin]')
            mostrados = 0
            if cards.count() > 0:
                print(f"Quantidade de produtos encontrados: {cards.count()}")
                print("\nMostrando os 5 primeiros:\n")

                for i in range(cards.count()):
                    if mostrados == 5:
                        break
                    try:
                        card = cards.nth(i)
                        titulo = card.locator("h2").first.inner_text()
                        preco = card.locator("span.a-offscreen").first.inner_text()
                        link = card.locator("a").first.get_attribute("href")
                        if link and link.startswith("/"):
                            link = "https://www.amazon.com.br" + link

                        print(f"{titulo}")
                        print(f"Preço: {preco}")
                        print(f"Link: {link}")
                        print("-" * 50)
                        print("\n")
                        mostrados += 1
                    except:
                        pass
            else:
                print("produtos não encontrados")
            
        else:
            print("barra de pesquisa não encontrada")

        context.storage_state(path="assets/amazon_state.json")
        context.close()
        browser.close()

