from modules.Amazon.main import amazon
from modules.MercadoLivre.main import mercadolivre
from modules.Aliexpress.main import aliexpress


pesquisa = input("Qual produto voce quer pesquisar? \n=")

if pesquisa != "":
    #amazon(pesquisa)
    #mercadolivre(pesquisa)
    aliexpress(pesquisa)
else:
    print("produto invalido")