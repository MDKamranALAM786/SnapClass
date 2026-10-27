import streamlit as st

def subject_card(name, code, section, stats=None, footer_callback=None):
    html = f"""
    <div style="
        background-color: #ffffff;
        padding: 25px 32px;
        border: 1px solid #626262;
        border-radius: 26px;
        margin-bottom: 20px;
        box-sizing: border-box;
        color: #1e293b;
    ">
        <h3 style="
            margin: 0;
            color: #1e293b;
            font-size: 1.5rem;
            font-weight: 700;
        ">
            {name}
        </h3>

        <p style="
            color: #64748b;
            margin: 24px 0 18px 0;
            font-size: 1.1rem;
        ">
            Code :
            <span style="
                background-color: #E0E3FF;
                color: #5865F2;
                padding: 3px 10px;
                border-radius: 5px;
            ">{code}</span>
            | Section : {section}
        </p>
    """

    if stats:
        html += """
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        ">
        """

        for icon, label, value in stats:
            html += f"""
            <div style="
                display: inline-flex;
                align-items: center;
                gap: 5px;
                background-color: #FBF0F6;
                padding: 8px 16px;
                border-radius: 14px;
                font-size: 0.95rem;
                color: #343434;
                white-space: nowrap;
            ">
                <span>{icon}</span>
                <span>{value} {label}</span>
            </div>
            """

        html += "</div>"

    html += "</div>"

    # Render HTML directly instead of passing it through Markdown.
    st.html(html)

    if footer_callback:
        footer_callback()

