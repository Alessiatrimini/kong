from IPython import embed
from PIL import Image
import streamlit as st
import hydralit_components as hc
import plotly.express as px
import pandas as pd
from config import *
from Aclass.CervedCall import CervedCall

st.set_page_config(layout="wide", initial_sidebar_state="collapsed")


menu_id = hc.nav_bar(
    menu_definition=menu_data,
    override_theme=over_theme,
    home_name="Dati sui fornitori",
    # login_name="Logout",
    hide_streamlit_markers=True,  # will show the st hamburger as well as the navbar now!
    sticky_nav=True,  # at the top or not
    sticky_mode="pinned",  # jumpy or not-jumpy, but sticky or pinned
)

# if menu_id == "Login":
#     ######## LOGIN ########
#     basewidth = 100
#     img = Image.open(LOGO_PATH)
    # wpercent = basewidth / float(img.size[0])
    # hsize = int((float(img.size[1]) * float(wpercent)))
    # img = img.resize((basewidth, hsize), Image.LANCZOS)

    # col1, col2, col3, col4, col5, col6, col7= st.columns(7)
    # col4.image(img, width=250)
    # col1, col2, col3 = st.columns(3)
    # col2.markdown(
    #     f"<h1 style='text-align: center; font-weight: bold; ont-size:20px;'>Kong Analytics</h1>",
    #     unsafe_allow_html=True,
    # )

    # st.write("")
#     ## VERIFICA DELL'UTENTE PER L'ACCESSO
#     if "user" not in st.session_state.keys():
#         st.session_state["user"] = col2.text_input(
#             "USERNAME", value="", help="Inserisci la tua email"
#         )
#     elif st.session_state["user"] == "":
#         st.session_state["user"] = col2.text_input(
#             "USERNAME", value="", help="Inserisci la tua email"
#         )

#     if st.session_state["user"].split("@")[0].upper() == 'ADMIN': #in abilitazioni.USERNAME.tolist():
#         col2.text("ACCESSO EFFETTUATO")
#         user = st.session_state["user"].split("@")[0]
#         message = f"{user.upper()} ha effettuato l'accesso."

#     elif st.session_state["user"] == "":
#         col2.text("")
#     elif (
#         st.session_state["user"].split("@")[0].upper()
#         != 'admin' #not in abilitazioni.USERNAME.tolist()
#     ):
#         col2.text("USERNAME ERRATO")

# if "user" in st.session_state.keys():
#     if st.session_state["user"].split("@")[0].upper() == 'ADMIN': #in abilitazioni.USERNAME.tolist():
#         username = st.session_state["user"].split("@")[0].upper()



if menu_id == "Dati sui fornitori":
        # with st.container():
        #     col1, col2, col3 = st.columns(3)
        #     with col1:
        #         piva = st.text_input('Piva', value = "02663091219", placeholder ='Inserici la Piva che vuoi ricercare', label_visibility='collapsed') #05907491210
        #     with col2:
        #         st.button('🔍',  key="btn_search")

        
        # if st.session_state.get("btn_search"):
        param = st.experimental_get_query_params()
        piva = param["piva"][0]
        call = CervedCall(piva, apival)
        nege = call.get_negevents()
        ragsoc = nege[0]['name']
        st.title(f"{ragsoc.upper()} -  PIVA: {piva}")

        st.header("Eventi negativi", divider = "gray")


    
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        try:
            k = list(negative_events)[0]
            len_prot  = len(nege[0][k])
            col1.metric(negative_events[k], len_prot)
            with col1:
                with st.expander("Dettagli"):
                    for n in nege[0][k]:
                        st.write(n['protests_registry'][0]['refusal_reason'])  
                        st.write("")
        except:
            col1.metric(negative_events[k], 0)
                
        try:
            k = list(negative_events)[1]
            len_prot  = len(nege[0][k])
            col2.metric(negative_events[k], len_prot)
            with col2:
                with st.expander("Dettagli"):
                    for n in nege[0][k]:
                        st.write(f"{n['deed_description']} - {n['beneficiary_subjects_personal_data'][0]['name']}")
                        st.write("")
        except:
            col2.metric(negative_events[k], 0)
        
        try:
            k = list(negative_events)[2]
            len_prot  = len(nege[0][k])
            col3.metric(negative_events[k], len_prot)
            with col3:
                with st.expander("Dettagli"):
            
                    for n in nege[0][k]:
                        st.write(f"{n['procedure_type']}")
                        st.write("")
        except:
            col3.metric(negative_events[k], 0)
        
        try:
            k = list(negative_events)[3]
            len_prot  = len(nege[0][k])
            col4.metric(negative_events[k], len_prot)
            with col4:
                with st.expander("Dettagli"):
                    for n in nege[0][k]:
                        st.write(f"{n['procedure_type']}")
                        st.write("")
        except:
            col4.metric(negative_events[k], 0)
        
        try:
            k = list(negative_events)[4]
            len_prot  = len(nege[0][k])
            col5.metric(negative_events[k], len_prot)
        except:
            col5.metric(negative_events[k], 0)
        
        try:
            k = list(negative_events)[5]
            len_prot  = len(nege[0][k])
            col6.metric(negative_events[k], len_prot)
        except:
            col6.metric(negative_events[k], 0)

        st.header("Dati di bilancio", divider = "gray")
        bilanci = call.get_bilanci()
        # st.write(bilanci)

        final_bilanci = pd.DataFrame()
        for key in bilanci.keys():
            # print(key)
            bilancio =  pd.DataFrame(bilanci[key]["conto_economico"]["voci"])
            bilancio_temp = bilancio.loc[bilancio.voce.isin(bilancio_key)]
            bilancio_temp['anno'] = key
            final_bilanci = pd.concat([final_bilanci, bilancio_temp[["anno","voce", "valore"]].copy()], ignore_index=True)
        
        # fig = px.line(final_bilanci, x=final_bilanci['anno'], y=final_bilanci['valore'], color = final_bilanci['voce'],markers=True)
        # st.plotly_chart(fig, use_container_width=True)
        for voce in final_bilanci.voce.tolist():
            try:
                data = final_bilanci.loc[final_bilanci.voce == voce]
                fig = px.line(data, x=data['anno'], y=data['valore'], title = voce.upper(), markers=True)
                st.plotly_chart(fig, use_container_width=True)
            except:
                pass




        # i = 0
        # for k in negative_events.keys():
        #     print(cols[i])
        #     with cols[i]:
        #         try:
        #             len_prot  = len(nege[0][k])
        #             st.metric(label=negative_events[k], value=len_prot)
                # except:
                #     st.metric(label=negative_events[k], value=0)

        # st.write(nege)
        

        # negf = call.get_negflag()
        # st.write(negf)
