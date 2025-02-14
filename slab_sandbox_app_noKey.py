import streamlit as st
import pandas as pd
import openai

st.set_page_config(layout="wide")

if "df_slab" not in st.session_state:
    file_path = "SLAB_Data.xlsx"
    df_slab = pd.read_excel(file_path)

    # Clean and standardize the data
    df_slab["Year"] = df_slab["Year"].astype(str).str.replace(".0", "", regex=False)
    df_slab = df_slab.applymap(lambda x: "-" if str(x).strip().lower() == "missing" else x)

    df_slab.insert(0, "Row Number", range(1, len(df_slab) + 1))
    df_slab.insert(1, "Select", False)

    df_slab.rename(columns={"Description": "Description - loaded from file"}, inplace=True)

    st.session_state.df_slab = df_slab

df_slab = st.session_state.df_slab

# Dropdown Options
grading_companies = ["", "PSA", "BGS", "SGC", "CSG", "HGA", "GMA", "ISA", "KSA", "RAW"]
grades = [""] + [str(x) for x in [1.0, 1.5] + [i for i in range(2, 11)]]
rookie_options = ["", "Yes", "No"]
card_sets = [
    "Court Kings", "Crusade", "Elite", "Flawless", "Gold Standard", "Hoops",
    "Immaculate Collection", "Innovation", "Intrigue", "National Treasures",
    "Pinnacle", "Preferred", "Prestige", "Prizm", "Select", "Signatures",
    "Spectra", "Timeless Treasures", "Upper Deck Black", "Titanium", "Totally Certified"
]
parallels = [
    "Purple Prizm", "Gold", "Prizm", "Silver Prizm", "Red", "Silver", "Blue",
    "Red Blue White Prizm", "Orange Die-Cut", "Blue Green", "Blue Prizm",
    "Purple", "Purple Pulsar", "Red Blue White Pulsar Prizm", "Die-Cut",
    "Black", "BLACK", "White", "Green", "Gold White", "Gold Prizm", "Green Black",
    "Red Blue White Mosaic Prizm", "Green Wave", "Blue White Prizm",
    "Red Blue Prizm", "Green Prizm", "Orange Prizm", "Red Prizm",
    "Silver Prizm Refractor", "Wave", "Blue Die-Cut Prizm", "Cracked Ice Prizm",
    "Purple Die-Cut Prizm", "Silver Green Prizm", "Gold Black", "Orange",
    "Gold Green", "Purple White", "Red Purple Prizm", "Gold Die-Cut", "Lustrous Rookies Signature",
    "Red Green Prizm", "Blue Gold Prizm", "Red Gold Prizm", "Silver White Prizm",
    "Red Silver Prizm", "Green Prizm Refractor", "Prizm Refractor", "Holo",
    "Gold Orange Prizm", "Silver Prizm Refractor Holo", "Purple White Prizm",
    "Purple Orange Prizm", "Atomic", "Green White Prizm", "Red Green",
    "Cracked Ice", "Blue Prizm Refractor", "Red Blue Mosaic Prizm", "Red Die-Cut",
    "2-on-2 Quad Memorabilia Platinum", "2-on-2 Quad Prime Memorabilia",
    "Art Nouveau Jersey Nameplates", "Art Nouveau Jersey Patches",
    "Art Nouveau Jerseys", "Art Nouveau Prime Jerseys", "Base Set Gold", "NBA Game Gear Duals", "Hall Monitors", "Brilliance", "Memorabilia Red",
    "Totally Red", "Hall of Fame Heroes", "Red Back", "Base", "Choice Award",
    "Rookie", "Purple Select Swatches", "Status", "Portraits", "Dominance", "Signatures"
]

st.title("SLAB Protocol™ AI Builder – Sandbox Demo")
st.markdown("#### A trading card standard powered by AI")

tabs = st.tabs(["\ud83d\udd04 Load Data File/Run Through Model", "\ud83d\udddd\ufe0f Edit AI Generated Fields", "\ud83d\udcca Preview SLAB Generated Data", "\ud83d\udcc4 Preview SLAB Generated XML", "\ud83d\udd0d SLAB Insights"])

with tabs[0]:
    st.markdown("### Processing Selected SLAB_Data.xlsx through Engine")
    st.dataframe(df_slab[["Description - loaded from file"]], use_container_width=True)

