from modules.Amazon.main import amazon
from modules.MercadoLivre.main import mercadolivre


pesquisa = input("Qual produto voce quer pesquisar? \n=")

if pesquisa != "":
    amazon(pesquisa)
    #mercadolivre(pesquisa)
else:
    print("produto invalido")