
# Código para rodar no Google Colab

# 1. Faça upload do arquivo bolao_copa_python.zip no Colab.

# 2. Descompacte:
!unzip bolao_copa_python.zip

# 3. Entre na pasta:
%cd bolao_copa_python

# 4. Instale as dependências:
!pip install -r requirements.txt

# 5. Rode o app com link público temporário:
!streamlit run app.py & npx localtunnel --port 8501
