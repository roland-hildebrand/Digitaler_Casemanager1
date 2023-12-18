'''
Run Befehl ist:
streamlit run "C:/Users/Paul Wunderlich/PycharmProjects/Digitaler_Casemanager/digital_casemanager.py"
##################################
# Markdown Template:
st.markdown("* **Modul:**  Text")
##################################
# Alternative page_names
page_names = ["Einleitung",
              "Mobilität",
              "Kognitive und kommunikative Fähigkeiten",
              "Verhaltensweisen und psychische Problemlagen",
              "Selbstversorgung",
              "Umgang mit krankheits- oder therapiebedingten Anforderungen",
              "Gestaltung des Alltagslebens und sozialer Kontakte",
              "Gestaltung der Betreuung",
              "Analyse und Weitere Schritte"]

'''
# Credits
__author__ = "Paul Wunderlich"
__copyright__ = "Copyright 2022, inIT work&care project"
__email__ = "paul.wunderlich@th-owl.de"
__status__ = "Dev"

# Libaries
import streamlit as st
import pandas as pd
import pickle

####################################################################################################
# Predefine variables
questions = ["Positionswechsel im Bett (bspw. Drehen und Wenden im Bett)",
              "Halten in der Sitzposition",
              "Aufstehen aus dem Sitz",
              "Umsetzen vom Bett bspw. in den Rollstuhl",
              "Sich innerhalb der Wohnung bewegen",
              "Sich außerhalb der Wohnung bewegen",
              "Treppensteigen",
              "Erkennen von vertrauten Personen",
              "Wissen von Uhrzeit und Datum",
              "Erinnerung an vergangene  Ereignisse (bspw. Familienfeiern, Reisen)",
              "Können Gefahren eingeschätzt werden (Herd ausgeschaltet?)",
              "Mitteilung von Bedürfnissen (bspw. Hunger oder Durst)",
              "Beteiligung an Gesprächen",
              "Verstehen von Aufforderungen",
              "Aggressives oder abwehrendes Verhalten",
              "Antriebslosigkeit",
              "Ängste",
              "traurige Stimmungslage",
              "Kämmen, Rasieren, Zähneputzen",
              "Waschen, Baden, Duschen",
              "An- und Auskleiden",
              "Toilettengang",
              "Essen zerkleinern, Flaschen öffnen",
              "Essen, Trinken",
              "Zubereitung von Mahlzeiten",
              "Einkaufen",
              "Reinigung von Wohnung od. Haus",
              "Instandhaltung von Wohnung od. Haus",
              "Gartenpflege",
              "Bereitstellung und/ oder Gabe von Medikamenten",
              "Anziehen von Kompressionsstrümpfen",
              "Gabe von Spritzen",
              "Verbandwechsel/ Wundversorgung",
              "Physiotherapeutische Übungen",
              "Arztbesuche oder Besuch anderer medizinischer Einrichtungen",
              "Einhaltung einer Diät",
              "Messung von Blutdruck-oder Blutzuckerwerten ect.",
              "Eigene Beschäftigung (bspw. Lesen, Musik hören)",
              "Gestaltung des Tagesrhythmus (z.B. Frühstück, Mittag- und Abendessen)",
              "Organisation von Aktivitäten (Spaziergang/-fahrt mit Bekannten/ Verwandten)",
              "Eigene Interaktion mit anderen Personen (z.B. persönliches Gespräch, Telefonat, WhatsApp, E-Mail)",
              "Ehe- od. Lebenspartner",
              "Eltern od. Kinder",
              "Nahe Angehörige wie bspw. Geschwister od. Nichte/Neffe",
              "Bekannte od. Freunde",
              "Nachbarn od. ehrenamtliche Personen",
              "Professionelle Dienstleister wie bspw. ambulanter Pflegedienst od. stationäre Pflegeeinrichtung"]

answers_a = ["Ohne fremde Hilfe möglich",
             "Etwas fremde Hilfe nötig",
             "Überwiegend fremde Hilfe nötig",
             "Komplett fremde Hilfe nötig",
             "Nicht erforderlich"]

answers_b = ["Immer",
             "Häufig",
             "Selten",
             "Nie"]

answers_c = ["Keine Auffälligkeiten",
             "Leichte Auffälligkeiten",
             "Mäßige Auffälligkeiten",
             "Schwere Auffälligkeiten"]

answers_d = ["Ja",
             "Nein"]

