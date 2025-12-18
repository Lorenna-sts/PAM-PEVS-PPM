import pandas as pd
import glob
import os

# --- Configurações ---
pasta_arquivos = '.' 
nome_arquivo_saida = 'dados_agregados_final.csv' # Nome alterado para indicar a correção BOM

# Definição dos encodings
encoding_leitura = 'cp1252' # Mantido para ler dados corrompidos
encoding_escrita = 'utf-8-sig' # ALTERADO: Adiciona o BOM para o Excel reconhecer UTF-8
colunas_desejadas = ['loc_nome', 'loc_cod', 'var_cod', 'd_2024']

lista_de_arquivos = glob.glob(os.path.join(pasta_arquivos, 'Agregação*.csv'))
all_data = []

# 1. Leitura dos arquivos (mantido o código de leitura)
for arquivo in lista_de_arquivos:
    try:
        df = pd.read_csv(arquivo, sep=';', encoding=encoding_leitura, index_col=0)
        all_data.append(df)
    except Exception:
        try:
            df = pd.read_csv(arquivo, sep=';', encoding='latin1', index_col=0)
            all_data.append(df)
        except:
            pass 

# 2. Concatena os DataFrames
if all_data:
    df_merged = pd.concat(all_data, ignore_index=True)

    # 3. CORREÇÃO DA COLUNA LOC_NOME (MANTIDA: Corrige os caracteres corrompidos)
    try:
        df_merged['loc_nome'] = df_merged['loc_nome'].astype(str).str.encode('latin1').str.decode('utf-8')
    except Exception:
        pass
        
    # 4. Limpeza e Ajuste de Colunas (Mantida)
    df_merged = df_merged.loc[:, df_merged.columns.isin(colunas_desejadas)]
    df_merged['var_cod'] = pd.to_numeric(df_merged['var_cod'], errors='coerce').astype('Int64')
        
    # 5. SALVA O DATAFRAME AGREGADO COM O ENCODING BOM
    try:
        df_merged.to_csv(nome_arquivo_saida, sep=';', encoding=encoding_escrita, index=False)
        print(f"\nSucesso! O arquivo foi salvo como: {nome_arquivo_saida}")
        print("Tente abrir este novo arquivo (com _BOM no nome) diretamente no Excel.")
        
    except Exception as e:
        print(f"ERRO ao salvar o arquivo: {e}")