import streamlit as st
import string
import secrets
import math

# PASSWORD CREATING
def generate_password(length, use_upper=True, use_lower=True, use_digits=True, use_symbols=True):
    alphabet = ''
    if use_upper:
        alphabet += string.ascii_uppercase
    if use_lower:
        alphabet += string.ascii_lowercase
    if use_digits:
        alphabet += string.digits
    if use_symbols:
        alphabet += string.punctuation

    if not alphabet:
        return 'No character set selected'

    password = ''.join(secrets.choice(alphabet) for _ in range(length))
    return password

# ENTROPY CALCULATING
def calculate_entropy(length, alphabet_size):
    return round(length * math.log2(alphabet_size), 2)

# ENTROPY CATEGORING
def entropy_to_category(e):
    if e < 40:
        return "Zayıf"
    if e < 60:
        return "Orta"
    if e < 80:
        return "Güçlü"
    return "Çok güçlü"

# ENTROPY INFORMATION
def entropy_info(e):
    if e == "Zayıf":
        st.warning("Şifre Zayıf")
    if e == "Orta":
        st.info("Şifre Orta")
    if e == "Güçlü":
        st.success("Şifre Güçlü")
    if e == "Çok güçlü":
        st.success("Şifre Çok Güçlü")

# PAGE CONFIGS
st.set_page_config(
    page_title="SPG",
    page_icon=":streamlit:",
    initial_sidebar_state="expanded",
    layout="centered"
)

# PAGE DETAILS
st.title("SPG")
st.write("Güçlü, rastgele ve güvenli parolalarınızı saniyeler içinde oluşturun.")

st.sidebar.header("Ayarlar")
length = st.sidebar.slider("Şifre uzunluğu", 4, 64, 12)
use_upper = st.sidebar.checkbox("Büyük harf (A-Z)", True)
use_lower = st.sidebar.checkbox("Küçük harf (a-z)", True)
use_digits = st.sidebar.checkbox("Rakamlar (0-9)", True)
use_symbols = st.sidebar.checkbox("Semboller (!@#...)", True)

# PASSWORD AND ENTROPY
if "password" not in st.session_state:
    st.session_state.password = ""
    
if "entropy" not in st.session_state:
    st.session_state.entropy = None

if st.button("Şifre Üret"):
    if not any([use_upper, use_lower, use_digits, use_symbols]):
        st.error("En az bir karakter tipi seçmelisin")
    else:
        pwd = generate_password(length, use_upper, use_lower, use_digits, use_symbols)
        st.session_state.password = pwd
        
        alphabet = ""
        if use_upper: alphabet += string.ascii_uppercase
        if use_lower: alphabet += string.ascii_lowercase
        if use_digits: alphabet += string.digits
        if use_symbols: alphabet += string.punctuation
        
        ent = calculate_entropy(len(pwd), len(alphabet))
        st.session_state.entropy = entropy_to_category(ent)

        if st.session_state.password:
            st.code(st.session_state.password, language='text')
            entropy_info(st.session_state.entropy)

