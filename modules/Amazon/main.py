from playwright.sync_api import sync_playwright
from shared.block_pass.humanizer import espera, mover_mouse, digitar_humano

def run(pesquisa):

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/136.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1366, "height": 768},
            locale="pt-Br"
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
        espera(1, 2)
        digitar_humano(search, pesquisa)
        espera(1, 2)
        search.press("Enter")
        espera(3, 5)
        print("Buscando produtos...\n")

        # cards dos produtos
        cards = page.locator('div[role="listitem"][data-asin]')
        print(f"Quantidade de produtos encontrados: {cards.count()}")
        print("\nMostrando os 10 primeiros:\n")

        for i in range(min(cards.count(), 10)):
            card = cards.nth(i)
            titulo = card.locator("h2").first.inner_text()
            preco = card.locator(".a-price").first.inner_text()
            link = card.locator("a").first.get_attribute("href")
            if link and link.startswith("/"):
                link = "https://www.amazon.com.br" + link

            print(f"Título: {titulo}")
            print(f"Preço: {preco}")
            print(f"Link: {link}")
            print("-" * 50)

        context.close()
        browser.close()

