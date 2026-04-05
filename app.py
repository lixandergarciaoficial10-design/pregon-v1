import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection
import time

elif menu == "Radar":
            st.title("📡 Radar de Competencia")
            
            with st.expander("➕ Agregar Cuenta al Radar"):
                cuenta = st.text_input("Usuario de Instagram (ej: tienda_rd):").replace("@", "").strip()
                if st.button("Guardar en Radar"):
                    if cuenta:
                        supabase.table("radar_config").insert({
                            "owner_id": user_id, 
                            "cuenta_instagram": cuenta, 
                            "esta_activo": True
                        }).execute()
                        st.success(f"✅ Vigilando a @{cuenta}")
                        st.rerun()

            st.divider()

            st.subheader("🔄 Sincronización")
            if st.button("🚀 ESCANEAR TODAS LAS CUENTAS AHORA"):
                with st.spinner("El Vigilante está barriendo Instagram..."):
                    # IMPORTAMOS TUS FUNCIONES DE VIGILANTE.PY
                    from vigilante import espiar_instagram, limpiar_y_calificar
                    
                    # 1. Buscamos qué cuentas tienes configuradas
                    mis_cuentas = supabase.table("radar_config").select("*").eq("owner_id", user_id).execute().data
                    
                    total_nuevos = 0
                    if mis_cuentas:
                        for fila in mis_cuentas:
                            target = fila.get('cuenta_instagram')
                            
                            # 2. Ejecutamos el scraper (Instagrapi en la nube)
                            datos_crudos = espiar_instagram(target)
                            
                            # 3. Calificamos los comentarios
                            leads_calificados = limpiar_y_calificar(datos_crudos, "Instagram")
                            
                            # 4. GUARDAR EN LA BASE DE DATOS (Esto es lo que faltaba)
                            for lead in leads_calificados:
                                try:
                                    supabase.table("leads").insert({
                                        "owner_id": user_id,
                                        "usuario_ig": lead['usuario_ig'],
                                        "comentario": lead['comentario'],
                                        "score_ia": lead['score_ia'],
                                        "producto_interes": lead.get('vehiculo_interes', 'General'),
                                        "fuente": "Instagram"
                                    }).execute()
                                    total_nuevos += 1
                                except:
                                    # Si el lead ya existe, Supabase dará error y lo saltamos (evita duplicados)
                                    pass
                    
                    if total_nuevos > 0:
                        st.success(f"¡Éxito! Encontramos {total_nuevos} leads nuevos.")
                        st.balloons()
                        time.sleep(2)
                        st.rerun() # Refresca para que aparezcan en el Dashboard
                    else:
                        st.warning("No se encontraron comentarios con intención de compra en este momento.")

            st.subheader("👀 Cuentas bajo vigilancia")
            radar_view = supabase.table("radar_config").select("*").eq("owner_id", user_id).execute().data
            if radar_view:
                for r in radar_view:
                    st.write(f"✅ Instagram: **@{r.get('cuenta_instagram')}**")
            else:
                st.info("Aún no tienes cuentas en el Radar.")
