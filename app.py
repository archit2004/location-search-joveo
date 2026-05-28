
import streamlit as st
from predict import search_location


st.set_page_config(page_title="Location Search", page_icon="📍", layout="centered")

st.title("Location Search")
st.caption("Search by city, state or pincode across India")

query = st.text_input("", placeholder="City, state, zip code", label_visibility="collapsed")

if query:
    results = search_location(query)
    
    if len(results) == 0:
        st.warning("No results found")
    else:
        names = [r['entity_name'] for r in results]
        selected = st.selectbox("Select location", names)
        
        selected_result = results[names.index(selected)]
        
        
        st.subheader(f" {selected_result['entity_name']}")
        st.caption(f"Type: `{selected_result['entity_type']}`")
        
        st.metric("Latitude", selected_result['latitude'])
        
        st.metric("Longitude", selected_result['longitude'])
        
        if 'normalized' in selected_result:
            st.divider()
            st.markdown("**Details**")
            norm = selected_result['normalized']
            
            col1, col2 = st.columns(2)
            with col1:
                if norm.get('city'):
                    st.markdown(f"**City:** {norm['city']}")
                if norm.get('state'):
                    st.markdown(f"**State:** {norm['state']}")
            with col2:
                if norm.get('pincode'):
                    st.markdown(f"**Pincode:** {norm['pincode']}")
                if norm.get('geoId') and norm['geoId'] != 'None':
                    st.markdown(f"**Geo ID:** {norm['geoId']}")