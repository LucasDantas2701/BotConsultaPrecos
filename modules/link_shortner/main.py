import requests

def shortner(link):
    try:
        response = requests.get(
            f"https://tinyurl.com/api-create.php?url={link}",
            timeout=10
        )

        if response.status_code == 200:
            return response.text

        return link

    except Exception as e:
        print(f"Erro ao encurtar link: {e}")
        return link