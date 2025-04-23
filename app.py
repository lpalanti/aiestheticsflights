import streamlit as st
import requests
import altair as alt
from datetime import datetime, timedelta

# --- CONFIG ---
st.set_page_config(page_title="Rastreador de Voos", layout="wide")

# --- API CONFIG ---
API_KEY = 'f8a08438f91b2695c91128afd91db218'  # Sua chave API
BASE_URL = 'http://api.aviationstack.com/v1/flights'

# --- HEADER ---
st.title("✈️ Rastreador de Voos em Tempo Real")
st.markdown("Veja informações de voos a partir dos dados públicos das companhias aéreas.")

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔎 Filtros de busca")

iata_departure = st.sidebar.text_input("Aeroporto de Origem (IATA)", "GRU")
iata_arrival = st.sidebar.text_input("Aeroporto de Destino (IATA)", "MIA")
flight_date = st.sidebar.date_input("Data do voo", datetime.today())
airline_filter = st.sidebar.text_input("Companhia aérea (ex: LATAM, Azul)", "")
class_filter = st.sidebar.selectbox("Classe", ["Todas", "Econômica", "Executiva", "Primeira"], index=0)
time_range = st.sidebar.slider("Horário de partida (local)", 0, 23, (0, 23))
direct_only = st.sidebar.checkbox("Apenas voos diretos")

# --- API REQUEST ---
params = {
    'access_key': API_KEY,
    'dep_iata': iata_departure,
    'arr_iata': iata_arrival,
    'flight_date': flight_date.strftime('%Y-%m-%d')
}

st.sidebar.markdown("---")
if st.sidebar.button("🔍 Buscar voos"):
    with st.spinner("Consultando dados de voo..."):
        response = requests.get(BASE_URL, params=params)
        data = response.json()

        if "data" not in data or not data["data"]:
            st.warning("Nenhum voo encontrado para os filtros selecionados.")
        else:
            voos = data["data"]

            # --- FILTRAGEM MANUAL (mock para filtros adicionais) ---
            voos_filtrados = []
            for voo in voos:
                hora_partida = voo['departure']['scheduled']
                airline = voo['airline']['name']
                if airline_filter and airline_filter.lower() not in airline.lower():
                    continue
                if hora_partida:
                    hora_obj = datetime.fromisoformat(hora_partida)
                    if not (time_range[0] <= hora_obj.hour <= time_range[1]):
                        continue
                if direct_only and voo['arrival']['airport'] != iata_arrival:
                    continue
                voos_filtrados.append(voo)

            if voos_filtrados:
                for voo in voos_filtrados:
                    st.markdown("----")
                    col1, col2, col3 = st.columns([2, 2, 2])
                    with col1:
                        st.subheader(f"✈️ {voo['airline']['name']}")
                        st.text(f"Voo: {voo['flight']['iata']}")
                        st.text(f"Aeronave: {voo.get('aircraft', {}).get('registration', 'N/A')}")
                    with col2:
                        st.markdown("**🛫 Partida**")
                        st.text(f"{voo['departure']['airport']} - {voo['departure']['scheduled']}")
                    with col3:
                        st.markdown("**🛬 Chegada**")
                        st.text(f"{voo['arrival']['airport']} - {voo['arrival']['scheduled']}")
            else:
                st.warning("Nenhum voo encontrado com os filtros aplicados.")

