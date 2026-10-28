import streamlit as st

st.set_page_config(page_title="Cajero UNAL", page_icon="🏦", layout="centered")

if "menu_activo" not in st.session_state:
    st.session_state["menu_activo"] = "Inicio"

with open("estado.csv", "a") as f:
    pass  

estado = {}
with open("estado.csv", "r") as f:
    for linea in f:
        partes = linea.strip().split(",")
        if len(partes) == 2:
            clave = partes[0]
            estado[clave] = int(partes[1])

valores_defecto = {
    "saldo": 500000,
    "total_consignado": 0,
    "num_consignaciones": 0,
    "total_retirado": 0,
    "num_retiros": 0,
    "meta_ahorro": 0  
}

for clave, valor in valores_defecto.items():
    if clave not in estado:
        estado[clave] = valor

def guardar_estado(diccionario_estado):
    with open("estado.csv", "w") as f:
        for clave, valor in diccionario_estado.items():
            f.write(f"{clave},{str(valor)}\n")

st.title("🏦 Bienvenido al Cajero UNAL")
st.caption("Examen Final - Panel de Gestión Bancaria interactivo.")
st.markdown("---")

with st.container(border=True):
    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(label="💰 Su saldo actual", value=f"${estado['saldo']:,}")
    with col_s2:
        meta_actual = estado["meta_ahorro"]
        if meta_actual > 0:
            porcentaje = (estado["saldo"] / meta_actual) * 100
            st.metric(label="🎯 Meta de Ahorro", value=f"${meta_actual:,}", delta=f"{porcentaje:.1f}% alcanzado")
        else:
            st.metric(label="🎯 Meta de Ahorro", value="Sin definir")

st.write("")

lista_opciones = ["Inicio", "Consignar", "Retirar", "Simular ahorro", "Metas de ahorro", "Ver estadísticas"]

def cambiar_menu():
    st.session_state["menu_activo"] = st.session_state["menu_cajero"]

indice_actual = lista_opciones.index(st.session_state["menu_activo"])

st.sidebar.header("Navigation")
opcion = st.sidebar.selectbox(
    "Elija una operación:",
    lista_opciones,
    index=indice_actual,
    key="menu_cajero",
    on_change=cambiar_menu
)

