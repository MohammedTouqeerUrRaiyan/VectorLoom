import streamlit as st
import requests


# ============================================================
# CONFIG
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000/api/v1"


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="VectorLoom",
    page_icon="🔷",
    layout="wide",
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        font-size: 18px;
        color: #777;
        margin-bottom: 30px;
    }

    .card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #ddd;
        margin-bottom: 15px;
        background-color: #fafafa;
    }

    .score {
        font-weight: 600;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🔷 VectorLoom</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "AI-Powered RAG & Hybrid Recommendation Platform"
    "</div>",
    unsafe_allow_html=True,
)


# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("VectorLoom")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Dashboard",
        "💬 AI Chat",
        "🛍️ Recommendations",
        "📚 Documents",
    ],
)


# ============================================================
# HEALTH CHECK
# ============================================================

def check_api():

    try:

        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=5,
        )

        return response.status_code == 200

    except requests.RequestException:

        return False


api_online = check_api()


if api_online:

    st.sidebar.success("API Online")

else:

    st.sidebar.error("API Offline")


# ============================================================
# DASHBOARD
# ============================================================

if page == "🏠 Dashboard":

    st.header("System Overview")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "API Status",
            "Online" if api_online else "Offline",
        )

    with col2:

        st.metric(
            "Platform",
            "VectorLoom",
        )

    with col3:

        st.metric(
            "Architecture",
            "RAG + Hybrid ML",
        )

    st.divider()

    st.subheader("Capabilities")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            ### 💬 Retrieval-Augmented Generation

            VectorLoom can answer questions using
            indexed documents rather than relying only
            on the language model.

            **Pipeline**

            Query → Retrieval → Hybrid Search →
            Reranking → Prompt → LLM → Citations
            """
        )

    with col2:

        st.markdown(
            """
            ### 🛍️ Hybrid Recommendation Engine

            VectorLoom combines:

            - Collaborative filtering
            - Content-based recommendations
            - Hybrid scoring

            to produce personalized product recommendations.
            """
        )

    st.divider()

    st.info(
        "Use the sidebar to test AI Chat, "
        "Recommendations and indexed Documents."
    )


# ============================================================
# AI CHAT
# ============================================================

elif page == "💬 AI Chat":

    st.header("💬 VectorLoom AI Chat")

    st.write(
        "Ask questions about the documents indexed in VectorLoom."
    )

    if "session_id" not in st.session_state:

        st.session_state.session_id = "streamlit-session"

    question = st.text_area(
        "Your question",
        placeholder="Example: What is a Salesforce trigger?",
        height=120,
    )

    if st.button(
        "Ask VectorLoom",
        type="primary",
    ):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            with st.spinner(
                "Retrieving documents and generating answer..."
            ):

                try:

                    response = requests.post(
                        f"{API_BASE_URL}/chat/chat",
                        json={
                            "question": question,
                            "session_id": st.session_state.session_id,
                        },
                        timeout=120,
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.subheader("Answer")

                        st.write(
                            data.get(
                                "answer",
                                "No answer returned.",
                            )
                        )

                        sources = data.get(
                            "sources",
                            [],
                        )

                        if sources:

                            st.subheader("Sources")

                            for source in sources:

                                st.markdown(
                                    f"- 📄 `{source}`"
                                )

                    else:

                        st.error(
                            f"API Error: {response.status_code}"
                        )

                        st.code(response.text)

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to VectorLoom API: {e}"
                    )


# ============================================================
# RECOMMENDATIONS
# ============================================================

elif page == "🛍️ Recommendations":

    st.header("🛍️ Product Recommendations")

    st.write(
        "Generate personalized recommendations "
        "using VectorLoom's hybrid recommendation engine."
    )

    customer_id = st.text_input(
        "Customer ID",
        value="75c54a755b8a467e53e0e4a01833deb029734feb22ad25438137925123a38f8b",
    )

    limit = st.slider(
        "Number of recommendations",
        min_value=1,
        max_value=20,
        value=5,
    )

    if st.button(
        "Get Recommendations",
        type="primary",
    ):

        if not customer_id.strip():

            st.warning("Please enter a customer ID.")

        else:

            with st.spinner(
                "Generating recommendations..."
            ):

                try:

                    response = requests.get(
                        f"{API_BASE_URL}/recommendations/"
                        f"{customer_id}",
                        params={
                            "limit": limit,
                        },
                        timeout=30,
                    )

                    if response.status_code == 200:

                        data = response.json()

                        st.success(
                            f"Found {data['count']} recommendations."
                        )

                        recommendations = data.get(
                            "recommendations",
                            [],
                        )

                        for index, item in enumerate(
                            recommendations,
                            start=1,
                        ):

                            st.markdown(
                                f"""
                                <div class="card">

                                <h3>
                                #{index} — {item.get("product_name", "Product")}
                                </h3>

                                <b>Article ID:</b>
                                {item.get("article_id", "N/A")}

                                <br><br>

                                <b>Type:</b>
                                {item.get("product_type", "N/A")}

                                <br>

                                <b>Category:</b>
                                {item.get("product_group", "N/A")}

                                <br>

                                <b>Colour:</b>
                                {item.get("colour", "N/A")}

                                <br>

                                <b>Department:</b>
                                {item.get("department", "N/A")}

                                <br><br>

                                <span class="score">
                                Hybrid Score:
                                {item.get("score", 0):.4f}
                                </span>

                                <br>

                                Collaborative Score:
                                {item.get("collaborative_score", 0):.4f}

                                <br>

                                Content Score:
                                {item.get("content_score", 0):.4f}

                                <br><br>

                                <b>Reason:</b>
                                {item.get("reason", "N/A")}

                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                    elif response.status_code == 404:

                        st.warning(
                            "No recommendations found for this customer."
                        )

                    else:

                        st.error(
                            f"API Error: {response.status_code}"
                        )

                        st.code(response.text)

                except requests.RequestException as e:

                    st.error(
                        f"Could not connect to VectorLoom API: {e}"
                    )


# ============================================================
# DOCUMENTS
# ============================================================

elif page == "📚 Documents":

    st.header("📚 Indexed Documents")

    st.write(
        "Documents currently available in VectorLoom's "
        "retrieval system."
    )

    try:

        response = requests.get(
            f"{API_BASE_URL}/documents/",
            timeout=15,
        )

        if response.status_code == 200:

            documents = response.json()

            st.success(
                f"{len(documents)} documents indexed."
            )

            for document in documents:

                with st.container():

                    col1, col2, col3 = st.columns(
                        [4, 1, 1]
                    )

                    with col1:

                        st.markdown(
                            f"### 📄 {document['name']}"
                        )

                    with col2:

                        st.metric(
                            "Pages",
                            document["pages"],
                        )

                    with col3:

                        st.metric(
                            "Chunks",
                            document["chunks"],
                        )

                    st.divider()

        else:

            st.error(
                f"API Error: {response.status_code}"
            )

    except requests.RequestException as e:

        st.error(
            f"Could not connect to VectorLoom API: {e}"
        )