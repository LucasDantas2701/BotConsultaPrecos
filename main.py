from modules.Amazon.main import run


pesquisa = input("Qual produto voce quer pesquisar? \n=")

if pesquisa != "":
    run(pesquisa)
else:
    print("produto invalido")