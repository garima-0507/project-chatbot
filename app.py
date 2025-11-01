import streamlit as st
from analysis import top_n_crops, compare_crops, compare_rainfall, top_bottom_rainfall
from fuzzywuzzy import process
import re
import plotly.express as px

# 🌿 Streamlit Page Setup
st.set_page_config(page_title="AgroSense - Smart Agri Chatbot", layout="centered")

st.title("🌾 AgroSense – Smart Agri Chatbot")
st.markdown("##### Ask questions about India's crop 🌱 and rainfall ☔ data (powered by Project Samarth).")

# 💬 Chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "bot", "content": "👋 Hi! I'm **AgroSense** — your Agri & Climate Data Assistant. How can I help you today?"}
    ]

# Display chat messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# Chat input
user_input = st.chat_input("Type your question here...")

if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    query = user_input.lower().strip()
    response = ""

    # -------------------- QUERY HANDLING --------------------
    # 1️⃣ Top crops
    if "top" in query and "crop" in query:
        m = re.search(r'\d+', query)
        n = int(m.group()) if m else 5
        df = top_n_crops(n)
        response = f"Here are the **Top {n} crops in India (National Totals)**:"
        with st.chat_message("assistant"):
            st.write(response)
            st.dataframe(df)
            fig = px.bar(df, x="crop", y="production (million tonnes)",
                         color="crop", title=f"Top {n} Crops by Production",
                         text="production (million tonnes)")
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Source: data.gov.in – Ministry of Agriculture")

    # 2️⃣ Compare crops
    elif "compare" in query and "crop" in query:
        match = re.findall(r"between\s+([a-z\s]+)\s+and\s+([a-z\s]+)", query)
        if match:
            crop1, crop2 = match[0][0].strip(), match[0][1].strip()
            df, prov = compare_crops(crop1, crop2)
            response = f"📊 Comparing crop production between **{crop1.title()}** and **{crop2.title()}**:"
            with st.chat_message("assistant"):
                st.write(response)
                st.dataframe(df)
                fig = px.bar(df, x="Crop ", y="Production (Million tonnes)",
                             color="Crop ", text="Production (Million tonnes)",
                             title=f"{crop1.title()} vs {crop2.title()} Production")
                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"Source: {prov['file']}")
        else:
            st.chat_message("assistant").write("Please ask like: *Compare crop between Rice and Wheat*")

    # 3️⃣ Compare rainfall
    elif "compare" in query and "rainfall" in query:
        match = re.findall(r"between\s+([a-z\s]+)\s+and\s+([a-z\s]+)", query)
        if match:
            d1, d2 = match[0][0].strip(), match[0][1].strip()
            df, prov = compare_rainfall(d1, d2)
            response = f"🌧️ Comparing rainfall between **{d1.title()}** and **{d2.title()}**:"
            with st.chat_message("assistant"):
                st.write(response)
                st.dataframe(df)
                fig = px.bar(df, x="District", y="Actual_Rainfall",
                             color="District", text="Actual_Rainfall",
                             title=f"Rainfall Comparison: {d1.title()} vs {d2.title()} (mm)")
                st.plotly_chart(fig, use_container_width=True)
                st.caption(f"Source: {prov['file']}")
        else:
            st.chat_message("assistant").write("Please ask like: *Compare rainfall between Chennai and Tiruvallur*")

    # 4️⃣ Highest rainfall
    elif "highest" in query and "rainfall" in query:
        top, bottom, prov = top_bottom_rainfall(1)
        response = "🌧️ District with **Highest Rainfall**:"
        with st.chat_message("assistant"):
            st.write(response)
            st.dataframe(top)
            fig = px.bar(top, x="District", y="Actual_Rainfall",
                         text="Actual_Rainfall", color="District",
                         title="Highest Rainfall District (mm)")
            st.plotly_chart(fig, use_container_width=True)
            st.caption(f"Source: {prov['file']}")

    # 5️⃣ Lowest rainfall
    elif "lowest" in query and "rainfall" in query:
        top, bottom, prov = top_bottom_rainfall(1)
        response = "☀️ District with **Lowest Rainfall**:"
        with st.chat_message("assistant"):
            st.write(response)
            st.dataframe(bottom)
            fig = px.bar(bottom, x="District", y="Actual_Rainfall",
                         text="Actual_Rainfall", color="District",
                         title="Lowest Rainfall District (mm)")
            st.plotly_chart(fig, use_container_width=True)
            st.caption(f"Source: {prov['file']}")

    else:
        response = "🤖 Sorry, AgroSense can currently answer about top crops or rainfall comparisons. More insights coming soon!"
        st.chat_message("assistant").write(response)

    st.session_state["messages"].append({"role": "bot", "content": response})
