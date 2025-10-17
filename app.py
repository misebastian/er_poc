import joblib
import streamlit as st
import pandas as pd

# Datos predefinidos de media y desviación estándar
data = {
    'Temp_C': [8.798144, 11.687883],
    'Dew Point Temp_C': [2.555294, 10.883072],
    'Rel Hum_%': [67.431694, 16.918881],
    'Wind Speed_km/h': [14.945469, 8.688696],
    'Visibility_km': [27.664447, 12.622688],
    'Press_kPa': [101.051623, 0.844005]
}
df = pd.DataFrame(data, index=['mean', 'std'])

# Cargar el modelo guardado con joblib
model = joblib.load('naive_bayes_model.pkl')

# Título de la aplicación con un diseño más moderno y tecnológico
st.markdown("""
    <div style="background-color:#0D47A1;padding:10px;border-radius:10px">
        <h1 style='text-align: center; color: #FFFFFF;'>Predicción de Lluvia con Naive Bayes</h1>
        <p style='text-align: center; color: #BBDEFB;'>Universidad del Norte. Maestría en Estadística Aplicada. Machine Learning.</p>
        <p style='text-align: center; color: #BBDEFB;'>Miguel Herrera, Carlos López, Javier de Moya.</p>
        <p style='text-align: center; color: #BBDEFB;'>30 de Agosto de 2024, Barranquilla.</p>
    </div>
""", unsafe_allow_html=True)

st.write("Por favor, introduce los valores a continuación:")

# Crear columnas para una mejor disposición visual
col1, col2 = st.columns(2)

with col1:
    Temp_C = st.number_input('Temperatura (°C)', value=None, format="%.2f")
    Dew_Point_Temp_C = st.number_input('Punto de Rocío (°C)', value=None, format="%.2f")
    Rel_Hum = st.number_input('Humedad Relativa (%)', value=None)
    Wind_Speed_km_h = st.number_input('Velocidad del Viento (km/h)', value=None)
    Visibility_km = st.number_input('Visibilidad (km)', value=None, format="%.2f")

with col2:
    Press_kPa = st.number_input('Presión Atmosférica (kPa)', value=None, format="%.2f")
    Month = st.number_input('Mes', value=1, min_value=1, max_value=12)
    Day = st.number_input('Día', value=1, min_value=1, max_value=31)
    Hour = st.number_input('Hora', value=0, min_value=0, max_value=23)

# Crear un botón para realizar la predicción
if st.button('Realizar Predicción'):
    # Definir los inputs en un DataFrame
    input_data = pd.DataFrame([[Temp_C, Dew_Point_Temp_C, Rel_Hum, Wind_Speed_km_h, Visibility_km, Press_kPa, Month, Day, Hour]],
                              columns=['Temp_C', 'Dew Point Temp_C', 'Rel Hum_%', 'Wind Speed_km/h', 'Visibility_km', 'Press_kPa', 'Month', 'Day', 'Hour'])

    # Reemplazar valores faltantes con las medias predefinidas
    for column in ['Temp_C', 'Dew Point Temp_C', 'Rel Hum_%', 'Wind Speed_km/h', 'Visibility_km', 'Press_kPa']:
        if pd.isna(input_data[column][0]):
            input_data[column] = df.at['mean', column]

    # Estandarizar las columnas numéricas
    input_data[["Temp_C", "Dew Point Temp_C", "Rel Hum_%", "Wind Speed_km/h", "Visibility_km", "Press_kPa"]] = (input_data[["Temp_C", "Dew Point Temp_C", "Rel Hum_%", "Wind Speed_km/h", "Visibility_km", "Press_kPa"]] - df.loc['mean']) / df.loc['std']

    # Realizar la predicción
    prediction = model.predict(input_data)

    # Mostrar el resultado con animaciones
    if prediction[0] == 1:
        st.markdown("""
        <div style='text-align: center;'>
            <h2 style='color: #F44336;'>La predicción es: Sí llueve ☔</h2>
            <div class="cloud">
                <div class="rain"></div>
                <div class="rain"></div>
                <div class="rain"></div>
            </div>
        </div>

        <style>
        .cloud {
            position: relative;
            background: linear-gradient(to bottom, #ECE9E6, #ffffff);
            width: 120px;
            height: 80px;
            margin: 50px auto;
            border-radius: 50px;
            box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
        }

        .cloud:before, .cloud:after {
            content: '';
            position: absolute;
            background: linear-gradient(to bottom, #ECE9E6, #ffffff);
            width: 100px;
            height: 100px;
            border-radius: 50px;
            top: -50px;
            left: 10px;
            box-shadow: 5px 5px 10px rgba(0, 0, 0, 0.1);
        }

        .cloud:after {
            width: 140px;
            height: 140px;
            top: -60px;
            left: -70px;
        }

        .rain {
            position: absolute;
            width: 5px;
            height: 15px;
            background: linear-gradient(to bottom, #00c6ff, #0072ff);
            bottom: -20px;
            left: 50%;
            margin-left: -2.5px;
            border-radius: 50%;
            animation: rain 0.5s infinite linear;
        }

        .rain:nth-child(2) {
            left: 60%;
            animation-delay: 0.3s;
        }

        .rain:nth-child(3) {
            left: 40%;
            animation-delay: 0.6s;
        }

        @keyframes rain {
            0% { transform: translateY(0); }
            100% { transform: translateY(40px); opacity: 0; }
        }
        </style>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style='text-align: center;'>
            <h2 style='color: #2196F3;'>La predicción es: No llueve 🌞</h2>
            <div class="sun">
                <div class="ray_box">
                    <div class="ray"></div>
                    <div class="ray"></div>
                    <div class="ray"></div>
                    <div class="ray"></div>
                    <div class="ray"></div>
                    <div class="ray"></div>
                    <div class="ray"></div>
                    <div class="ray"></div>
                </div>
            </div>
        </div>

        <style>
        .sun {
            position: relative;
            background: #FFEB3B;
            width: 100px;
            height: 100px;
            margin: 50px auto;
            border-radius: 50%;
            box-shadow: 0 0 50px rgba(255, 235, 59, 0.5);
        }

        .ray_box {
            position: absolute;
            top: 50%;
            left: 50%;
            width: 120px;
            height: 120px;
            margin-top: -60px;
            margin-left: -60px;
            animation: spin 3s linear infinite;
        }

        .ray {
            position: absolute;
            background: #FFEB3B;
            width: 10px;
            height: 40px;
            top: 0;
            left: 50%;
            margin-left: -5px;
            border-radius: 20px;
            box-shadow: 0 0 15px rgba(255, 235, 59, 0.5);
        }

        .ray:nth-child(2) {
            transform: rotate(45deg);
        }
        .ray:nth-child(3) {
            transform: rotate(90deg);
        }
        .ray:nth-child(4) {
            transform: rotate(135deg);
        }
        .ray:nth-child(5) {
            transform: rotate(180deg);
        }
        .ray:nth-child(6) {
            transform: rotate(225deg);
        }
        .ray:nth-child(7) {
            transform: rotate(270deg);
        }
        .ray:nth-child(8) {
            transform: rotate(315deg);
        }

        @keyframes spin {
            100% { transform: rotate(360deg); }
        }
        </style>
        """, unsafe_allow_html=True)