# Initialze further steps
further_steps = ["Altersgerechtes Wohnen zu Hause", "Ambulante Pflege", "Arzt", "Betreuung & Begleitung", "Einkauf",
                 "Ergotherapie", "Ernährung", "Haushaltshilfe", "Hilfsmittel", "Logopädie", "Medikamente",
                 "Mobilität & Bewegung", "Physiotherapie", "Psychotherapie", "Selbsthilfe & Unterstützungsangebote",
                 "Stationäre Pflege", "Nichts"]
####################################################################################################
# Funktionen


def recommend_next_steps(antworten):

    # Erstellung eines dictionaries aus zwei Listen -> data=Liste von Listen
    dict_data = dict(zip(questions, antworten))

    answers = pd.DataFrame.from_dict(dict_data)

    # Antworten in Zahlen umwandeln
    vals_to_replace = {"Ohne fremde Hilfe möglich": 1, "Etwas fremde Hilfe nötig": 2,
                        "Überwiegend fremde Hilfe nötig": 3,
                        "Komplett fremde Hilfe nötig": 4, "Nicht erforderlich": 0,
                        "Immer": 1, "Häufig": 2, "Selten": 3, "Nie": 4,
                        "Keine Auffälligkeiten": 1, "Leichte Auffälligkeiten": 2, "Mäßige Auffälligkeiten": 3,
                        "Schwere Auffälligkeiten": 4,
                        "Ja": 1, "Nein": 2}
    for column in answers:
        answers[column] = answers[column].map(vals_to_replace)

    # Laden des gelernten Vorhersagemodells
    filename = './models/multi-label-clf_v4.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    # Inference
    prediction = loaded_model.predict(answers)

    return prediction

####################################################################################################
# Passwortmanager in der Sidebar
st.sidebar.title("Digitaler Case Manager")
st.sidebar.markdown("Bitte geben Sie den Benutzernamen und das Passwort ein und setzen den Haken neben Login!")
username = st.sidebar.text_input("Benutzername:")
password = st.sidebar.text_input("Passwort:",type='password')


