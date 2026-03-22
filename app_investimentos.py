import streamlit as st
import pandas as pd

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Gestor de Portefólio Total", layout="wide")

st.title("📈 Controlo de Investimentos: XTB, T212 e Trade Republic")

# --- 1. ENTRADA DE DADOS (Saldos Atuais) ---
# Por agora, vamos inserir manualmente. No próximo passo, ligamos as APIs.
st.sidebar.header("💰 Valores Atuais na Carteira")

with st.sidebar.expander("Saldos por Corretora"):
    valor_xtb = st.number_input("Total na XTB (€)", min_value=0.0, value=1000.0)
    valor_t212 = st.number_input("Total na Trading 212 (€)", min_value=0.0, value=2500.0)
    valor_tr = st.number_input("Total na Trade Republic (€)", min_value=0.0, value=1500.0)

st.sidebar.divider()
st.sidebar.header("💸 Novo Aporte")
novo_investimento = st.sidebar.number_input("Quanto vais investir hoje? (€)", min_value=0.0, value=500.0)

# --- 2. DEFINIÇÃO DA ESTRATÉGIA (%) ---
# Aqui defines quanto queres ter de cada coisa
st.write("### 🎯 Definir Alvos de Alocação")
st.info("Define que percentagem da tua carteira total queres em cada corretora ou ativo.")

col_a, col_b, col_c = st.columns(3)
alvo_xtb = col_a.slider("% Alvo XTB", 0, 100, 20)
alvo_t212 = col_b.slider("% Alvo Trading 212", 0, 100, 50)
alvo_tr = col_c.slider("% Alvo Trade Republic", 0, 100, 30)

total_alvo = alvo_xtb + alvo_t212 + alvo_tr

if total_alvo != 100:
    st.warning(f"⚠️ A soma das percentagens é {total_alvo}%. Deve ser 100% para o cálculo estar correto.")

# --- 3. CÁLCULOS DE REBALANCEAMENTO ---
valor_total_atual = valor_xtb + valor_t212 + valor_tr
valor_total_pos_investimento = valor_total_atual + novo_investimento

# Criar tabela de dados
dados = {
    "Corretora": ["XTB", "Trading 212", "Trade Republic"],
    "Valor Atual (€)": [valor_xtb, valor_t212, valor_tr],
    "Alvo (%)": [alvo_xtb, alvo_t212, alvo_tr]
}

df = pd.DataFrame(dados)

# Cálculo do valor que deveria ter
df["Valor Ideal (€)"] = (valor_total_pos_investimento * (df["Alvo (%)"] / 100))

# Cálculo da diferença (Quanto falta investir)
df["A Reforçar (€)"] = df["Valor Ideal (€)"] - df["Valor Atual (€)"]

# --- 4. EXIBIÇÃO DOS RESULTADOS ---
st.divider()
m1, m2, m3 = st.columns(3)
m1.metric("Total Atual", f"{valor_total_atual:.2f} €")
m2.metric("Novo Investimento", f"{novo_investimento:.2f} €")
m3.metric("Novo Total Projetado", f"{valor_total_pos_investimento:.2f} €")

st.write("### 🚀 Sugestão de Reforço")

# Formatar a tabela para ficar fácil de ler
def destacar_reforco(val):
    color = 'green' if val > 0 else 'white'
    return f'color: {color}; font-weight: bold'

st.dataframe(df.style.applymap(destacar_reforco, subset=['A Reforçar (€)']), use_container_width=True)

st.success("Dica: Os valores em verde na coluna 'A Reforçar' são os que deves depositar em cada conta hoje.")