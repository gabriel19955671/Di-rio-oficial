# 📄 Monitor Diário Oficial de Alagoas

Este projeto é um sistema em Python com interface web (Streamlit) que permite monitorar automaticamente as publicações do Diário Oficial de Alagoas para empresas específicas.

## 🔧 Funcionalidades

- Cadastro de clientes com nome e dois números de CACEAL
- Consulta automática por nome ou CACEAL no Diário Oficial (por data)
- Exibição da página do diário com a publicação encontrada
- Exportação dos resultados em formato Excel (.xlsx)

## 🚀 Como usar

1. Clone este repositório:

```bash
git clone https://github.com/seu-usuario/diario-oficial-al.git
cd diario-oficial-al
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o sistema com Streamlit:

```bash
streamlit run app.py
```

## 📁 Estrutura

```
📦 diario-oficial-al
├── app.py             # Código principal do app Streamlit
├── clientes.csv       # Arquivo com cadastro de clientes
├── requirements.txt   # Lista de bibliotecas necessárias
└── README.md          # Este arquivo
```

## 🌐 Publicação

Este projeto é compatível com o [Streamlit Cloud](https://streamlit.io/cloud) para publicação online gratuita.

---
Criado por Gabriel Vilela Contador.
