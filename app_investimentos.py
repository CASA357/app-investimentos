import streamlit as st
import pandas as pd

# -------------------------------------------------------------------
# 1. SIMULAÇÃO DE LIGAÇÃO ÀS APIS (Substituiremos pelas reais depois)
# -------------------------------------------------------------------
def get_xtb_data():
    # Aqui entrará o código WebSocket para a XStation5
    return [
        {"Ativo": "Bitcoin", "Corretora": "XTB", "Valor Atual (€)": 500, "Alvo (%)": 15},
        {"Ativo": "Ouro", "Corretora": "XTB", "Valor Atual (€)": 1200, "Alvo (%)": 15}
    ]

def get_t212_data():
    # Aqui entrará o código HTTP Request para a API da Trading 212
    return [
        {"Ativo": "VWCE (Global)", "Corretora": "Trading 212", "Valor Atual (€)": 4500, "Alvo (%)": 50},
        {"Ativo": "S&P 500", "Corretora": "Trading 212", "Valor Atual (€)": 1800, "Alvo (%)": 20}
    ]

# -------------------------------------------------------------------
# 2. INTERFACE E LÓGICA DA APP
# -------------------------------------------------------------------
st.set_page_config(page_title="O Meu Portefólio", layout="wide")
st.title("📊 Gestor de Portefólio - XTB & Trading 212")

# Barra lateral para inputs
st.sidebar.header("Novo Investimento")
novo_capital = st.sidebar.number_input("Capital a adicionar (€):", min_value=0.0, value=1000.0, step=50.0)

# Juntar os dados das duas corretoras
dados_carteira = get_xtb_data() + get_t212_data()
df = pd.DataFrame(dados_carteira)

# Cálculos Globais
valor_atual_total = df["Valor Atual (€)"].sum()
valor_futuro_total = valor_atual_total + novo_capital
soma_alvos = df["Alvo (%)"].sum()

# Mostrar avisos se as percentagens não baterem certo
if soma_alvos != 100:
    st.error(f"Atenção: A soma dos teus alvos é {soma_alvos}%. Tem de ser exatamente 100%.")

# Matemática de Rebalanceamento
df["Valor Alvo (€)"] = valor_futuro_total * (df["Alvo (%)"] / 100)
df["Ação Necessária (€)"] = df["Valor Alvo (€)"] - df["Valor Atual (€)"]

# Formatar a coluna de Ação para dizer "Comprar" ou "Vender"
def formatar_acao(valor):
    if valor > 0:
        return f"🟢 Comprar: {valor:.2f} €"
    elif valor < 0:
        return f"🔴 Vender: {abs(valor):.2f} €"
    return "⚪ Equilibrado"

df["O que fazer?"] = df["Ação Necessária (€)"].apply(formatar_acao)

# Limpar visualização da tabela
df_display = df[["Ativo", "Corretora", "Valor Atual (€)", "Alvo (%)", "O que fazer?"]]

# Mostrar Métricas no topo
col1, col2, col3 = st.columns(3)
col1.metric("Valor Atual da Carteira", f"{valor_atual_total:.2f} €")
col2.metric("Capital a Adicionar", f"{novo_capital:.2f} €")
col3.metric("Valor Futuro Projetado", f"{valor_futuro_total:.2f} €")

st.write("### O teu plano de ação:")
st.dataframe(df_display, use_container_width=True, hide_index=True)