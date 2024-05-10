#Código do chatbot pensado para a Imersão Alura + Google

#importando bibliotecas a serem utilizadas
import google.generativeai as genai
import streamlit as st
from PIL import Image
import numpy as np

#configurando a chave de api


#definindo favicon e configurações iniciais do WebApp
favicon = Image.open('utilities/logotipo.png')
st.set_page_config(page_title='TecnoGuia ',page_icon=favicon,layout="wide", initial_sidebar_state="collapsed")


def verificar_preenchimento(*args):
    for preenchimento in args:
        if len(preenchimento)==0:
            return 0
    return 1

def main():
    #definindo titulo da página
    st.markdown("<h1 style='text-align: center;'>TecnoGuia</h1>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center;'>O TecnoGuia é um assistente criado utilizando a API do Google Gemini, para instruir jovens com interesse em tecnologia em qual carreira seguir.</h5>", unsafe_allow_html=True)
    
    st.markdown("<h5 style='text-align: center;'>Para utilizar é fácil: basta preencher abaixo com a sua GOOGLE API KEY, que pode ser criada **aqui** e os campos seguintes com as suas informações e clicar em enviar. Dessa forma, o Gemini vai poder te direcionar melhor!</h5>", unsafe_allow_html=True)
    
    GOOGLE_API_KEY = st.text_input('Insira aqui a sua GOOGLE API KEY')
    genai.configure(api_key=GOOGLE_API_KEY)
    st.write(GOOGLE_API_KEY)
    
    st.write('---')
    generation_config={
    "candidate_count":1,
    "temperature":0.5,
    }

    safety_settings={
    'HARASSMENT':'BLOCK_NONE',
    'HATE':'BLOCK_NONE',
    'SEXUAL':'BLOCK_NONE',
    'DANGEROUS':'BLOCK_NONE',
    }
    model=genai.GenerativeModel(model_name="gemini-1.0-pro",safety_settings=safety_settings,generation_config=generation_config)

    


    with st.container(border=True):
        col1,col2,col3,col4,col5 = st.columns(5)
        with col1:
            areas_interesse=st.multiselect("1. Selecione suas áreas de interesse: ",options=['Programação','Design','Redes','Segurança','Dados','Robótica'])
            habilidades=st.multiselect("2. Selecione suas habilidades: ",options=['Lógica','Criatividade','Comunicação','Resolução de problemas','Pensamento Crítico','Adaptabilidade','Colaboração','Gestão de tempo'])
        with col2:
            estilo_aprendizagem=st.radio("3. Selecione seu estilo de aprendizagem favorito:",options=['Aulas teóricas','Aulas práticas','Ambas'])
            if estilo_aprendizagem=="Ambas":
                estilo_aprendizagem="Aulas teóricas e práticas"
            perfil_profissional=st.radio("4. Como você se vê trabalhando?",options=['Em equipe','Sozinho'])
        with col3:
            nivel_matematica=st.radio("5. O quão confortável você se sente com matemática e lógica?",options=['Muito confortavel','Moderadamente confortável','Pouco confortável','Nada confortável'])
            criatividade=st.radio("6. Você gosta de criar e inovar ou seguir processos ja estabelecidos?",options=["Criar e inovar",'Seguir processos estabelecidos'])
        with col4:
            comunicacao=st.radio("7. Você tem facilidade para se comunicar e trabalhar em equipe?",options=['Sim, tenho facilidade', 'Não tenho facilidade'])
            afinidade_linguagens=st.radio("8. Você tem interesse em linguagens de programação ou prefere áreas mais visuais?",options=['Interesse em linguagens','Prefiro áreas mais visuais'])
        with col5:
            pensamento_logico=st.radio("9. Você se considera uma pessoa com raciocínio lógico apurado?",options=['Sim, tenho raciocinio lógico apurado','Não tenho raciocinio lógico apurado'])
            resolucao_problemas=st.radio("10. Você gosta de desafios e encontrar soluções para problemas complexos?",options=['Sim','Não'])
            if resolucao_problemas == "Sim":
                resolucao_problemas="Gosto"
            elif resolucao_problemas == "Não":
                resolucao_problemas ="Não gosto"
    ativar= st.button("Enviar",use_container_width=False)
    if ativar:
        check=verificar_preenchimento(areas_interesse,habilidades)
        if check == 0:
            st.error("Por favor, selecione pelo menos uma opção nos campos 1 e 2.")
        else:
            with st.spinner ('Ótimas opções! Estou pensando nos melhores cursos para você...'):
                texto = f'''Olá Gemini! Sou um estudante do ensino médio interessado em seguir carreira na área de tecnologia, mas preciso de ajuda para escolher o curso de graduação ideal. Para que você possa me conhecer melhor, aqui estão algumas informações sobre mim:
                        Áreas de Interesse: {areas_interesse};
                        Habilidades: {habilidades};
                        Estilo de Aprendizagem: {estilo_aprendizagem};
                        Perfil Profissional: me vejo trabalhando {perfil_profissional};
                        Nível de Matemática: eu me sinto {nivel_matematica} com matemática e lógica;
                        Criatividade: eu gosto de {criatividade};
                        Comunicação: {comunicacao} para me comunicar em equipe.;
                        Afinidade com Linguagens: eu {afinidade_linguagens};
                        Pensamento Lógico: {pensamento_logico};
                        Resolução de Problemas: {resolucao_problemas} gosto de desafios e encontrar soluções para problemas complexos;

                        Com base nessas informações, você poderia me sugerir até 2 cursos de graduação em tecnologia que se encaixam no meu perfil?
                        A partir disso, resuma levemente, em até 2 linhas, os cursos indicados.'''
                
                response = model.generate_content(texto)
                st.write(response.text)

if __name__ == '__main__':
    main()