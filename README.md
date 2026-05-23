
# Bolão da Copa 2026 em Python

Este projeto é um sistema de bolão feito em Python com Streamlit e SQLite.

## O que tem no sistema

- Login de usuários;
- Cadastro de apostadores;
- Login de administrador;
- Dashboard colorido;
- Top 5 apostadores;
- Ranking geral;
- Tela de jogos e palpites;
- Bloqueio de palpite após início do jogo;
- Painel administrador;
- Cadastro de jogos;
- Lançamento de resultados;
- Cálculo automático de pontos.

## Login inicial do administrador

E-mail:

```text
admin@bolao.com
```

Senha:

```text
admin123
```

Depois que testar, altere essa senha no banco ou crie outro administrador.

## Como rodar no computador

No terminal:

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Como rodar no Google Colab

1. Crie um notebook novo no Colab.
2. Faça upload do arquivo ZIP do projeto.
3. Rode:

```python
!unzip bolao_copa_python.zip
%cd bolao_copa_python
!pip install -r requirements.txt
```

4. Depois rode:

```python
!streamlit run app.py & npx localtunnel --port 8501
```

O Colab vai mostrar um link público temporário.

## Observação sobre hospedagem

Colab serve para teste. Para deixar online de verdade, recomendo hospedar em:

- Streamlit Community Cloud;
- Render;
- Railway;
- VPS;
- servidor próprio.

Para algo profissional com muitos usuários, o ideal é trocar o SQLite por PostgreSQL.


## Correção para erro de dependências no Colab

Se aparecer erro envolvendo `protobuf`, `numpy`, `opencv-python`, `shap` ou `grain`, use o `requirements.txt` corrigido desta versão.

No Colab, rode:

```python
!pip install -q streamlit pyngrok
```

Depois:

```python
!streamlit run app.py & npx localtunnel --port 8501
```

Esses avisos geralmente acontecem porque o Colab já vem com várias bibliotecas instaladas e algumas têm versões diferentes. Para este projeto, precisamos basicamente de Streamlit; Pandas e SQLite já funcionam no ambiente.
