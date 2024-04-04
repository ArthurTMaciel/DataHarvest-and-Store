import os, time, boto3
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configuração do WebDriver para o Firefox (certifique-se de que o geckodriver está instalado e no seu PATH)
driver = webdriver.Firefox()

# Abre o site
driver.get('https://www.observatorioei.org.br/')

# Clique no primeiro botão de entrar
entrar1 = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="acesse"]'))
)
entrar1.click()

# Inserir os dados de login
email = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="exampleInputEmail1"]'))
)
email.send_keys('dado_sensiivel_retirado')

# Inserir senha
senha = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="exampleInputPassword1"]'))
)
senha.send_keys('dado_sensiivel_retirado')

# Segundo botao de entrar
entrar2 = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[2]/div/form/div[3]/button'))
)
entrar2.click()

time.sleep(2)

# Clique em "Gestao de avaliação"
gestao = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="navbarSupportedContent"]/ul/li[6]/a'))
)
gestao.click()

time.sleep(2)

# Clique em "Gerenciar instituições"
gerenciar = WebDriverWait(driver, 10).until(
    EC.visibility_of_element_located((By.XPATH, '//*[@id="navbarSupportedContent"]/ul/li[6]/div[1]/div[2]/div/div/div[1]/div/div[2]/p'))
)
gerenciar.click()

time.sleep(2)

# Local onde o arquivo foi baixado
download_path = "C:/Users/Alessandra Rezende/Downloads"

# Lista todos os arquivos no diretório de downloads
files = os.listdir(download_path)


vetor_xpath = [('/html/body/div[1]/div/div[2]/div/div[4]/div[4]/div/div[4]/a/div/img','Itaborai'),
               ('/html/body/div[1]/div/div[2]/div/div[4]/div[5]/div/div[4]/a/div/img','Quissama')]
#('/html/body/div[1]/div/div[2]/div/div[4]/div[6]/div/div[4]/a/div/img','SaoSebastiao')]
#('/html/body/div[1]/div/div[2]/div/div[4]/div[3]/div/div[4]/a/div/img','Mossoro') CAMPO DE MOSSORO AINDA NAO ESTA ATIVO

for i in range(len(vetor_xpath)):

    # Clique no campo que queremos 
    campo = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,vetor_xpath[i][0] ))
    )
    campo.click()

    time.sleep(2)

    # Clique em "aplicações"
    aplicacoes = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div/div[3]/div/div[3]/a[3]/div/div/div/i'))
    )
    aplicacoes.click()
    
    time.sleep(2)

    # Clique em "baixar dados"
    baixar = WebDriverWait(driver, 60).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div/div[5]/div[2]/div[3]/div[2]/button/div/span'))
    )
    baixar.click()

    time.sleep(10)

    #renomeia o arquivo
    os.rename(f'{download_path}/amostras.json', f'{download_path}/amostras_{vetor_xpath[i][1]}.json')

    # Assume que apenas um arquivo é baixado, pega o primeiro arquivo da lista
    file_name = f'amostras_{vetor_xpath[i][1]}.json'

    # Configurações do S3
    s3_bucket_name = 'qpdi-fgv'
    aws_access_key_id = 'dado_sensiivel_retirado'
    aws_secret_access_key = 'dado_sensiivel_retirado'
    s3_object_key = 's3://qpdi-fgv/pastateste/dados_brutos_' + vetor_xpath[i][1] + '.json'  # Defina o nome do objeto que será criado no seu bucket do S3

    # Enviar o arquivo para o Amazon S3
    s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
    with open(os.path.join(download_path, file_name), 'rb') as data:
        s3.upload_fileobj(data, s3_bucket_name, s3_object_key)

    driver.back()
    
    time.sleep(2)

    driver.back()
    
    time.sleep(2)












    

# Fechar o navegador
driver.quit()
