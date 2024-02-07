# URL dinâmico e construção do URL

from flask import Flask, redirect, url_for

app = Flask(__name__)

@app.route("/hello/")  # lidando com /hello ou /hello/ para evitar problemas
@app.route("/hello/<nome>")  # definindo uma rota dinâmica com um parâmetro nome
def hello(nome=None):  # a função recebe o parâmetro nome
    if nome:
        return "<h1> Hello {} </h1>".format(nome) 
    else:
        return "<h1> Hello, seja bem-vindo! </h1>"
    
# como montar o URL dinâmico
'''
@app.route("/<url>/<variavel>")
def hello(variavel):
    return "<h1> Hello {} </h1>".format(variavel)
'''


# rota com URL dinâmica para exibir posts do blog
@app.route("/blog/")
@app.route("/blog/<postID>") 
def blog(postID=None):
    if postID:
        return "Informações do post {}".format(postID) 
    else:
        return "Todos os posts do blog"  

#############################################################################

# construção do URL
    
@app.route("/admin")
def admin():
    return "<h1> ADMIN </h1>"
@app.route("/guest/")
@app.route("/guest/<name>")
def guest(name=None):
    if  name:
        return "<p> Olá guest <b>%s</b></p>" % name
    else:
        return "<p> Olá guest, seja bem vindo"

@app.route("/user/<name>")
def user(name):
    if name == "admin":
        return redirect(url_for('admin')) # caso a URL seja "/user/admin" ele irá retornar a função admin
    else:
        return redirect(url_for('guest', name=name)) # irá retornar a função guest e o nome (caso n tenha nada irá para a pagina generica)
# o uso do redirect serve para redirecionar a rota para algo desejado, como o admin ou convidado
# o url_for tem que ser usando quando for colocar qual roda se refere (deve existir uma logica para fazer sem)
# mas já que há existe vamo usar a da própria biblioteca

# exemplo teste rredirect para o google
    
@app.route("/google")
def google():
    return redirect("https://google.com")


if __name__ == "__main__":
    app.run(debug=True, port=3000)
