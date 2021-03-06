from CreateDB import criarBanco
from models.Usuario import Usuario
from database.UsuarioDAO import UsuarioDAO
from util.Validator import Validator

def menuUsuario(usuario):
    limparTela()

    op = 100

    while op > 0:
        try:

            if(len(usuario.nome) > 28):
                print('=' * (len(usuario.nome) + 4))
            else:
                print('=' * 34)

            print("||" + '{:^30}'.format(usuario.nome) + "||")

            if (len(usuario.nome) > 28):
                print('=' * (len(usuario.nome) + 4))
            else:
                print('=' * 34)

            print("1) Ver meu perfil\n"
                  "2) Adicionar amigo\n"
                  "3) Listar amigos\n"
                  "4) Solicitações de amizade\n"
                  "5) Enviar mensagem para amigo\n"
                  "6) Listar mensagens\n"
                  "0) Logout\n")
            op = int(input("-->"))
        except:
            print("Essa não é uma opção válida...\n\n\n")
            continue

        #Opção de logout, quando usada quebra o laço, saindo do menu de usuário e voltando para menu principal.
        if(op == 0):
            break

        elif(op == 1):
            limparTela()

            print("=" * 34)
            print("|Nome: %s {:>{n}}".format('|', n=(26-len(usuario.nome))) % usuario.nome)
            print("|Data de nascimento: %s {:>{n}}".format('|', n=(12-len(usuario.data_nasc.strftime("%d/%m/%Y")))) % usuario.data_nasc.strftime("%d/%m/%Y"))
            print("|Profissão: %s {:>{n}}".format('|', n=(21-len(usuario.profissao))) % usuario.profissao)
            print("|Gênero: %s {:>{n}}".format('|', n=(24-len(usuario.genero))) % usuario.genero)
            print("|Cidade: %s {:>{n}}".format('|', n=(24-len(usuario.cidade))) % usuario.cidade)
            print("|Estado: %s {:>{n}}".format('|', n=(24-len(usuario.estado))) % usuario.estado)
            print("|País: %s {:>{n}}".format('|', n=(26-len(usuario.pais))) % usuario.pais)

        #Opção de adicionar amigo, pede o nome da pessoa, procura todos os usuários com esse nome e lista com seu respectivo id,
        #verifica se nenhum usuário foi encontrado
        #se só 1 usuário for encontrado, ele já enviar a solicitação
        #se mais de 1 usuário for encontrado, pede para especificar o id do usuário e em seguida envia solicitação
        elif(op == 2):
            nome = input("Digite o nome da pessoa: ")
            users = UsuarioDAO().procurarUsuariosPorNome(nome)

            if len(users) == 0:
                limparTela()
                print("Nenhum usuário com esse nome foi encontrado.")
                continue
            elif len(users) == 1:
                if(UsuarioDAO().isFriend(usuario.id, users[0].id)):
                    limparTela()
                    print(users[0].nome + " já é seu amigo!")
                    continue

                limparTela()

                if(UsuarioDAO().solicitacaoAmizade(usuario.id, users[0].id)):
                    print("Solicitação de amizade enviada!\n\n")
                else:
                    print("Houve um problema... Não já existe uma solicitação pendente?\n\n")
            else:
                for user in users:
                    print(user.id + " - " + user.nome)

                id = int(input("Digite o ID da pessoa que deseja adicionar: "))

                if(UsuarioDAO().procurarUsuarioPorId(id) is None):
                    print("Usuário com esse ID não encontrado.\n\n")
                    continue
                else:
                    if (usuario.isFriend(id)):
                        print(UsuarioDAO().procurarUsuarioPorId(id).nome + " já é seu amigo!")
                        continue

                    if(usuario.solicitacaoAmizade(id)):
                        print("Solicitação de amizade enviada!\n\n")
                    else:
                        print("Houve um problema... Não já existe uma solicitação pendente?\n\n")

        #Opção que lista todos os amigos do usuário
        elif(op == 3):
            limparTela()
            for user in UsuarioDAO().listarAmigos(usuario.id):
                print(user.nome)

        #Opção que lista todas as solicitações de amizade pendentes
        elif(op == 4):
            limparTela()
            if(len(UsuarioDAO().listarSolicitacoes(usuario.id)) == 0):
                print("Nenhuma solicitação pendente!")

            for solicitacao in UsuarioDAO().listarSolicitacoes(usuario.id):
                if(not solicitacao[1] is None):
                    print(UsuarioDAO().procurarUsuarioPorId(solicitacao[1]).nome + " - " + solicitacao[3])

                    if(solicitacao[3] == "PENDENTE"):
                        op1 = input("Deseja aceitar esta solicitação? (s/n) ")

                        if(op1.lower().startswith("s")):
                            UsuarioDAO().aceitarAmizade(solicitacao[1], usuario.id)
                            limparTela()
                            print("Amizade aceita!")
                        elif(op1.lower().startswith("n")):
                            UsuarioDAO().negarAmizade(solicitacao[1], usuario.id)
                            limparTela()
                            print("Amizade negada!")

        #Lista os amigos com seus respectivos ids, e em seguida pede o id do usuário a enviar a mensagem, e depois a mensagem
        #Obs: No momento, o usuário pode enviar mensagem para um id que não é seu amigo. (A consertar)
        elif(op == 5):
            for user in UsuarioDAO().listarAmigos(usuario.id):
                print(str(user.id) + " - " + str(user.nome))

            id = int(input("ID do amigo: "))
            user = UsuarioDAO().procurarUsuarioPorId(id)

            if user is None:
                print("Usuário inválido")
                continue

            msg = input("Mensagem: ")

            UsuarioDAO().enviarMensagem(usuario.id, id, msg)
            limparTela()
            print("Mensagem enviada com sucesso!")

        #Lista todas as mensagens enviadas e recebidas.
        elif(op == 6):
            msgs = UsuarioDAO().listarMensagens(usuario.id)
            limparTela()

            for msg in msgs:
                print(UsuarioDAO().procurarUsuarioPorId(msg[1]).nome + " para " + UsuarioDAO().procurarUsuarioPorId(msg[2]).nome + ": " + msg[3])

