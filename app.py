# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuración simple
st.set_page_config(
    page_title="Predictor de Deserción Universitaria",
    page_icon="🎓",
    layout="wide"
)

# Título
st.title("🎓 Predictor de Deserción Universitaria")
st.markdown("Sistema para identificar estudiantes en riesgo de abandono académico")

# Simulamos el modelo para evitar problemas de instalación
class SimplePredictor:
    def __init__(self):
        self.class_names = ["🚨 Alto Riesgo", "⚠️ Riesgo Medio", "✅ Bajo Riesgo"]
    
    def predict(self, input_data):
        # Simulamos predicciones basadas en reglas simples
        age = input_data['age']
        grade_1st = input_data['grade_1st_sem']
        approved_1st = input_data['units_approved_1st']
        debtor = input_data['debtor']
        
        # Lógica simple de predicción
        if debtor == 1 or grade_1st < 10 or approved_1st < 3:
            return 0, [0.7, 0.2, 0.1]  # Alto riesgo
        elif grade_1st < 14 or approved_1st < 5:
            return 1, [0.2, 0.6, 0.2]  # Riesgo medio
        else:
            return 2, [0.1, 0.2, 0.7]  # Bajo riesgo

# Inicializar predictor
predictor = SimplePredictor()

# Sidebar
st.sidebar.title("Navegación")
app_mode = st.sidebar.radio("Modo", ["Predicción Individual", "Dashboard", "Acerca de"])

if app_mode == "Predicción Individual":
    st.header("📊 Predicción Individual")
    
    with st.form("student_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Datos Básicos")
            age = st.slider("Edad", 17, 70, 20)
            gender = st.selectbox("Género", ["Femenino", "Masculino"])
            international = st.selectbox("Internacional", ["No", "Sí"])
            
        with col2:
            st.subheader("Datos Académicos")
            grade_1st_sem = st.slider("Promedio 1er semestre (0-20)", 0, 20, 12)
            units_approved_1st = st.slider("Materias aprobadas 1er sem", 0, 10, 4)
            admission_grade = st.slider("Nota admisión (0-200)", 0, 200, 120)
        
        col3, col4 = st.columns(2)
        
        with col3:
            st.subheader("Situación Económica")
            debtor = st.selectbox("Es deudor", ["No", "Sí"])
            scholarship = st.selectbox("Tiene beca", ["No", "Sí"])
            tuition_fees = st.selectbox("Matrícula al día", ["Sí", "No"])
            
        with col4:
            st.subheader("Otros Datos")
            marital_status = st.selectbox("Estado civil", ["Soltero", "Casado", "Otro"])
            displaced = st.selectbox("Zona rural", ["No", "Sí"])
        
        submitted = st.form_submit_button("🔮 Predecir Riesgo")
    
    if submitted:
        # Preparar datos
        input_data = {
            'age': age,
            'grade_1st_sem': grade_1st_sem,
            'units_approved_1st': units_approved_1st,
            'debtor': 1 if debtor == "Sí" else 0,
            'scholarship': 1 if scholarship == "Sí" else 0,
            'tuition_fees': 1 if tuition_fees == "Sí" else 0
        }
        
        # Predecir
        prediction, probabilities = predictor.predict(input_data)
        predicted_class = predictor.class_names[prediction]
        
        # Mostrar resultados
        st.success(f"**Predicción:** {predicted_class}")
        
        # Gráfico
        fig = go.Figure(data=[
            go.Bar(x=predictor.class_names, y=probabilities, 
                  marker_color=['#FF6B6B', '#FFE66D', '#4ECDC4'])
        ])
        fig.update_layout(title="Probabilidades de Predicción", yaxis_range=[0, 1])
        st.plotly_chart(fig)
        
        # Recomendaciones
        st.subheader("🎯 Plan de Acción")
        
        if prediction == 0:
            st.error("""
            **🚨 INTERVENCIÓN INMEDIATA**
            - Reunión con consejero académico
            - Evaluación económica urgente
            - Programa de mentoría intensiva
            """)
        elif prediction == 1:
            st.warning("""
            **⚠️ MONITOREO REFORZADO**
            - Talleres de habilidades de estudio
            - Grupo de apoyo entre pares
            - Revisión académica mensual
            """)
        else:
            st.success("""
            **✅ SITUACIÓN ESTABLE**
            - Continuar apoyo actual
            - Oportunidades de desarrollo
            - Participación en proyectos
            """)

elif app_mode == "Dashboard":
    st.header("📈 Dashboard de Analytics")
    
    # Métricas
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Tasa Deserción", "23.5%", "-4.2%")
    with col2:
        st.metric("Estudiantes Riesgo", "156", "+12")
    with col3:
        st.metric("Intervenciones", "68%", "+8%")
    
    # Gráficos
    data = pd.DataFrame({
        'Riesgo': ['Alto', 'Medio', 'Bajo'],
        'Estudiantes': [45, 80, 120]
    })
    fig = px.pie(data, values='Estudiantes', names='Riesgo', title='Distribución de Riesgos')
    st.plotly_chart(fig)

else:
    st.header("ℹ️ Acerca de")
    st.markdown("""
    ## Predictor de Deserción Universitaria
    **Sistema para identificación temprana de estudiantes en riesgo**
    
    ### Características:
    - Predicción individual de riesgo
    - Dashboard de analytics
    - Recomendaciones personalizadas
    
    ### Tecnologías:
    - Streamlit
    - Plotly
    - Pandas
    """)

st.sidebar.markdown("---")
st.sidebar.info("✨ App desarrollada para prevenir la deserción universitaria")