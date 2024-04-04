from datetime import datetime
import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import boto3
import os

# Configurações de conexão com o banco de dados
db_host = 'dado_sensiivel_retirado'
db_port = 'dado_sensiivel_retirado' 
db_name = 'dado_sensiivel_retirado'
db_user = 'dado_sensiivel_retirado'
db_password = 'dado_sensiivel_retirado'

caminho = 'G:/Drives compartilhados/lepes_dados/equipe_dados/Projeto_EAPI/dados_intermediarios/'

ob = pd.read_csv(caminho + 'ob.csv',sep=';')
ep = pd.read_csv(caminho + 'ep.csv',sep=';')
ed = pd.read_csv(caminho + 'ed.csv',sep=';')

# Construindo a string de conexão com o banco de dados 
db_connection_string = f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

# Criando uma engine de conexão com o banco de dados 
engine = create_engine(db_connection_string)

# Estabelecendo uma conexão com o banco de dados usando a engine
conn = engine.connect()


# Envia o DataFrame para o banco de dados
ob.to_sql('dds_eapi_od', con=conn, if_exists='replace', index=False)
ep.to_sql('dds_eapi_ep', con=conn, if_exists='replace', index=False)
ed.to_sql('dds_eapi_ed', con=conn, if_exists='replace', index=False)

# Fecha a conexão
conn.close()

# Configurações do S3
s3_bucket_name = 'qpdi-fgv'
aws_access_key_id = 'dado_sensiivel_retirado'
aws_secret_access_key = 'dado_sensiivel_retirado'

# Lista de arquivos a serem carregados
arquivos_para_subir = ['ob', 'ep', 'ed']

# Obter data e hora atual
data_hora_atual = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Iterar sobre os arquivos e fazer o upload para o Amazon S3
for arquivo in arquivos_para_subir:
    nome_arquivo_com_data_hora = f"{arquivo}_{data_hora_atual}.csv"
    s3_object_key = f's3://qpdi-fgv/pastateste/{nome_arquivo_com_data_hora}'  # Nome do objeto no bucket S3
    with open(os.path.join(caminho, f'{arquivo}.csv'), 'rb') as data:
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        s3.upload_fileobj(data, s3_bucket_name, s3_object_key)
