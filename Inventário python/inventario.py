import csv # biblioteca do csv 
from reportlab.pdfgen import canvas
import qrcode
import os

produtos = [] # lista dos produtos

def adicionar_produto(nome, quant):
    nome = nome.strip().lower()

    for item in produtos: # for para verificar se o produto já está na lista, caso esteja só adiciona a mais no produto
        if item["Produto"] == nome:
            item["Quantidade"] += quant
            return

    #  add se n tiver o produto
    produtos.append({"Produto": nome, "Quantidade": quant})

def salvar_csv():
    # estudar um pouco mais sobre arquivos para ver se tem como fazer de um jeito melhor
    with open("inventario.csv", "w", newline="") as csvfile:
        fieldnames = ["Produto", "Quantidade"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(produtos)

def gerar_qr_code(): # função pra gerar o qr code com ajuda do gpt pq eu tava tendo um pouco de dificuldade
    qr_folder = "qrcodes/"

    if not os.path.exists(qr_folder): # verifica se o diretorio já existe
        os.makedirs(qr_folder)

    # cria a tabela em csv utilizando uma string
    tabela_csv = "\n".join([f"{item['Produto']},{item['Quantidade']}" for item in produtos])

    # salva o qr code com o tamamho e no diretorio recomendado
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(tabela_csv)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white") # cor do qr code
    img.save(os.path.join(qr_folder, "tabela_inventario.png")) 

def gerar_pdf(): # função pra gerar o pdf
    pdf_file = "inventario.pdf" # to pensando em colocar uma função para que você escolha o nome para alocar melhor 

    c = canvas.Canvas(pdf_file)
    c.setFont("Helvetica", 12) 

    for produto in produtos:
        linha = f"{produto['Produto']}: {produto['Quantidade']}"
        c.drawString(100, 700, linha)

    # add o qr code da tabela inteira (ainda nn preciso mudar o tamanho pq a quantidade de informações é mto pequena)
    c.drawInlineImage(os.path.join("qrcodes", "tabela_inventario.png"), 400, 700, width=100, height=100)

    c.save()
    print(f"PDF gerado em {pdf_file}")

if __name__ == "__main__":
    while True:
        nome_produto = input("Digite o nome do produto (ou 'sair' para encerrar): ")
        if nome_produto.lower() == 'sair':
            break

        try: # tava dando mto problema pq eu sem querer colocava numero quando ia digitar e o codigo travava inteiro e eu perdia td q tinha colocado
            # então to usando o try pra não desandar tudo
            quantidade_produto = int(input("Digite a quantidade do produto: "))
            adicionar_produto(nome_produto, quantidade_produto)
        except ValueError:
            print("Quantidade inválida. Por favor, digite um número inteiro.")

    salvar_csv()
    gerar_qr_code()
    gerar_pdf()