def limparTela():
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

def menu():
    op = 100

    while op > 0:
        try:
            op = int(input("================================\n"
                           "||           GeekWay          ||\n"
                           "================================\n"
                           "1) Login\n"
                           "2) Registrar\n"
                           "0) Sair\n"
                           "--> "))
        except:
            limparTela()
            print("Essa não é uma opção válida...\n\n\n")
            continue

        #Quebra o laço e finaliza o programa
        if(op == 0):
            print("Volte sempre...")
            return

        #Pede email e senha e em seguida verifica se existe no banco
        #se for autenticado, vai para o menu de usuário
        elif(op == 1):
            email = input("E-mail: ")
            senha = input("Senha: ")

            if(UsuarioDAO().verificar_login(email, senha)):
                limparTela()
                print("Logado com sucesso!\n\n\n")

                usuario = UsuarioDAO().procurarUsuarioPorEmail(email)
                menuUsuario(usuario)
            else:
                limparTela()
                print("Login inválido.\n\n\n")
                continue

        #Pede informações de cadastro e verifica se email já existe.
        #se cadastrar, redireciona para menu de usuário
        elif(op == 2):
            while True:
                nome = input("Nome: ")
                if(not Validator().validName(nome)):
                    print("Nome pequeno ou grande demais.")
                    continue
                break

            while True:
                email = input("E-mail: ")
                if(UsuarioDAO().emailExists(email)):
                    print("Este email já existe, cadastre outro.\n")
                    continue
                if(not Validator().validEmail(email)):
                    print("E-mail inválido, cadastre outro.\n")
                    continue
                break

            while True:
                senha = input("Senha: ")
                if(not Validator().validPassword(senha)):
                    print("Senha pequena ou grande demais.")
                    continue
                break

            while True:
                data_nasc = input("Data de nascimento (dd/mm/YYYY): ")
                if(Validator().validDate(data_nasc) == False):
                    print("Data de nascimento inválida.")
                    continue
                data_nasc = Validator().validDate(data_nasc)
                break

            user = None

            try:
                user = Usuario(nome, email, senha, data_nasc, "", "", "", "", "")
                id = UsuarioDAO().insert(user)
            except:
                limparTela()
                print("Oops! Houve algum problema... Talvez você tenha passado dos limites :P")
                continue

            limparTela()
            print("Cadastrado com sucesso!\n\n\n")

            menuUsuario(UsuarioDAO().procurarUsuarioPorId(id))

        limparTela()

def main():
    #Função para criar o banco com todas as tabelas.
    criarBanco()

    #Menu principal
    menu()

if __name__ == '__main__':
    main()