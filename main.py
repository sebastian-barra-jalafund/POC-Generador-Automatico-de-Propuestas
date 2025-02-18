import streamlit as st
import datetime
import os
import zipfile
from templates import EVENT_TEMPLATES
from utils import validate_budget, validate_date, format_currency
from pdf_generator import generate_pdf

def init_session_state():
    if 'form_submitted' not in st.session_state:
        st.session_state.form_submitted = False
    if 'generated_proposal' not in st.session_state:
        st.session_state.generated_proposal = None

def create_project_zip():
    zip_filename = "event_proposal_generator.zip"
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        # Lista de archivos para incluir
        files_to_zip = ['main.py', 'templates.py', 'utils.py', 'pdf_generator.py']
        for file in files_to_zip:
            if os.path.exists(file):
                zipf.write(file)
        # Incluir la carpeta .streamlit y su contenido
        if os.path.exists('.streamlit/config.toml'):
            zipf.write('.streamlit/config.toml', '.streamlit/config.toml')
    return zip_filename

def main():
    st.set_page_config(
        page_title="Event Proposal Generator",
        page_icon="📋",
        layout="wide"
    )

    init_session_state()

    st.title("🎉 Event Proposal Generator")

    # Create columns for layout
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### Event Details")
        with st.form("event_form"):
            event_type = st.selectbox(
                "Event Type",
                options=list(EVENT_TEMPLATES.keys()),
                help="Select the type of event you're planning"
            )

            date = st.date_input(
                "Event Date",
                min_value=datetime.date.today(),
                help="Select the date of your event"
            )

            location = st.text_input(
                "Event Location",
                help="Enter the venue or location for your event"
            )

            budget = st.text_input(
                "Budget ($)",
                help="Enter your total budget for the event"
            )

            additional_requirements = st.text_area(
                "Additional Requirements",
                help="Enter any special requirements or notes for your event"
            )

            submit_button = st.form_submit_button("Generate Proposal")

            if submit_button:
                # Validate inputs
                if not location:
                    st.error("Please enter a location")
                    return

                budget_valid, budget_result = validate_budget(budget)
                if not budget_valid:
                    st.error(budget_result)
                    return

                date_valid, date_result = validate_date(date.strftime('%Y-%m-%d'))
                if not date_valid:
                    st.error(date_result)
                    return

                # Generate proposal
                proposal_template = EVENT_TEMPLATES[event_type]
                generated_proposal = proposal_template.format(
                    date=date.strftime('%B %d, %Y'),
                    location=location,
                    budget=format_currency(float(budget)),
                    additional_requirements=additional_requirements or "No additional requirements specified."
                )

                st.session_state.generated_proposal = generated_proposal
                st.session_state.form_submitted = True

    with col2:
        if st.session_state.form_submitted and st.session_state.generated_proposal:
            st.markdown("### Generated Proposal")
            st.text_area(
                "Preview",
                value=st.session_state.generated_proposal,
                height=400,
                disabled=True
            )

            # Generate PDF
            if st.button("Download PDF"):
                pdf_filename = "event_proposal.pdf"
                generate_pdf(st.session_state.generated_proposal, pdf_filename)

                with open(pdf_filename, "rb") as pdf_file:
                    pdf_bytes = pdf_file.read()

                st.download_button(
                    label="Download Proposal PDF",
                    data=pdf_bytes,
                    file_name=pdf_filename,
                    mime="application/pdf"
                )

                # Clean up the temporary PDF file
                os.remove(pdf_filename)

        # Agregar botón para descargar el proyecto completo
        st.markdown("### Download Project")
        if st.button("Download Complete Project"):
            zip_filename = create_project_zip()
            with open(zip_filename, "rb") as zip_file:
                zip_bytes = zip_file.read()

            st.download_button(
                label="Download Project ZIP",
                data=zip_bytes,
                file_name=zip_filename,
                mime="application/zip"
            )

            # Clean up the temporary ZIP file
            os.remove(zip_filename)

if __name__ == "__main__":
    main()