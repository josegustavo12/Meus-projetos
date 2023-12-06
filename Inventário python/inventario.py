import csv
from reportlab.pdfgen import canvas
import qrcode
import os

produtos = []
cores = { # cores que eu coloquei 
    'reset': '\033[0m',
    'preto': '\033[30m',
    'vermelho': '\033[31m',
    'verde': '\033[32m',
    'amarelo': '\033[33m',
    'azul': '\033[34m',
    'magenta': '\033[35m',
    'ciano': '\033[36m',
    'branco': '\033[37m',
    'negrito': '\033[1m',
    'inverte_cores': '\033[7m',
}
# tive que botar fora e dentro das funções para que eu consiga modificar dinamicamente (veja mais na função que modifica as cores)
def imprimir_string_colorida(texto, cor): # função para imprimir a string (a de imprimir e a de modificar as cores são diferentes)
    cores = {
        'reset': '\033[0m',
        'preto': '\033[30m',
        'vermelho': '\033[31m',
        'verde': '\033[32m',
        'amarelo': '\033[33m',
        'azul': '\033[34m',
        'magenta': '\033[35m',
        'ciano': '\033[36m',
        'branco': '\033[37m',
        'negrito': '\033[1m',
        'inverte_cores': '\033[7m',
    }

    if cor not in cores:
        raise ValueError(f'Cor "{cor}" não é suportada.') # lançando o erro, caso a cor esteja fora da lista

    print(f'{cores[cor]}{texto}{cores["reset"]}')

def adicionar_produto(nome, quant):
    nome = nome.strip().lower()

    for item in produtos: # logica para não repetir produtos na lista geral
        if item["Produto"] == nome:
            item["Quantidade"] += quant
            return

    produtos.append({"Produto": nome, "Quantidade": quant}) # add caso n tenha

def remover_produto(nome, quant):
    nome = nome.strip().lower()

    for index, produto in enumerate(produtos): # logica para procurar o indice do produto
        if produto["Produto"] == nome:
            if produtos[index]["Quantidade"] >= quant:
                produtos[index]["Quantidade"] -= quant
                if produtos[index]["Quantidade"] == 0:
                    produtos.pop(index) # remove da lista quando o valor é zero
                return
            else:
                print(f'A quantidade a ser removida para "{nome}" excede a quantidade presente na lista.')
                return

    print(f'O produto "{nome}" não foi encontrado no inventário.')

def salvar_csv(nome_pasta, nome_arquivo): # salva a lista de produtos em csv
    with open(os.path.join(nome_pasta, nome_arquivo), "w", newline="") as csvfile:
        fieldnames = ["Produto", "Quantidade"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(produtos)

def gerar_qr_code(nome_pasta): # função para gerar o qr code e o  pdf (to  pensando em tirar o pdf)
    tabela_csv = os.path.join(nome_pasta, "tabela_inventario.csv") # colocando a tabela na pasta
    # na main lá em baixo tem uma parte do codigo para verificar a existencia da pasta
    salvar_csv(nome_pasta, "tabela_inventario.csv")

    qr = qrcode.QRCode( # não sei perfeitamente como ta funcionando isso, mas é um objeto com as informações do qrcode
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    with open(tabela_csv, 'r') as csvfile: # lê o arquivo e add os dados
        qr.add_data(csvfile.read())
        qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join(nome_pasta, "tabela_inventario.png"))

def gerar_pdf(nome_pasta):
    nome_arquivo_pdf = os.path.join(nome_pasta, "inventario.pdf")
    c = canvas.Canvas(nome_arquivo_pdf)
    c.setFont("Helvetica", 12) 

    for produto in produtos:
        linha = f"{produto['Produto']}: {produto['Quantidade']}"
        c.drawString(100, 700, linha)

    c.drawInlineImage(os.path.join(nome_pasta, "tabela_inventario.png"), 400, 700, width=100, height=100)

    c.save()
    print(f"PDF gerado em {nome_arquivo_pdf}")

def modificar_cores_menu():
    global cores # é para isso que precisa da cores na global

    print("\n========= MODIFICAR CORES DO MENU =========")
    print("Cores disponíveis:")
    for cor in cores.keys():
        print(f"{cor}")

    cor_menu = input("Digite o nome da cor para o menu: ")
    if cor_menu in cores:
        print(f'A cor do menu foi modificada para "{cor_menu}".')
        return cor_menu
    else:
        print(f'A cor "{cor_menu}" não é suportada. A cor do menu permanecerá inalterada.')
        return None

def menu_interativo(): # menu do sistema
    nome_pasta = "inventario"
    os.makedirs(nome_pasta, exist_ok=True) # logica que eu tinha falado sobre criar a pasta caso ela n exista (remove possiveis erros)

    cor_menu = 'vermelho' # cor padrão 

    while True:
        imprimir_string_colorida("\n======= MENU =======", cor_menu) # a função para imprimir (to pensando em usar o map para printar tudo e reduzir a uma linha quase)
        print("1. Adicionar Produto")
        print("2. Remover Produto")
        print("3. Visualizar Inventario")
        print("4. Gerar Código QR e PDF")
        print("5. Modificar Cores do Menu")
        print("6. Sair")

        escolha = input("Escolha a opção (1-6): ")

        if escolha == "1":
            nome_produto = input("Digite o nome do produto: ")
            try:
                quantidade_produto = int(input("Digite a quantidade do produto: "))
                adicionar_produto(nome_produto, quantidade_produto)
            except ValueError:
                print("Quantidade inválida. Por favor, digite um número inteiro.")
        elif escolha == "2":
            nome_produto = input("Digite o nome do produto a ser removido: ")
            try:
                quantidade_produto = int(input("Digite a quantidade a ser removida: "))
                remover_produto(nome_produto, quantidade_produto)
            except ValueError:
                print("Quantidade inválida. Por favor, digite um número inteiro.")
        elif escolha == "3":
            print("\n=== Inventario ===")
            for produto in produtos:
                print(f"{produto['Produto']}: {produto['Quantidade']}")
        elif escolha == "4": # depois quero implementar uma função para o usuario dar o nome a pasta
            gerar_qr_code(nome_pasta)
            gerar_pdf(nome_pasta)
            print(f"Arquivos gerados na pasta: {nome_pasta}")
        elif escolha == "5":
            nova_cor_menu = modificar_cores_menu()
            if nova_cor_menu:
                cor_menu = nova_cor_menu
        elif escolha == "6":
            break
        else:
            print("Opção inválida. Escolha uma opção de 1 a 6.")

if __name__ == "__main__":
    menu_interativo()
