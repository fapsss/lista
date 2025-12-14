import streamlit as st
import os

# Definicja ścieżki do pliku
PLIK_MAGAZYNU = "magazyn.txt"

def zaladuj_magazyn():
    """Wczytuje towary z pliku tekstowego do listy."""
    if os.path.exists(PLIK_MAGAZYNU):
        with open(PLIK_MAGAZYNU, 'r') as f:
            # Wczytujemy każdą linię i usuwamy znaki nowej linii
            return [linia.strip() for linia in f.readlines() if linia.strip()]
    return []

def zapisz_magazyn(lista_towarow):
    """Zapisuje listę towarów do pliku tekstowego, każda pozycja w nowej linii."""
    with open(PLIK_MAGAZYNU, 'w') as f:
        for towar in lista_towarow:
            f.write(towar + '\n')

def dodaj_towar(nazwa):
    """Dodaje towar do listy i zapisuje do pliku."""
    if nazwa:
        # 1. Wczytaj aktualny stan
        magazyn = zaladuj_magazyn()
        
        # 2. Dodaj nowy element
        magazyn.append(nazwa.strip())
        
        # 3. Zapisz zaktualizowany stan
        zapisz_magazyn(magazyn)
        st.success(f"Dodano towar: '{nazwa}'")

def usun_towar(nazwa):
    """Usuwa pierwsze wystąpienie towaru i zapisuje do pliku."""
    magazyn = zaladuj_magazyn()
    try:
        # Usuń z listy
        magazyn.remove(nazwa)
        # Zapisz zaktualizowany stan
        zapisz_magazyn(magazyn)
        st.warning(f"Usunięto towar: '{nazwa}'")
    except ValueError:
        st.error(f"Błąd: Towar '{nazwa}' nie został znaleziony w magazynie.")


# --- INTERFEJS UŻYTKOWNIKA STREAMLIT ---

st.set_page_config(page_title="Magazyn Zapisujący do Pliku", layout="wide")

st.title("💾 System Magazynowy (Zapis Plikowy)")
st.subheader("Używa pliku magazyn.txt do trwałego przechowywania danych")

# --- SEKCJA DODAWANIA TOWARU ---
st.header("➕ Dodaj nowy towar")
with st.form(key='dodaj_form'):
    nowy_towar = st.text_input("Nazwa towaru", key='input_dodaj')
    dodaj_button = st.form_submit_button("Dodaj do Magazynu")

    if dodaj_button:
        dodaj_towar(nowy_towar)


# --- SEKCJA STANU MAGAZYNU I USUWANIA ---
st.header("📋 Aktualny stan magazynu")

# Wczytanie aktualnego stanu magazynu (odświeżane przy każdej interakcji)
aktualny_magazyn = zaladuj_magazyn()

if aktualny_magazyn:
    st.code(aktualny_magazyn)
    st.info(f"Całkowita liczba towarów: **{len(aktualny_magazyn)}**")
    
    unikalne = sorted(list(set(aktualny_magazyn)))
    
    st.markdown("##### Usuwanie pozycji")
    
   

# Wybór towaru do usunięcia
    towar_do_usuniecia = st.selectbox(
        "Wybierz towar do usunięcia",
        options=unikalne,
        key='select_usun'
    )

    usun_button = st.button("Usuń wybrane (jedno wystąpienie)")

    if usun_button and towar_do_usuniecia:
        usun_towar(towar_do_usuniecia)
    
    # 🚨 Zmiana na nowszą i zalecaną funkcję:
        st.rerun()
        
else:
     st.warning("Magazyn jest pusty. Dodaj pierwszy towar.")
        
