
import os
import pytesseract
import pymupdf
from fastapi import FastAPI
import requests
import re
from PIL import Image

app = FastAPI()



@app.get("/")
def home():
    return 'bemvindo'


@app.get("/arquivo/{url:path}")
def pegar_arquivo(url :str):


    response = requests.get(url)
    arquivo_path = os.path.basename(url)
    arquivo = open(arquivo_path, 'wb')
    arquivo.write(response.content)

    doc = pymupdf.open(arquivo)
    texto_extraido = ''

    for indx, text_pag in enumerate(doc.pages()):
        page = doc[indx]
        mat = pymupdf.Matrix(4, 4)
        pix = page.get_pixmap(matrix=mat)
        pix.save('foto_nf.png')

        imagem2 = Image.open('foto_nf.png')

        #caminho = r'C:\Program Files (x86)\Tesseract-OCR'

        pytesseract.pytesseract.tesseract_cmd ="/usr/bin/tesseract"
        txt = pytesseract.image_to_string(imagem2)
        txt = txt.replace("\n", "")
        txt = txt.strip()
        txt = txt.lower()
        texto_extraido = texto_extraido + txt

    lista_parametros_numero_nota = ['numero da nota', 'numero da nfs-e', 'nf-e']
    nota = ''

    for parametro in lista_parametros_numero_nota:
        if nota == '':
            parametro_num_nota = texto_extraido.find(parametro)
            if parametro_num_nota < 0:
                nota = ''
            else:
                txt_nota_ = texto_extraido.replace(" . ", "")
                txt_nota = txt_nota_[parametro_num_nota:]
                buscar_numero = re.compile('\d+')
                num_nota = buscar_numero.findall(txt_nota)
                num_nota = num_nota[0]
                nota = nota + num_nota
        else:
            break

    print(nota)

    lista_parametros_data_nota = ['data e hora de emissao', 'emissao']
    data = ''

    for parametro_data in lista_parametros_data_nota:
        if data == '':
            parametro_data = texto_extraido.find(parametro_data)
            if parametro_data < 0:
                data = ''
            else:
                txt_data = texto_extraido[parametro_data:]
                busca_data = re.compile('\d{2}/\d{2}/\d{4}')
                valor_data = busca_data.findall(txt_data)
                data_nota = valor_data[0]
                data = data + data_nota
        else:
            break

    print(data)

    lista_parametros_prestador = ['prestador de servico', 'remetente', 'nfs-eemitente', 'cnpj',
                                  'nfs-eprestador', ]

    cnpj_prestador_texto = ''

    for parametro in lista_parametros_prestador:
        if cnpj_prestador_texto == '':
            parametro_prestador = texto_extraido.find(parametro)
            if parametro_prestador < 0:
                cnpj_prestador_texto = ''
            else:
                parametro_prestador2 = texto_extraido.find('tomador')
                txt_prestador = texto_extraido[parametro_prestador:parametro_prestador2]

                txt_prestador = txt_prestador.replace(" -", "-")
                busca_cnpj_prestador = re.compile('\d{2}.\d{3}.\d{3}/\d{4}-\d{2}')
                cnpj_prestador_busca = busca_cnpj_prestador.findall(txt_prestador)
                cnpj_prestador = cnpj_prestador_busca[0]
                cnpj_prestador_texto = cnpj_prestador_texto + cnpj_prestador
        else:
            break

    print(cnpj_prestador_texto)

    lista_parametros_prestador_nome = ['social', 'empresarial']
    prestador = ''
    email = ''

    for parametro in lista_parametros_prestador_nome:
        if prestador == '':
            parametro_prestador = texto_extraido.find(parametro)
            if parametro_prestador < 0:
                prestador = ''
            else:
                parametro_prestador2 = texto_extraido.find('endere')
                txt_prestador_nome = texto_extraido[parametro_prestador:parametro_prestador2]

                nome_prestador = txt_prestador_nome.replace('social: ', "")
                nome_prestador = nome_prestador.replace('social', "")
                nome_prestador = nome_prestador.replace('empresarial', "")
                nome_prestador = nome_prestador.replace('e-mail', "")

                busca_email = re.compile(r'[a-z0-9_.+-]+@[a-z0-9_.+-]+\.[a-z0-9_.+-]')
                email_nome = busca_email.findall(nome_prestador)
                for email_lista in email_nome:
                    if email_lista == '':
                        pass
                    else:
                        email = email + email_lista
                        index_email = nome_prestador.find(email)
                        nome_prestador = nome_prestador[:index_email]

                nome_prestador = nome_prestador.replace(cnpj_prestador_texto, "")
                nome_prestador = nome_prestador.replace('cnpj / cpf / nif', "")
                nome_prestador = nome_prestador.upper()
                prestador = prestador + nome_prestador
        else:
            break

    print(prestador)

    lista_parametros_tomador = ['tomador de servico', 'tomador']
    cnpj_tomador_texto = ''
    txt_tomador = ''

    for parametro in lista_parametros_tomador:
        if cnpj_tomador_texto == '':
            parametro_tomador = texto_extraido.find(parametro)
            if parametro_tomador < 0:
                cnpj_tomador_texto = ''
            else:
                parametro_tomador2 = texto_extraido.find('intermediario de servico')
                txt_tomador = texto_extraido[parametro_tomador:parametro_tomador2]
                txt_tomador = txt_tomador + txt_tomador

                txt_tomador = txt_tomador.replace(" -", "-")
                busca_cnpj_tomador = re.compile('\d{2}.\d{3}.\d{3}/\d{4}-\d{2}')
                cnpj_tomador_busca = busca_cnpj_tomador.findall(txt_tomador)
                cnpj_tomador = cnpj_tomador_busca[0]
                cnpj_tomador_texto = cnpj_tomador_texto + cnpj_tomador

    print(cnpj_tomador_texto)

    lista_parametros_tomador_nome = ['social', 'empresarial']
    tomador = ''
    email_tomador = ''

    for parametro in lista_parametros_tomador_nome:
        if tomador == '':
            parametro_prestador = txt_tomador.find(parametro)
            if parametro_prestador < 0:
                tomador = ''
            else:
                parametro_prestador2 = txt_tomador.find('endere')
                txt_tomador_nome = txt_tomador[parametro_prestador:parametro_prestador2]

                nome_tomador = txt_tomador_nome.replace('social: ', "")

                nome_tomador = nome_tomador.replace('social', "")
                nome_tomador = nome_tomador.replace('empresarial', "")
                nome_tomador = nome_tomador.replace('e-mail', "")

                busca_email = re.compile(r'[a-z0-9_.+-]+@[a-z0-9_.+-]+\.[a-z0-9_.+-]')
                email_nome = busca_email.findall(nome_tomador)
                for email_lista in email_nome:
                    if email_lista == '':
                        pass
                    else:
                        email_tomador = email_tomador + email_lista
                        index_email = nome_tomador.find(email_tomador)
                        nome_tomador = nome_tomador[:index_email]

                parametro_tomador_cnpj = nome_tomador.find('cpf')
                nome_tomador = nome_tomador[:parametro_tomador_cnpj]
                nome_tomador = nome_tomador.upper()
                tomador = tomador + nome_tomador
        else:
            break

    print(tomador)

    lista_parametros_descricao = ['cao dos servicos', 'descrigdo do servigo']
    descricao_nota = ''

    for parametro in lista_parametros_descricao:
        if descricao_nota == '':
            parametro_descricao = texto_extraido.find(parametro)
            if parametro_descricao < 0:
                descricao_nota = ''
            else:
                parametro_descricao2 = texto_extraido.find('valor total')
                if parametro_descricao2 < 0:
                    parametro_descricao2 = texto_extraido.find('local da prestag')
                descricao = texto_extraido[parametro_descricao:parametro_descricao2]
                descricao = descricao.replace("cao dos servicos", "")
                descricao = descricao.replace("descrigdo do servigo", "")
                descricao = descricao.replace("descrigao dos servicos: ", "")
                parametro_descricao_final = descricao.find('tributa')
                descricao = descricao[:parametro_descricao_final]
                descricao_nota = descricao_nota + descricao
        else:
            break

    print(descricao_nota)

    lista_parametros_preco = ['valor total do servico', 'valor liquido', 'valor total da nota']
    valor_nota = ''

    for parametro in lista_parametros_preco:
        if valor_nota == '':
            parametro_valor = texto_extraido.find(parametro)
            if parametro_valor < 0:
                valor_nota = ''
            else:
                txt_valor = texto_extraido[parametro_valor:]
                busca_valor = re.compile('\d+.\d+,\d+')
                valor = busca_valor.findall(txt_valor)
                valor = valor[0]
                valor_nota = valor_nota + valor
        else:
            break

    print(valor_nota)

    dados_nota = {
        "num_nota": nota,
        "data_nota": data,
        "nome_prestador": prestador,
        "cnpj_prestador": cnpj_prestador_texto,
        "nome_tomador": tomador,
        "cnpj_tomador": cnpj_tomador_texto,
        "descricao_nota": descricao_nota,
        "valor_nota": valor_nota,
    }

    arquivo.close()
    doc.close()

    os.remove(arquivo.name)
    os.remove('foto_nf.png')

    return dados_nota
