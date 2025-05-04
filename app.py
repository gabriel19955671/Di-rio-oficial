import streamlit as st
import pandas as pd
import os
from datetime import datetime
import requests
from PyPDF2 import PdfReader
from io import BytesIO
from pdf2image import convert_from_bytes
import tempfile

st.set_page_config(page_title="Diário Oficial AL - Monitoramento", layout="centered")
st.title("📑 Monitor Diário Oficial de Alagoas")

CAMINHO_CLIENTES = "clientes.csv"

def carregar_clientes():
    if os.path.exists(CAMINHO_CLIENTES):
        return pd.read_csv(CAMINHO_CLIENTES, sep=",")
    else:
        return pd.DataFrame(columns=["Nome", "CACEAL1", "CACEAL2"])

def salvar_cliente(nome, c1, c2):
    if os.path.exists(CAMINHO_CLIENTES):
        df = pd.read_csv(CAMINHO_CLIENTES, sep=",")
    else:
        df = pd.DataFrame(columns=["Nome", "CACEAL1", "CACEAL2"])

    # Forçar colunas corretas
    df = df[["Nome", "CACEAL1", "CACEAL2"]] if not df.empty else pd.DataFrame(columns=["Nome", "CACEAL1", "CACEAL2"])

    novo = pd.DataFrame([[nome, c1, c2]], columns=["Nome", "CACEAL1", "CACEAL2"])
    df = pd.concat([df, novo], ignore_index=True)
    df.to_csv(CAMINHO_CLIENTES, index=False)

aba = st.sidebar.radio("Menu", ["📋 Cadastrar Clientes", "🔎 Consultar Publicações"])

if aba == "📋 Cadastrar Clientes":
    st.subheader("Cadastro de Clientes")
    with st.form("cadastro_cliente"):
        nome = st.text_input("Nome do Cliente")
        caceal1 = st.text_input("CACEAL 1")
        caceal2 = st.text_input("CACEAL 2")
        submitted = st.form_submit_button("Salvar Cliente")
        if submitted and nome and caceal1:
            salvar_cliente(nome, caceal1, caceal2)
            st.success("✅ Cliente salvo com sucesso!")

    st.divider()
    st.subheader("📄 Clientes Cadastrados")
    st.dataframe(carregar_clientes())

if aba == "🔎 Consultar Publicações":
    st.subheader("Buscar Publicações")
    df_clientes = carregar_clientes()
    cliente_sel = st.selectbox("👤 Selecione um cliente", df_clientes["Nome"].unique() if not df_clientes.empty else [])

    if cliente_sel:
        dados_cliente = df_clientes[df_clientes["Nome"] == cliente_sel].iloc[0]
        c1 = dados_cliente["CACEAL1"]
        c2 = dados_cliente["CACEAL2"]

        col1, col2 = st.columns(2)
        with col1:
            data_inicio = st.date_input("📅 Data Início")
        with col2:
            data_fim = st.date_input("📅 Data Fim")

        if st.button("🔍 Buscar Publicações"):
            datas = pd.date_range(data_inicio, data_fim)
            resultados = []

            with st.spinner("Consultando edições..."):
                for data in datas:
                    data_str = data.strftime("%Y-%m-%d")
                    r = requests.get(f"https://diario.imprensaoficial.al.gov.br/apinova/api/editions/searchEditionByDate?editionDate={data_str}")
                    if r.status_code == 200 and r.json():
                        edicao_id = r.json()[0]["id"]
                        pdf_url = f"https://diario.imprensaoficial.al.gov.br/apinova/api/editions/downloadPdf/{edicao_id}"
                        pdf_res = requests.get(pdf_url)
                        if pdf_res.status_code == 200:
                            reader = PdfReader(BytesIO(pdf_res.content))
                            for i, page in enumerate(reader.pages):
                                texto = page.extract_text()
                                if not texto:
                                    continue
                                if any(x.lower() in texto.lower() for x in [cliente_sel.lower(), c1.lower(), c2.lower()]):
                                    caceal_encontrado = c1 if c1 in texto else c2
                                    resultados.append({
                                        "Data da Publicação": data.strftime("%d/%m/%Y"),
                                        "Cliente": cliente_sel,
                                        "CACEAL": caceal_encontrado
                                    })
                                    with tempfile.TemporaryDirectory() as path:
                                        images = convert_from_bytes(pdf_res.content, first_page=i+1, last_page=i+1, output_folder=path)
                                        st.image(images[0], caption=f"🗓️ {data.strftime('%d/%m/%Y')} • Cliente: {cliente_sel} • CACEAL: {caceal_encontrado}", use_column_width=True)
                                    break

            if resultados:
                df_resultado = pd.DataFrame(resultados)
                st.success("✅ Publicações encontradas no período selecionado.")
                st.dataframe(df_resultado)
                st.download_button("📥 Baixar Excel", df_resultado.to_excel(index=False, engine='openpyxl'), file_name="publicacoes_resultado.xlsx")
            else:
                st.warning("Nenhuma publicação encontrada no período e cliente selecionados.")
