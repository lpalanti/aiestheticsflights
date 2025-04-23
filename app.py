import requests
import streamlit as st
import datetime  # Importar a biblioteca datetime para manipulação de datas

# Substitua com a sua chave da API
API_KEY = 'f8a08438f91b2695c91128afd91db218'  # Chave fornecida
BASE_URL = "http://api.aviationstack.com/v1/flights"  # URL correta da API

# Função para buscar voos
def buscar_voos(origem, destino, data_partida, data_retorno):
    params = {
        'access_key': API_KEY,
        'dep_iata': origem,  # Código IATA do aeroporto de origem (Ex: 'JFK' para JFK Airport)
        'arr_iata': destino,  # Código IATA do aeroporto de destino (Ex: 'LHR' para Heathrow)
        'flight_date': data_partida,  # Data do voo de ida (Formato: 'YYYY-MM-DD')
        'return_date': data_retorno,  # Data do voo de retorno (Formato: 'YYYY-MM-DD')
    }
    
    # Fazendo a requisição GET para a API
    response = requests.get(BASE_URL, params=params)
    
    # Verificando a resposta da API
    if response.status_code == 200:
        return response.json()  # Retorna os dados dos voos encontrados
    else:
        print(f"Erro ao buscar voos: {response.status_code}")
        return None

# Interface do Streamlit
st.title('Busca de Voos')

# Entradas do usuário
origem = st.text_input('Origem (código IATA do aeroporto)', 'JFK')  # Exemplo: 'JFK' para JFK em NY
destino = st.text_input('Destino (código IATA do aeroporto)', 'LHR')  # Exemplo: 'LHR' para Heathrow em Londres

# Alterando a forma como as datas são tratadas
data_partida = st.date_input('Data de Partida', value=datetime.date(2025, 5, 10))
data_retorno = st.date_input('Data de Retorno', value=datetime.date(2025, 5, 20))

# Quando o usuário clicar no botão de buscar
if st.button('Buscar Voos'):
    dados_voos = buscar_voos(origem, destino, str(data_partida), str(data_retorno))
    
    if dados_voos:
        # Verifique o conteúdo da resposta para depuração
        st.write("Resposta da API:")
        st.json(dados_voos)  # Exibe o JSON completo da resposta
        
        # Exibindo os voos encontrados
        if 'data' in dados_voos:
            st.write(f"Resultados encontrados: {len(dados_voos['data'])} voos")
            for voo in dados_voos['data']:
                st.write(f"Voo: {voo['flight']['iata']} - {voo['airline']['name']}")
                st.write(f"Origem: {voo['departure']['airport']} - {voo['departure']['estimated']} (Estimado)")
                st.write(f"Destino: {voo['arrival']['airport']} - {voo['arrival']['estimated']} (Estimado)")
                st.write(f"Status do voo: {voo['flight']['status']}")
                st.write("---")
        else:
            st.write("Nenhum voo encontrado na resposta.")
    else:
        st.write("Nenhum voo encontrado ou erro na requisição.")
