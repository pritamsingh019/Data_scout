"""
DataScout — Query Input Component.

Renders the natural language query input with contextual suggestions.
"""

from typing import Optional, List, Dict

import streamlit as st


def generate_suggestions(columns: List[str], dtypes: Dict[str, str]) -> List[str]:
    """Generate contextual query suggestions based on dataset schema.

    Args:
        columns: List of column names.
        dtypes: Dict mapping column name to dtype string.

    Returns:
        Up to 5 query suggestions tailored to the dataset.
    """
    suggestions = []

    numeric_cols = [c for c, d in dtypes.items() if 'int' in d or 'float' in d]
    categorical_cols = [c for c, d in dtypes.items() if 'object' in d or 'category' in d]
    date_cols = [c for c, d in dtypes.items() if 'datetime' in d]

    if numeric_cols and categorical_cols:
        suggestions.append(
            f"What is the average {numeric_cols[0]} by {categorical_cols[0]}?"
        )

    if numeric_cols:
        suggestions.append(f"Show me the top 10 rows by {numeric_cols[0]}")
        suggestions.append(f"What is the distribution of {numeric_cols[0]}?")

    if date_cols and numeric_cols:
        suggestions.append(
            f"Show me {numeric_cols[0]} trends over {date_cols[0]}"
        )

    if len(numeric_cols) >= 2:
        suggestions.append(
            f"What is the correlation between {numeric_cols[0]} and {numeric_cols[1]}?"
        )

    return suggestions[:5]


def render_query_input(dataset_loaded: bool) -> Optional[str]:
    """Render the natural language query input field.

    Args:
        dataset_loaded: Whether a dataset has been uploaded and is ready.

    Returns:
        The user's query string, or None if no query was submitted.
    """
    st.subheader("💬 Ask a Question")

    if not dataset_loaded:
        st.text_input(
            "Your question",
            placeholder="Upload a dataset first to get started...",
            disabled=True,
            key="query_input_disabled"
        )
        return None

    # Show suggestions if metadata is available
    metadata = st.session_state.get('dataset_metadata')
    if metadata:
        suggestions = generate_suggestions(
            metadata.get('columns', []),
            metadata.get('dtypes', {})
        )
        if suggestions:
            st.caption("💡 **Suggestions:** " + " • ".join(suggestions))

    # Query input
    query = st.text_input(
        "Your question",
        placeholder="e.g., What is the average revenue by region?",
        key="query_input",
        max_chars=500,
        label_visibility="collapsed"
    )

    # Submit button
    col1, col2 = st.columns([6, 1])
    with col2:
        submitted = st.button("🔍 Ask", type="primary", use_container_width=True)

    if submitted and query and query.strip():
        return query.strip()

    return None