# Falls Login korrekt -> Digitaler Case Manager
if st.sidebar.checkbox("Login") and username == st.secrets["admin_name"] and password == st.secrets["admin_password"]:
    # Erfolgsmeldung in der Sidebar
    st.sidebar.success("Anmeldung erfolgreich!")

    # Logos
    col1, col2 = st.columns(2)
    col1.image("images/InIT-Logo.png", width=256)
    col2.image("images/Logo work_care.png", width=256)

    # Einleitung
    st.title("Digitaler Case Manager")


    st.markdown("### Herzlich Willkommen zum Digitalen Case Manager! ")
    st.markdown("Zunächst möchten wir Ihnen den digitalen Case Manager kurz vorstellen.")
    st.markdown("In den folgenden Modulen finden Sie Fragen zu den Bereichen: Mobilität, kognitive und "
                "kommunikative Fähigkeiten, Verhaltensweisen und psychische Problemlagen, Selbstversorgung, "
                "Umgang mit krankheits- oder therapiebedingten Anforderungen, Gestaltung des Alltagslebens "
                "und der sozialen Kontakte sowie der Gestaltung der derzeitigen Betreuungssituation. Gerne "
                "können Sie sich hierzu in der nachstehenden Dropbox informieren."
               )

    explanation = st.expander("Erläuterung zu den Modulen")
    with explanation:
        st.markdown("Die Fragestellungen sind in folgende sieben Module unterteilt: ")
        st.markdown("* **Modul 1 „Mobilität“:**  \n"  
                    " Hier finden Sie Fragen nach der Inanspruchnahme von fremder Hilfe wie "
                    "beispielsweise beim Aufstehen oder Treppensteigen.")
        st.markdown("* **Modul 2 „Kognitive und kommunikative Fähigkeiten“:**  \n"
                    "In diesem Modul werden Fragen nach "
                    "geistigen Beeinträchtigungen gestellt wie etwa: Kann sich die zupflegende Person mitteilen?")
        st.markdown("* **Modul 3 „Verhaltensweisen und psychische Problemlagen“:**  \n"
                    "In diesem Modul werden Fragen bezüglich "
                    "aggressiven Verhaltens, zu Ängsten oder traurigen Stimmungslagen des Betroffenen gestellt.")
        st.markdown("* **Modul 4 „Selbstversorgung“:**  \n"
                    "Dieses Modul beinhaltet Fragestellungen hinsichtlich der "
                    "Körperpflege und der Haushaltsführung.")
        st.markdown("* **Modul 5 „Umgang mit krankheits- oder therapiebedingten Anforderungen“:**  \n"
                    "Hier finden Sie Fragen, "
                    "ob Ihr Angehöriger selbständig Medikamente einnehmen oder Blutzucker messen kann.")
        st.markdown("* **Modul 6 „Gestaltung des Alltagslebens und sozialer Kontakte“:**  \n"
                    "In diesem Modul liegt "
                    "der Schwerpunkt auf der Frage, ob die zu pflegende Person ihren Alltag selbständig planen und mit "
                    "anderen Menschen in Kontakt treten kann.")
        st.markdown("* **Modul 7 „Gestaltung der Betreuung“:**  \n"
                    "Im letzten Modul werden Sie danach gefragt, welche Personen"
                    " die zu pflegende Person unterstützen oder betreuen.")

    st.markdown("Diese Module orientieren sich an dem Auskunftsbogen zur Vorbereitung auf eine Pflegebegutachtung des "
                "[Medizinischen Dienstes](https://www.medizinischerdienst.de/). Diese Pflegebegutachtung ist erforderlich, "
                "wenn Sie Leistungen im Rahmen der gesetzlichen Pflegeversicherung beantragen möchten."
               )
    
    st.markdown("##### Fragebogen")
    st.markdown("Nehmen Sie sich nun etwas Zeit zur Beantwortung der Fragen, um sich ein umfassendes Bild über Ihre "
                "Möglichkeiten zur Versorgungsplanung in Ihrer derzeitigen Pflegesituation zu verschaffen. ")

    ######################################
    ## Horizontale Auswahlmöglichkeiten
    #st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    # Modul 1
    modul_1 = st.expander("Modul 1: Mobilität", expanded=False)
    with modul_1:
        # Questions for Modul 1
        m1_1, m1_2, m1_3, m1_4, m1_5, m1_6, m1_7 = st.empty(), st.empty(), st.empty(), st.empty(),\
                                                   st.empty(), st.empty(), st.empty()

        m1 = []
        m1_keys = ["m1f1", "m1f2", "m1f3", "m1f4", "m1f5", "m1f6", "m1f7"]
        m1_ids = (m1_1, m1_2, m1_3, m1_4, m1_5, m1_6, m1_7)
        for i, elem in enumerate(m1_ids):
            m1.append([elem.radio(f"{i+1}. {questions[i]}:", answers_a, key=m1_keys[i])])

    ######################################
    # Modul 2
    modul_2 = st.expander("Modul 2: Kognitive und kommunikative Fähigkeiten", expanded=False)
    with modul_2:
        # Questions for Modul 2
        m2_1, m2_2, m2_3, m2_4, m2_5, m2_6, m2_7 = st.empty(), st.empty(), st.empty(), st.empty(),\
                                                   st.empty(), st.empty(), st.empty()

        m2 = []
        m2_keys = ["m2f1", "m2f2", "m2f3", "m2f4", "m2f5", "m2f6", "m2f7"]
        m2_ids = (m2_1, m2_2, m2_3, m2_4, m2_5, m2_6, m2_7)
        for i, elem in enumerate(m2_ids):
            m2.append([elem.radio(f"{i+8}. {questions[i+7]}:", answers_b, key=m2_keys[i])])

    ######################################
    # Modul 3
    modul_3 = st.expander("Modul 3: Verhaltensweisen und psychische Problemlagen", expanded=False)
    with modul_3:
        # Questions for Modul 3
        m3_1, m3_2, m3_3, m3_4 = st.empty(), st.empty(), st.empty(), st.empty()

        m3 = []
        m3_keys = ["m3f1", "m3f2", "m3f3", "m3f4"]
        m3_ids = (m3_1, m3_2, m3_3, m3_4)
        for i, elem in enumerate(m3_ids):
            m3.append([elem.radio(f"{i+15}. {questions[i+14]}:", answers_c, key=m3_keys[i])])

    ######################################
    # Modul 4
    modul_4 = st.expander("Modul 4: Selbstversorgung", expanded=False)
    with modul_4:
        # Questions for Modul 4
        m4_1, m4_2, m4_3, m4_4, m4_5, m4_6 = st.empty(), st.empty(), st.empty(), st.empty(), st.empty(), st.empty()
        m4_7, m4_8, m4_9, m4_10, m4_11 = st.empty(), st.empty(), st.empty(), st.empty(), st.empty()

        m4 = []
        m4_keys = ["m4f1", "m4f2", "m4f3", "m4f4", "m4f5", "m4f6", "m4f7", "m4f8", "m4f9", "m4f10", "m4f11"]
        m4_ids = (m4_1, m4_2, m4_3, m4_4, m4_5, m4_6, m4_7, m4_8, m4_9, m4_10, m4_11)
        for i, elem in enumerate(m4_ids):
            m4.append([elem.radio(f"{i+19}. {questions[i+18]}:", answers_a, key=m4_keys[i])])

    ######################################
    # Modul 5
    modul_5 = st.expander("Modul 5: Umgang mit krankheits- oder therapiebedingten Anforderungen", expanded=False)
    with modul_5:
        # Questions for Modul 5
        m5_1, m5_2, m5_3, m5_4 = st.empty(), st.empty(), st.empty(), st.empty()
        m5_5, m5_6, m5_7, m5_8 = st.empty(), st.empty(), st.empty(), st.empty()

        m5 = []
        m5_keys = ["m5f1", "m5f2", "m5f3", "m5f4", "m5f5", "m5f6", "m5f7", "m5f8"]
        m5_ids = (m5_1, m5_2, m5_3, m5_4, m5_5, m5_6, m5_7, m5_8)
        for i, elem in enumerate(m5_ids):
            m5.append([elem.radio(f"{i+30}. {questions[i+29]}:", answers_a, key=m5_keys[i])])

    ######################################
    # Modul 6
    modul_6 = st.expander("Modul 6: Gestaltung des Alltagslebens und sozialer Kontakte", expanded=False)
    with modul_6:
        # Questions for Modul 6
        m6_1, m6_2, m6_3, m6_4 = st.empty(), st.empty(), st.empty(), st.empty()

        m6 = []
        m6_keys = ["m6f1", "m6f2", "m6f3", "m6f4"]
        m6_ids = m6_1, m6_2, m6_3, m6_4
        for i, elem in enumerate(m6_ids):
            m6.append([elem.radio(f"{i+38}. {questions[i+37]}:", answers_b, key=m6_keys[i])])

    ######################################
    # Modul 7
    modul_7 = st.expander("Modul 7: Gestaltung der Betreuung", expanded=False)
    with modul_7:
        # Questions for Modul 7
        m7_1, m7_2, m7_3, m7_4, m7_5, m7_6 = st.empty(), st.empty(), st.empty(), st.empty(), st.empty(), st.empty()

        m7 = []
        m7_keys = ["m7f1", "m7f2", "m7f3", "m7f4", "m7f5", "m7f6"]
        m7_ids = m7_1, m7_2, m7_3, m7_4, m7_5, m7_6
        for i, elem in enumerate(m7_ids):
            m7.append([elem.radio(f"{i+42}. {questions[i+41]}:", answers_d, key=m7_keys[i])])

    ######################################
    # Weitere Schritte
    st.title("Analyse und Weitere Schritte")
    st.markdown('Durch das Klicken auf "Starte Analyse" beginnen starten Sie den Digitalen Case Manager.')
    start_inference = st.button("Starte Analyse")

    # Inferenz
    if start_inference:
        antworten = m1 + m2 + m3 + m4 + m5 + m6 + m7

        # Inference
        prediction = recommend_next_steps(antworten)

        # Umwandeln der Vorhersage in Text
        for column in range(len(prediction)):
            indices = [index for index, element in enumerate(prediction[column]) if element == 1]
            pred_steps = []
            for i in indices:
                pred_steps.append(further_steps[i])

            # Check ob weitere Pflegeschritte empfohlen wurden
            if pred_steps == ["Nichts"]:
                st.markdown("#### Anhand der gegebenen Antworten werden Ihnen keine weiteren Pflegeschritte empfohlen.")
            elif pred_steps:
                st.markdown("#### Es werden Ihnen folgende weitere Pflegeschritte empfohlen:")
                for step in pred_steps:
                    st.markdown(f"* {step}")
            else:
                st.subheader("Hier ist etwas schief gelaufen. Bitte wiederholen Sie den Digitalen Case Manager.")


else:
    st.sidebar.error("Benutzername / Passwort war nicht korrekt oder Sie haben den Haken vergessen!")

#Funding
st.sidebar.markdown("*Diese Arbeit wurde im Rahmen des Projekts work & care entwickelt. "
                    "Das Projekt wird vom Ministerium für Wirtschaft, Innovation, Digitalisierung und Energie des Landes "
                    "Nordrhein-Westfalen (MWIDE NRW) unter dem Förderkennzeichen __34.EFRE-0300198__ gefördert.*")
st.sidebar.image("images/EFRE_Foerderhinweis_deutsch_farbig.jpg")
st.sidebar.image("images/nrw-mweimh-logo.jpg")
st.sidebar.image("images/Ziel2NRW_RGB_1809_jpg.jpg")    
    
# Developer and Email
st.sidebar.markdown("__Developed by Paul Wunderlich__")
st.sidebar.markdown("__Email: paul.wunderlich@th-owl.de__")
