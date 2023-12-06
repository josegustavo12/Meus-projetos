import csv
from reportlab.pdfgen import canvas
import qrcode
import os

produtos = []
cores = { # cores que eu coloquei (prec)
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

def imprimir_string_colorida(texto, cor): # função para por cor na string
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
        # Adicione outras cores conforme necessário
    }

    if cor not in cores:
        raise ValueError(f'Cor "{cor}" não é suportada.')

    print(f'{cores[cor]}{texto}{cores["reset"]}')

# Função para adicionar um produto à lista
def adicionar_produto(nome, quant):
    nome = nome.strip().lower()

    for item in produtos:
        if item["Produto"] == nome:
            item["Quantidade"] += quant
            return

    produtos.append({"Produto": nome, "Quantidade": quant})

# Função para remover um produto da lista
def remover_produto(nome, quant):
    nome = nome.strip().lower()
    indice = next((index for index, produto in enumerate(produtos) if produto["Produto"] == nome), None)

    if indice is not None:
        if produtos[indice]["Quantidade"] >= quant:
            produtos[indice]["Quantidade"] -= quant
            if produtos[indice]["Quantidade"] == 0:
                produtos.pop(indice)
        else:
            print(f'A quantidade a ser removida para "{nome}" excede a quantidade presente na lista.')
    else:
        print(f'O produto "{nome}" não foi encontrado no inventário.')

# Função para salvar a lista de produtos em um arquivo CSV
def salvar_csv(nome_pasta, nome_arquivo):
    with open(os.path.join(nome_pasta, nome_arquivo), "w", newline="") as csvfile:
        fieldnames = ["Produto", "Quantidade"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(produtos)

# Função para gerar código QR e PDF a partir da lista de produtos
def gerar_qr_code(nome_pasta):
    tabela_csv = os.path.join(nome_pasta, "tabela_inventario.csv")

    # Salva a lista de produtos em um arquivo CSV
    salvar_csv(nome_pasta, "tabela_inventario.csv")

    # Cria um objeto QRCode com configurações específicas
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    # Lê o arquivo CSV e adiciona os dados ao objeto QRCode
    with open(tabela_csv, 'r') as csvfile:
        qr.add_data(csvfile.read())
        qr.make(fit=True)

    # Salva a imagem do código QR
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join(nome_pasta, "tabela_inventario.png"))

# Função para gerar um PDF a partir da lista de produtos e do código QR
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

# Função para modificar as cores do menu
def modificar_cores_menu():
    global cores  # Certifique-se de que a variável cores é acessível globalmente

    print("\n======= MODIFICAR CORES DO MENU =======")
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

# Função para criar um menu interativo
def menu_interativo():
    nome_pasta = "inventario"
    os.makedirs(nome_pasta, exist_ok=True)

    cor_menu = 'vermelho'  # Cor padrão para o menu

    while True:
        imprimir_string_colorida("\n======= MENU =======", cor_menu)
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
        elif escolha == "4":
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
