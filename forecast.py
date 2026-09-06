# ============================================================
# PROFESSIONAL THEME
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL APPLICATION BACKGROUND
       ======================================================== */

    .stApp {
        background:
            linear-gradient(
                rgba(3, 12, 25, 0.72),
                rgba(3, 15, 32, 0.82)
            ),
            url("https://images.unsplash.com/photo-1473341304170-971dccb5ac1e?auto=format&fit=crop&w=2400&q=90");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }

    /* Add a subtle overlay for readability */
    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        background:
            radial-gradient(
                circle at top right,
                rgba(0, 153, 255, 0.10),
                transparent 35%
            ),
            radial-gradient(
                circle at bottom left,
                rgba(0, 99, 170, 0.12),
                transparent 35%
            );

        pointer-events: none;
        z-index: 0;
    }

    /* Main content */
    .main {
        position: relative;
        z-index: 1;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 2.5rem;
        padding-right: 2.5rem;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    section[data-testid="stSidebar"] {

        background:
            linear-gradient(
                180deg,
                rgba(3, 16, 34, 0.97),
                rgba(5, 27, 52, 0.97)
            );

        border-right:
            1px solid rgba(80, 180, 255, 0.20);

        box-shadow:
            8px 0 30px rgba(0, 0, 0, 0.30);
    }

    section[data-testid="stSidebar"] * {
        color: #f2f8ff !important;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    section[data-testid="stSidebar"] .stCaption {
        color: #8fb2d6 !important;
    }


    /* ========================================================
       MAIN HEADINGS
       ======================================================== */

    h1 {
        color: #ffffff !important;

        font-size: 2.65rem !important;

        font-weight: 850 !important;

        letter-spacing: -1px;

        line-height: 1.15;

        text-shadow:
            0 3px 16px rgba(0, 0, 0, 0.55);

        margin-bottom: 0.35rem !important;
    }

    h2 {
        color: #f4f9ff !important;

        font-size: 1.65rem !important;

        font-weight: 800 !important;

        letter-spacing: -0.3px;

        margin-top: 1.8rem !important;

        margin-bottom: 0.8rem !important;

        text-shadow:
            0 2px 10px rgba(0, 0, 0, 0.45);
    }

    h3 {
        color: #dff2ff !important;

        font-size: 1.25rem !important;

        font-weight: 750 !important;

        margin-top: 1.2rem !important;

        text-shadow:
            0 2px 8px rgba(0, 0, 0, 0.40);
    }


    /* ========================================================
       NORMAL TEXT
       ======================================================== */

    p,
    li,
    label,
    .stMarkdown {
        color: #d7e7f7;
    }

    .intro-text {

        color: #a9c7e3;

        font-size: 1.05rem;

        line-height: 1.7;

        font-weight: 450;

        margin-bottom: 1.6rem;

        text-shadow:
            0 2px 8px rgba(0, 0, 0, 0.45);
    }


    /* ========================================================
       METRIC CARDS
       ======================================================== */

    div[data-testid="stMetric"] {

        background:
            linear-gradient(
                145deg,
                rgba(13, 46, 82, 0.94),
                rgba(5, 25, 50, 0.96)
            );

        border:
            1px solid rgba(101, 193, 255, 0.28);

        border-radius: 18px;

        padding: 20px 20px 18px 20px;

        min-height: 125px;

        box-shadow:
            0 14px 35px rgba(0, 0, 0, 0.30),
            inset 0 1px 0 rgba(255, 255, 255, 0.05);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {

        transform: translateY(-3px);

        box-shadow:
            0 18px 40px rgba(0, 0, 0, 0.38),
            0 0 20px rgba(0, 153, 255, 0.10);
    }

    div[data-testid="stMetric"] label {

        color: #91b5d7 !important;

        font-size: 0.76rem !important;

        font-weight: 750 !important;

        letter-spacing: 0.8px;

        text-transform: uppercase;
    }

    div[data-testid="stMetricValue"] {

        color: #ffffff !important;

        font-size: 1.85rem !important;

        font-weight: 850 !important;

        letter-spacing: -0.5px;

        text-shadow:
            0 2px 10px rgba(0, 0, 0, 0.35);
    }

    div[data-testid="stMetricDelta"] {

        color: #72d9ff !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       BUTTONS
       ======================================================== */

    .stButton > button,
    .stDownloadButton > button {

        min-height: 48px;

        border-radius: 12px;

        font-size: 0.95rem;

        font-weight: 800;

        letter-spacing: 0.2px;

        color: #ffffff !important;

        background:
            linear-gradient(
                90deg,
                #0098dc,
                #0065d1
            );

        border:
            1px solid rgba(130, 220, 255, 0.35);

        box-shadow:
            0 8px 25px rgba(0, 110, 200, 0.30);

        transition:
            all 0.2s ease;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {

        transform: translateY(-2px);

        background:
            linear-gradient(
                90deg,
                #00a8ee,
                #0074e8
            );

        box-shadow:
            0 12px 30px rgba(0, 130, 230, 0.40);
    }


    /* ========================================================
       SLIDER
       ======================================================== */

    div[data-baseweb="slider"] {
        margin-bottom: 1rem;
    }


    /* Slider text */
    section[data-testid="stSidebar"] [data-testid="stWidgetLabel"] {

        color: #cfe5fa !important;

        font-weight: 700 !important;
    }


    /* ========================================================
       SELECTBOX / INPUTS
       ======================================================== */

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {

        background:
            rgba(10, 36, 65, 0.90) !important;

        border:
            1px solid rgba(110, 190, 245, 0.25) !important;

        border-radius: 11px;

        color: #ffffff !important;
    }

    input {
        color: #ffffff !important;
    }


    /* ========================================================
       EXPANDERS
       ======================================================== */

    .streamlit-expanderHeader {

        background:
            linear-gradient(
                135deg,
                rgba(11, 39, 70, 0.95),
                rgba(7, 27, 51, 0.95)
            );

        border:
            1px solid rgba(105, 187, 245, 0.20);

        border-radius: 12px;

        color: #f2f8ff !important;

        font-weight: 750;

        padding: 0.8rem 1rem;
    }

    .streamlit-expanderContent {

        background:
            rgba(5, 22, 42, 0.88);

        border:
            1px solid rgba(100, 180, 240, 0.12);

        border-top: none;

        border-radius: 0 0 12px 12px;

        color: #d8e9f8 !important;
    }


    /* ========================================================
       DATAFRAME
       ======================================================== */

    div[data-testid="stDataFrame"] {

        border-radius: 15px;

        overflow: hidden;

        border:
            1px solid rgba(110, 190, 245, 0.20);

        box-shadow:
            0 12px 30px rgba(0, 0, 0, 0.25);

        background:
            rgba(5, 22, 42, 0.88);
    }


    /* ========================================================
       CHART CONTAINER
       ======================================================== */

    div[data-testid="stVegaLiteChart"],
    div[data-testid="stArrowVegaLiteChart"],
    div[data-testid="stPlotlyChart"] {

        background:
            linear-gradient(
                145deg,
                rgba(6, 28, 52, 0.90),
                rgba(5, 21, 41, 0.94)
            );

        border:
            1px solid rgba(99, 183, 242, 0.18);

        border-radius: 16px;

        padding: 12px;

        box-shadow:
            0 12px 28px rgba(0, 0, 0, 0.24);
    }


    /* ========================================================
       ALERT / INFO BOXES
       ======================================================== */

    div[data-testid="stAlert"] {

        border-radius: 12px;

        background:
            rgba(8, 31, 57, 0.92);

        border:
            1px solid rgba(106, 190, 245, 0.18);
    }


    /* ========================================================
       DIVIDERS
       ======================================================== */

    hr {

        border: none;

        height: 1px;

        background:
            linear-gradient(
                90deg,
                transparent,
                rgba(115, 190, 245, 0.30),
                transparent
            );

        margin: 1.4rem 0;
    }


    /* ========================================================
       SIDEBAR TEXT
       ======================================================== */

    section[data-testid="stSidebar"] p {

        color: #b9d0e7 !important;

        line-height: 1.55;
    }

    section[data-testid="stSidebar"] strong {

        color: #ffffff !important;

        font-weight: 800 !important;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer-text {

        color: #7595b5;

        text-align: center;

        font-size: 0.78rem;

        padding: 2rem 0 0.5rem 0;

        letter-spacing: 0.3px;
    }


    /* ========================================================
       RESPONSIVE DESIGN
       ======================================================== */

    @media (max-width: 900px) {

        .block-container {

            padding-left: 1rem;

            padding-right: 1rem;
        }

        h1 {

            font-size: 2rem !important;
        }

        h2 {

            font-size: 1.45rem !important;
        }

        div[data-testid="stMetric"] {

            min-height: 105px;

            padding: 15px;
        }

        div[data-testid="stMetricValue"] {

            font-size: 1.45rem !important;
        }
    }

    </style>
    """,
    unsafe_allow_html=True,
)