with st.container(border=True):
    if st.session_state["menu_activo"] == "Inicio":
        st.subheader("👋 Panel de Bienvenida")
        st.info("Seleccione una operación en el menú de la izquierda para comenzar a gestionar sus productos.")
        
    elif st.session_state["menu_activo"] == "Consignar":
        st.subheader("📥 Realizar Consignación")
        consignar_monto = st.number_input("Monto a consignar:", min_value=0, step=10000, value=None)
        
        if st.button("Confirmar Consignación", type="primary", use_container_width=True):
            if consignar_monto is None or consignar_monto <= 0:
                st.error("Monto inválido. No se puede consignar ese valor.")
            else:
                estado["saldo"] += consignar_monto
                estado["total_consignado"] += consignar_monto
                estado["num_consignaciones"] += 1
                guardar_estado(estado)
                st.session_state["menu_activo"] = "Inicio"
                st.rerun()

    elif st.session_state["menu_activo"] == "Retirar":
        st.subheader("📤 Realizar Retiro")
        retirar_monto = st.number_input("Monto a retirar:", min_value=0, step=10000, value=None)
        
        if st.button("Confirmar Retiro", type="primary", use_container_width=True):
            if retirar_monto is None or retirar_monto <= 0:
                st.error("Monto inválido. No se puede retirar ese valor.")
            elif retirar_monto % 10000 != 0:
                st.error("El monto debe ser múltiplo de $10,000")
            elif retirar_monto > estado["saldo"]:
                st.error(f"Fondos insuficientes. Su saldo actual es de ${estado['saldo']:,}")
            else:
                estado["saldo"] -= retirar_monto
                estado["total_retirado"] += retirar_monto
                estado["num_retiros"] += 1
                guardar_estado(estado)
                st.session_state["menu_activo"] = "Inicio"
                st.rerun()

    elif st.session_state["menu_activo"] == "Simular ahorro":
        st.subheader("📊 Simulación de Ahorro Proyectado")
        ahorro = st.number_input("¿Cuánto va a ahorrar cada mes?", min_value=0, step=5000, value=None)
        meses = st.number_input("¿Por cuántos meses quiere simular?", min_value=1, max_value=120, step=1, value=None)
        
        if st.button("Calcular Proyección", type="primary", use_container_width=True):
            if ahorro is None or ahorro <= 0:
                st.error("El ahorro mensual debe ser mayor a $0")
            elif meses is None or meses <= 0:
                st.error("La cantidad de meses debe ser mayor a 0")
            else:
                saldo_simulado = estado["saldo"]
                st.write("### Tabla de proyección mensual:")
                for i in range(meses):
                    saldo_simulado += ahorro
                    st.write(f"**Mes {i+1}:** ${saldo_simulado:,}")
                st.success(f"En {meses} meses tendría un total de **${saldo_simulado:,}** (Nota: No modifica su saldo real)")

    elif st.session_state["menu_activo"] == "Metas de ahorro":
        st.subheader("🎯 Definir Meta de Ahorro")
        nueva_meta = st.number_input("Establezca o cambie su meta de ahorro total:", min_value=0, step=50000, value=None if estado["meta_ahorro"] == 0 else estado["meta_ahorro"])
        
        if st.button("Guardar Meta", type="primary", use_container_width=True):
            if nueva_meta is None or nueva_meta <= 0:
                st.error("Por favor ingrese un valor válido y mayor a $0 para la meta.")
            else:
                estado["meta_ahorro"] = nueva_meta
                guardar_estado(estado)
                st.session_state["menu_activo"] = "Inicio"
                st.rerun()
            
        st.markdown("---")
        st.write("### Progreso Actual")
        
        saldo_actual = estado["saldo"]
        
        if meta_actual == 0:
            st.warning("Aún no has fijado una meta de ahorro válida (o es $0).")
        else:
            st.write(f"**Meta fijada:** ${meta_actual:,}")
            st.write(f"**Saldo que aporta:** ${saldo_actual:,}")
            
            if saldo_actual >= meta_actual:
                st.balloons() 
                st.success("🎉 ¡Felicitaciones! Has alcanzado o superado tu meta de ahorro establecida.")
                st.progress(1.0) 
                st.write("**Porcentaje alcanzado:** 100%")
            else:
                porcentaje = saldo_actual / meta_actual
                falta_dinero = meta_actual - saldo_actual
                
                st.write(f"Te faltan **${falta_dinero:,}** para cumplir tu objetivo.")
                st.write(f"**Porcentaje alcanzado:** {porcentaje * 100:.1f}%")
                st.progress(porcentaje) 

    elif st.session_state["menu_activo"] == "Ver estadísticas":
        st.subheader("📈 Estadísticas Generales de la Cuenta")
        
        col1, col2 = st.columns(2)
        with col1:
            with st.container(border=True):
                st.markdown("### 📥 Historial de Ingresos")
                st.write(f"**Total consignado:** ${estado['total_consignado']:,}")
                st.write(f"**Número de consignaciones:** {estado['num_consignaciones']}")
                promedio_con = estado["total_consignado"] / estado["num_consignaciones"] if estado["num_consignaciones"] > 0 else 0
                st.write(f"**Promedio por consignación:** ${promedio_con:,.0f}")
            
        with col2:
            with st.container(border=True):
                st.markdown("### 📤 Historial de Egresos")
                st.write(f"**Total retirado:** ${estado['total_retirado']:,}")
                st.write(f"**Número de retiros:** {estado['num_retiros']}")
                promedio_ret = estado["total_retirado"] / estado["num_retiros"] if estado["num_retiros"] > 0 else 0
                st.write(f"**Promedio por retiro:** ${promedio_ret:,.0f}")