with tabs[1]:
    st.markdown(
        """
        ### \ud83d\udddd\ufe0f Edit SLAB Fields Workspace
        This workspace allows you to **review and refine the fields generated by the AI model** from the card description.  
        **Every change you make contributes to improving model accuracy over time.**
        """
    )

    search_query = st.text_input("Search Description")

    st.markdown("#### Bulk Update Selected Rows")
    col1, col2 = st.columns([1, 3])

    with col1:
        field_to_update = st.selectbox(
            "Field Drop Down",
            df_slab.columns[3:],
            key="bulk_field_select"
        )

    with col2:
        bulk_value = st.text_input("Value for Bulk Update", key="bulk_value_generic")

    master_checkbox = st.checkbox("Select All Visible Rows")

    if search_query:
        filtered_df = df_slab[df_slab["Description - loaded from file"].str.contains(search_query, case=False, na=False)]
    else:
        filtered_df = df_slab.copy()

    if master_checkbox:
        filtered_df.loc[:, "Select"] = True
        df_slab.loc[filtered_df.index, "Select"] = True

    column_config = {col: st.column_config.TextColumn() for col in df_slab.columns[3:]}

    edited_df = st.data_editor(
        filtered_df,
        use_container_width=True,
        num_rows="fixed",
        hide_index=True,
        column_config=column_config
    )

    for idx, row in edited_df.iterrows():
        st.session_state.df_slab.loc[idx] = row

    if st.button("Apply Bulk Update"):
        selected_rows = df_slab[df_slab["Select"].astype(bool)].index.tolist()

        if bulk_value and selected_rows:
            for idx in selected_rows:
                df_slab.at[idx, field_to_update] = bulk_value

        df_slab.loc[selected_rows, "Select"] = False
        st.session_state.df_slab = df_slab.copy()
        st.rerun()

with tabs[2]:
    st.markdown(
        """
        ### \ud83d\udcca Preview SLAB Generated Data
        This page displays the **fully structured card data** after AI extraction and any manual edits.  
        You can review the updated data here before exporting it to other formats.
        """
    )
    st.dataframe(
        st.session_state.df_slab.drop(columns=["Select"]),
        use_container_width=True
    )

with tabs[3]:
    for _, row in st.session_state.df_slab.iterrows():
        st.code(f"""
<Card>
  <Year>{row['Year']}</Year>
  <PlayerName>{row['Player Name']}</PlayerName>
  <CardNumber>{row['Card Number']}</CardNumber>
  <Set>{row['Card Set']}</Set>
  <Parallel>{row['Parallel']}</Parallel>
  <GradingCompany>{row['Grading Company']}</GradingCompany>
  <Grade>{row['Grade']}</Grade>
  <Limited>{row['Limited']}</Limited>
  <ShortPrint>{row['Short Print']}</ShortPrint>
  <Auto>{row['Auto']}</Auto>
  <Rookie>{row['Rookie']}</Rookie>
</Card>
""", language="xml")
with tabs[4]:
    st.markdown("### 🤖 SLAB Assistant – Ask Anything About SLAB Protocol™")
    user_query = st.text_area("Paste one or a list of cards descriptions for AI SLAB breakdown:")

    if st.button("Submit Query"):
        if user_query.strip():
            try:
                import json

                openai.api_key = st.secrets["OPENAI_API_KEY"]

                # For OpenAI v1.0+, use this pattern
                client = openai.Client(api_key=openai.api_key)

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": """
                        You are an expert in the SLAB Protocol™ trading card standard.
                        Your task is to break down card descriptions into a structured table with the following SLAB fields:
                        - Year
                        - Player Name
                        - Card Number
                        - Card Set
                        - Parallel
                        - Grading Company
                        - Grade
                        - Limited
                        - Short Print
                        - Auto
                        - Rookie

                        The user may provide one or multiple descriptions. For each description, output a row in JSON format.
                        Return an **array of JSON objects**, where each object represents a card and includes **only the fields listed above**.

                        If any field is unknown or not present in the description, set it as an empty string "".
                        Do not include explanations or extra text. Return **only valid JSON**.
                        """
                        },
                        {"role": "user", "content": user_query}
                    ],
                )

                gpt_response = response.choices[0].message.content.strip()

                # Handle GPT sometimes wrapping in ```json ... ```
                if gpt_response.startswith("```json"):
                    gpt_response = gpt_response[7:-3].strip()

                try:
                    parsed_response = json.loads(gpt_response)

                    if isinstance(parsed_response, dict):
                        parsed_response = [parsed_response]

                    slab_columns = [
                        "Year", "Player Name", "Card Number", "Card Set", "Parallel",
                        "Grading Company", "Grade", "Limited", "Short Print", "Auto", "Rookie"
                    ]
                    normalized_data = [{col: item.get(col, "") for col in slab_columns} for item in parsed_response]

                    result_df = pd.DataFrame(normalized_data)
                    st.markdown("**Extracted SLAB Fields:**")
                    st.dataframe(result_df, use_container_width=True)

                except json.JSONDecodeError:
                    st.error("❌ Failed to parse AI response as JSON. GPT may have included text or formatting issues.")
                    st.markdown("Here’s the raw response:")
                    st.text(gpt_response)

            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("Please enter card descriptions before submitting.")
