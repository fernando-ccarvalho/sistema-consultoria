from view import conectar

con = None
cur = None

try:
    con = conectar()
    cur = con.cursor()
    query = """
    CREATE TABLE IF NOT EXISTS formulario (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR (255),
        email VARCHAR (255),
        telefone VARCHAR (50),
        data_consulta VARCHAR (50),
        estado VARCHAR (50),
        assunto VARCHAR (255)
    )
    """

    cur.execute(query)

    con.commit()

    print('Conexão e Tabela criadas com sucesso no MySQL')

finally:
    if cur:
        cur.close()
    if con and con.is_connected():
        con.close()