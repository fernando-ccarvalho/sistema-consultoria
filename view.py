import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def conectar():

    return mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME') 
        )


# ====================
# C - CREATE(inserir)
# ====================

def inserir_info(i):
    con = None
    cur = None
    try:
        con = conectar()
        cur = con.cursor()

        query = """ 
        INSERT INTO formulario
        (nome, email, telefone, data_consulta, estado, assunto)
        VALUES (%s, %s, %s, %s, %s, %s)
    """

        cur.execute(query, i)
        con.commit()
    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()


# ==========================
# R - READ (acessar/mostrar)
# ==========================

def mostrar_info():
    con = None
    cur = None
    try:
        con = conectar()
        cur = con.cursor()

        query = 'SELECT * FROM formulario'
        cur.execute(query)

        return cur.fetchall()
    
    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()

        

# ======================
# U - UPDATE (atualizar)
# ======================

def atualizar_info(i):
    con = None
    cur = None
    try:
        con = conectar()
        cur = con.cursor()
    
        query = """
        UPDATE formulario 
        SET nome=%s, email=%s, telefone=%s, data_consulta=%s, estado=%s, assunto=%s
        WHERE id = %s
    """
    
        cur.execute(query, i)
        con.commit()
    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()

#====================
# D - DELETE (apagar)
#====================

def deletar_info(i):
    con = None
    cur = None
    try:
        con = conectar()
        cur = con.cursor()

        query = 'DELETE FROM  formulario WHERE   ID =%s'

        cur.execute(query, i)

        con.commit()
    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()
    

#==========================
# FILTRO (busca específica)
#==========================

def buscar_info_id(i):
    cur = None
    con = None
    try:
        con = conectar()
        cur = con.cursor()

        query = 'SELECT * FROM formulario WHERE id=%s or nome LIKE %s'

        cur.execute(query,(i, f'%{i}%'))

        return cur.fetchall()
    finally:
        if cur:
            cur.close()
        if con and con.is_connected():
            con.close()
    