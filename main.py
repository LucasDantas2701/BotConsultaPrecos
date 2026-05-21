from modules.Amazon.main import run


pesquisa = input("Qual produto voce quer pesquisar?")

if pesquisa != "":
    run(pesquisa)
else:
    print("produto invalido")