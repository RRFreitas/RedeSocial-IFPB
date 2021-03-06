import mysql.connector
from common.ConfigDB import *

def criarBanco():
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE tb_usuario(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                nome varchar(100) NOT NULL,
                email varchar(50) NOT NULL UNIQUE,
                senha varchar(20) NOT NULL,
                data_nasc date,
                profissao varchar(30),
                genero varchar(15),
                cidade varchar(30),
                estado varchar(30),
                pais varchar(30)
            );
        """)

        cursor.execute("""
            CREATE TABLE tb_postagem(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                usuario_id integer NOT NULL,
                mensagem varchar(140),
                privacidade varchar(20),
                data_hora datetime,
                curtidas integer,
                FOREIGN KEY(usuario_id) REFERENCES tb_usuario(id)
            );
        """)

        cursor.execute("""
            CREATE TABLE tb_postagem_privada(
                postagem_id integer,
                id_usuario_permitido integer,
                FOREIGN KEY(postagem_id) REFERENCES tb_postagem(id),
                FOREIGN KEY(id_usuario_permitido) REFERENCES tb_usuario(id)
            );
        """)

        cursor.execute("""
            CREATE TABLE tb_comentario_postagem(
                postagem_id integer,
                usuario_id integer,
                mensagem text,
                data_hora datetime,
                curtidas integer,
                FOREIGN KEY(postagem_id) REFERENCES tb_postagem(id),
                FOREIGN KEY(usuario_id) REFERENCES tb_usuario(id)
            );
        """)

        cursor.execute("""
        CREATE TABLE tb_mensagem_direta(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                remetente_id integer,
                destinatario_id integer,
                mensagem text,
                data_hora datetime,
                visualizada boolean,
                FOREIGN KEY(remetente_id) REFERENCES tb_usuario(id),
                FOREIGN KEY(destinatario_id) REFERENCES tb_usuario(id)
            );
        """)

        cursor.execute("""
            CREATE TABLE tb_solicitacao_amizade(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                solicitante_id integer,
                solicitado_id integer,
                status varchar(8),
                data_solicitacao date,
                FOREIGN KEY(solicitante_id) REFERENCES tb_usuario(id),
                FOREIGN KEY(solicitado_id) REFERENCES tb_usuario(id)
            );
        """)

        cursor.execute("""
            CREATE TABLE tb_notificacoes(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                usuario_id integer,
                mensagem text,
                FOREIGN KEY(usuario_id) REFERENCES tb_usuario(id)
            );
        """)

        cursor.execute("""
            CREATE TABLE tb_amizade(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                usuario1_id integer,
                usuario2_id integer,
                data_inicio date,
                FOREIGN KEY(usuario1_id) REFERENCES tb_usuario(id),
                FOREIGN KEY(usuario2_id) REFERENCES tb_usuario(id)
            );
        """)

        cursor.execute("""
            CREATE TABLE tb_grupo(
                id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                id_criador integer,
                nome varchar(50),
                data_criacao date,
                descricao varchar(500),
                FOREIGN KEY(id_criador) REFERENCES tb_usuario(id)
            );
        """)

        cursor.execute("""
            CREATE TABLE tb_grupo_participante(
                grupo_id integer,
                participante_id integer,
                data_entrada date,
                cargo varchar(20),
                FOREIGN KEY(grupo_id) REFERENCES tb_grupo(id),
                FOREIGN KEY(participante_id) REFERENCES tb_usuario(id)
            );
        """)
    except mysql.connector.ProgrammingError as e:
        if(e.args[0] == 1050):
            return
        elif(e.args[0] == 1049):
            print("Por favor, crie a base de dados! Finalizando programa...")
            exit()
        else:
            print(e)
            exit()
    except:
        raise