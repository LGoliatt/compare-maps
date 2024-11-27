import streamlit as st
import folium
from streamlit_folium import st_folium
import requests

@st.cache_data
def load_geojson(url):
    response = requests.get(url)
    response.raise_for_status()  
    return response.json()

st.set_page_config(page_title="Comparação de Rotas", page_icon="🌍", layout="wide")
st.title("Comparação de Rotas")

st.write("Digite os links dos arquivos GeoJSON para cada mapa separados por vírgula.")
st.write("Exemplo IDA e VOLTA da Linha 525: https://drive.google.com/uc?id=1j9wB2KQWG7VSvrPjzNUNRRy-Vo7a23fK, https://drive.google.com/uc?id=18LTgDkDMS5eUxl-Y1KKlyuF7aycNUwtg")
# Entrada para links GeoJSON
geojson_urls_1 = st.text_input("Links do GeoJSON para o Mapa 1 (ROTA PADRÃO)", "")
geojson_urls_2 = st.text_input("Links do GeoJSON para o Mapa 2 (ROTA OTIMIZADA)", "")



def adicionar_rotas_ao_mapa(mapa, urls, nome_rota_base, cores):
    """Adiciona rotas de GeoJSON ao mapa com cores específicas."""
    for i, url in enumerate(urls[:2], start=1):  # Limitar a apenas duas rotas (ida e volta)
        try:
            geojson_data = load_geojson(url.strip())
            folium.GeoJson(
                geojson_data,
                name=f"{nome_rota_base} {i}",
                tooltip=f"{nome_rota_base} {'Ida' if i == 1 else 'Volta'}",
                style_function=lambda x, color=cores[i - 1]: {
                    "color": color,
                    "weight": 3,
                    "opacity": 0.8,
                }
            ).add_to(mapa)
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao carregar o GeoJSON do link '{url}': {e}")

if geojson_urls_1 or geojson_urls_2:
    # Inicializar mapas
    mapa_1 = folium.Map(location=[-21.7610, -43.3434], zoom_start=12)
    mapa_2 = folium.Map(location=[-21.7610, -43.3434], zoom_start=12)

    # Adicionar rotas ao Mapa 1
    if geojson_urls_1:
        urls_1 = geojson_urls_1.split(',')
        adicionar_rotas_ao_mapa(mapa_1, urls_1, "Rota Mapa 1", ["blue", "red"])

    # Adicionar rotas ao Mapa 2
    if geojson_urls_2:
        urls_2 = geojson_urls_2.split(',')
        adicionar_rotas_ao_mapa(mapa_2, urls_2, "Rota Mapa 2", ["blue", "red"])

    # Exibir os mapas
    col1, col2 = st.columns(2)

    with col1:
        st.write("Rota Padrão:")
        st_folium(mapa_1, width=550, height=550, key="mapa_1")

    with col2:
        st.write("Rota Otimizada:")
        st_folium(mapa_2, width=550, height=550, key="mapa_2")

    # legenda
    st.markdown("""
    <div style='border: 1px solid black; padding: 10px; width: fit-content; background-color: white;'>
        <b>Legenda:</b><br>
        <div style='display: flex; align-items: center;'>
            <span style='width: 20px; height: 20px; background-color: blue; display: inline-block; margin-right: 10px;'></span>
            Ida
        </div>
        <div style='display: flex; align-items: center; margin-top: 5px;'>
            <span style='width: 20px; height: 20px; background-color: red; display: inline-block; margin-right: 10px;'></span>
            Volta
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    st.write("Por favor, insira os links das rotas para visualizar os mapas.")
