# app.py
import streamlit as st
import os
import time
import pandas as pd
import json
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
from pipeline.pipeline import PipelineOrchestrator
from pipeline.state_managers.pipeline_state_manager import PipelineStateManager
from pipeline.state_managers.global_state_manager import GlobalStateManager
from pipeline.workflows.resume_parser import ResumeParser
from pipeline.workflows.resume_data_processor import ResumeDataProcessor
from pipeline.workflows.features_extractor import DataExtractor
from pipeline.workflows.validators import PreScreeningValidator
from pipeline.workflows.mandatory_params_matcher import MandatoryParamsMatcher
from pipeline.workflows.optional_params_matcher import OptionalParamsMatcher
from pipeline.workflows.score_aggregator import ScoreAggregator
from pipeline.workflows.llm_jd_processor import LLMJobDescriptionProcessor
from pipeline.workflows.llm_resumes_analyzer import LLMResumesAnalyzer
from pipeline.config import (
    ROLE_MATCHING_DEFINITIONS,
    JOB_DESC_FOR_JAVA_DEVELOPER,
    JOB_DESC_FOR_REACT_DEVELOPER,
)

# Configure the app
st.set_page_config(
    page_title="Resume Matcher",
    page_icon="📄",
    layout="wide",
)

# Custom CSS for button styling
st.markdown(
    """
    <style>
    /* General App Styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background-color: #fafafa;
    }
    
    /* Button Styling with Gradient */
    .stButton > button {
        background: linear-gradient(135deg, #2563eb, #1e40af);
        color: white;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.15);
        transition: all 0.3s ease;
        width: 100%;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        border-radius: 6px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #1e40af, #1e3a8a);
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.25);
        color: white;
    }
    
    .stButton > button:active {
        transform: translateY(0px);
    }
    
    /* Notification and Info Boxes */
    .config-changed {
        background-color: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 12px 16px;
        margin: 12px 0;
        border-radius: 6px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    .llm-generated {
        background-color: #f0f9ff;
        border-left: 4px solid #0ea5e9;
        padding: 12px 16px;
        margin: 12px 0;
        border-radius: 6px;
        color: #0c4a6e;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    /* Container Styling */
    .stExpander {
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.03);
        overflow: hidden;
    }
    
    
    /* Input Boxes */
    input, textarea, .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        border-radius: 6px !important;
        border-color: #e2e8f0 !important;
        padding: 0.5rem 0.75rem !important;
    }
    
    input:focus, textarea:focus, .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    }
    
    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        border-radius: 8px;
        overflow: hidden;
        background-color: #f1f5f9;
        padding: 2px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px;
        padding: 8px 16px;
    }
    
    .stTabs [data-baseweb="tab-highlight"] {
        background-color: white;
        border-radius: 6px;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);
    }
    
    /* Divider Styling */
    hr {
        margin: 2rem 0;
        border-color: #e2e8f0;
    }
    
    /* Checkbox Styling */
    .stCheckbox > div > div > div[role="checkbox"] {
        box-shadow: 0 0 3px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    
    /* Larger Title and Subtitle */
    h1 {
        font-weight: 700 !important;
        font-size: 2.2rem !important;
        color: #111827 !important;
        margin-bottom: 1.5rem !important;
        letter-spacing: -0.025em !important;
    }
    
    h2, h3 {
        font-weight: 600 !important;
        color: #1f2937 !important;
        letter-spacing: -0.01em !important;
    }
    
    /* PDF Viewer Styling */
    .pdf-viewer-container {
        display: flex;
        flex-direction: column;
        height: calc(100vh - 200px);
        border: none;
        padding: 0;
        margin: 0;
        background: transparent;
        overflow: hidden;
    }
    
    .pdf-viewer-container iframe {
        width: 100%;
        height: 100%;
        border: none;
        background: transparent;
    }
    
    .close-viewer-btn {
        width: 100%;
        margin-top: 10px;
        background: linear-gradient(135deg, #2563eb, #1e40af) !important;
    }
    
    /* Progress Bar Styling */
    .stProgress > div > div > div {
        background-color: #3b82f6 !important;
        background-image: linear-gradient(45deg, rgba(255, 255, 255, 0.15) 25%, transparent 25%, transparent 50%, rgba(255, 255, 255, 0.15) 50%, rgba(255, 255, 255, 0.15) 75%, transparent 75%, transparent) !important;
        background-size: 1rem 1rem !important;
        animation: progress-animation 1s linear infinite !important;
    }
    
    @keyframes progress-animation {
        0% {
            background-position: 0 0;
        }
        100% {
            background-position: 1rem 0;
        }
    }
    
    /* Animated Card Effects */
    .stCard {
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .stCard:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
    }
    
    /* Subtle Header Animation */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .main h1 {
        animation: fadeIn 0.5s ease-out;
    }
    
    /* Status Indicators */
    .status-passed {
        color: #059669;
        font-weight: 600;
    }
    
    .status-failed {
        color: #dc2626;
        font-weight: 600;
    }
    
    /* Scrollbar Styling */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f5f9;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #cbd5e1;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #94a3b8;
    }
    
    </style>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@200..800&display=swap');
    body, .stMarkdown, p, div, h1, h2, h3, h4, h5, h6 {
        font-family: 'Manrope', sans-serif !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Create directories
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
MANDATORY_KEYWORDS_INPUT_KEY = "mandatory_keywords_input"


# Initialize session state variables
if "completed_resumes" not in st.session_state:
    st.session_state.completed_resumes = 0

if "total_resumes" not in st.session_state:
    st.session_state.total_resumes = 0

if "processing_status" not in st.session_state:
    st.session_state.processing_status = ""

if "results" not in st.session_state:
    st.session_state.results = []

if "global_state" not in st.session_state:
    st.session_state.global_state = GlobalStateManager(
        job_role="JAVA_DEVELOPER",
        mandatory_screening_params=ROLE_MATCHING_DEFINITIONS["JAVA_DEVELOPER"][
            "mandatory"
        ],
        optional_screening_params=ROLE_MATCHING_DEFINITIONS["JAVA_DEVELOPER"][
            "optional_groups"
        ],
        job_description=JOB_DESC_FOR_JAVA_DEVELOPER,
    )

if "keywords_configured" not in st.session_state:
    st.session_state.keywords_configured = False

if "generated_keywords" not in st.session_state:
    st.session_state.generated_keywords = None

if "use_llm_keywords" not in st.session_state:
    st.session_state.use_llm_keywords = False

if "reset_config_btn_clicked" not in st.session_state:
    st.session_state.reset_config_btn_clicked = False

if "selected_job_role" not in st.session_state:
    st.session_state.selected_job_role = "JAVA_DEVELOPER"

# Configure thread pool
MAX_WORKERS = 4  # Adjust based on system capabilities
CHUNK_SIZE = 10  # Process resumes in chunks


def save_uploaded_file(uploaded_file):
    """Save uploaded file to disk and return the path"""
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path


def process_resume_wrapper(file_info, use_default_jd, job_description, global_state):
    """Process a single resume with proper state management"""
    resume_name, file_path = file_info
    try:
        # Initialize state manager
        state = PipelineStateManager()

        # Create a copy of global state to avoid threading issues
        local_global_state = GlobalStateManager(
            job_role=global_state.job_role,
            mandatory_screening_params=global_state.mandatory_screening_params,
            optional_screening_params=global_state.optional_screening_params,
            job_description=(
                job_description if not use_default_jd else global_state.job_description
            ),
        )

        # Copy other properties
        local_global_state.use_partial_matching = global_state.use_partial_matching
        local_global_state.use_case_sensitive = global_state.use_case_sensitive
        local_global_state.use_strict_experience_check = (
            global_state.use_strict_experience_check
        )
        local_global_state.working_exp_criteria = global_state.working_exp_criteria

        # Define pipeline stages
        pipeline_stages = [
            ("Resume Parser", ResumeParser(path=file_path)),
            ("Resume Data Processor", ResumeDataProcessor()),
            ("Data Extractor", DataExtractor()),
            ("Pre-screening Validator", PreScreeningValidator()),
            ("Mandatory Keywords Matcher", MandatoryParamsMatcher()),
            ("Optional Keywords Matcher", OptionalParamsMatcher()),
            ("Score Aggregator", ScoreAggregator()),
        ]

        # Create and run pipeline
        pipeline = PipelineOrchestrator(pipeline_stages)
        result = pipeline.orchestrate(state=state, global_state=local_global_state)

        # Get viewer path from the file_info
        view_path = os.path.join("resume_viewer", resume_name)
        return resume_name, result, view_path, None
    except Exception as e:
        return resume_name, None, None, str(e)


def process_resumes(uploaded_resumes, use_default_jd, job_description, global_state):
    """Process uploaded resumes in parallel using ThreadPoolExecutor and update session state"""
    start_time = time.time()
    # Reset counters
    st.session_state.completed_resumes = 0
    st.session_state.total_resumes = len(uploaded_resumes)
    st.session_state.results = []

    status_placeholder = st.empty()
    progress_bar = st.progress(0)

    # Save resumes to disk for processing
    temp_files = []
    viewer_dir = "resume_viewer"
    os.makedirs(viewer_dir, exist_ok=True)
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    for resume in uploaded_resumes:
        file_path = os.path.join(UPLOAD_DIR, resume.name)
        with open(file_path, "wb") as f:
            f.write(resume.getbuffer())
        temp_files.append((resume.name, file_path))

        # Create permanent copy for viewing
        view_path = os.path.join(viewer_dir, resume.name)
        with open(view_path, "wb") as f:
            f.write(resume.getbuffer())

    # Determine number of workers (limit based on CPU count)
    max_workers = min(multiprocessing.cpu_count(), 4)

    # Process resumes using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_resume = {
            executor.submit(
                process_resume_wrapper,
                file_info,
                use_default_jd,
                job_description,
                global_state,
            ): file_info[0]
            for file_info in temp_files
        }

        # Process results as they complete
        for i, future in enumerate(as_completed(future_to_resume)):
            resume_name = future_to_resume[future]
            try:
                resume_name, result, view_path, error = future.result()

                if error:
                    status_placeholder.text(
                        f"❌ Failed to process {resume_name}: {error}"
                    )
                else:
                    st.session_state.results.append((resume_name, result, view_path))
                    st.session_state.completed_resumes += 1

                # Update progress
                progress = (i + 1) / len(uploaded_resumes)
                progress_bar.progress(progress)

                # Update status text
                status_placeholder.text(
                    f"✅ Completed resume {i+1}/{len(uploaded_resumes)}: {resume_name}"
                )
            except Exception as e:
                status_placeholder.text(f"❌ Error processing {resume_name}: {str(e)}")

    # Clean up temporary files
    for _, file_path in temp_files:
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass

    # Final status update
    status_placeholder.text(
        f"✅ Completed processing {st.session_state.completed_resumes} of {st.session_state.total_resumes} resumes"
    )
    end_time = time.time()
    print(f"Total time taken for processing: {end_time - start_time} seconds")


def main():
    # Create a custom header with logo

    # Display current processing status if any
    if st.session_state.processing_status:
        st.info(f"Status: {st.session_state.processing_status}")

    # Add job role selector
    available_roles = list(ROLE_MATCHING_DEFINITIONS.keys())

    def on_role_change():
        selected_role = st.session_state.job_role_selector
        if selected_role != st.session_state.selected_job_role:
            st.session_state.selected_job_role = selected_role
            # Reset LLM keywords when changing roles
            st.session_state.use_llm_keywords = False

            # Set job description based on role
            job_description = (
                JOB_DESC_FOR_REACT_DEVELOPER
                if selected_role == "REACT_DEVELOPER"
                else JOB_DESC_FOR_JAVA_DEVELOPER
            )

            # Create new global state with the selected role's configuration
            st.session_state.global_state = GlobalStateManager(
                job_role=selected_role,
                mandatory_screening_params=ROLE_MATCHING_DEFINITIONS[selected_role][
                    "mandatory"
                ],
                optional_screening_params=ROLE_MATCHING_DEFINITIONS[selected_role][
                    "optional_groups"
                ],
                job_description=job_description,
            )

            st.session_state.keywords_configured = True

    role_col1, role_col2 = st.columns([3, 3])
    with role_col2:
        st.subheader("Job Role Selection")
        st.markdown(
            "Select a job role to automatically configure matching criteria and JD."
        )
        st.selectbox(
            "Select Job Role",
            options=available_roles,
            index=(
                available_roles.index(st.session_state.selected_job_role)
                if st.session_state.selected_job_role in available_roles
                else 0
            ),
            key="job_role_selector",
            on_change=on_role_change,
        )

    with role_col1:
        st.markdown(
            """
            <div style="display: flex; align-items: center; margin-bottom: 1rem; padding-bottom: 1rem;">
                <div style="font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #2563eb, #1e40af); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-right: 0.75rem;">📄</div>
                <div>
                    <h1 style="margin: 0; padding: 0; font-size: 2.2rem; font-weight: 700;">AI Resume Matcher</h1>
                    <p style="margin: 0; padding: 0; color: #6b7280; font-size: 1rem;">Match resumes to Job Descriptions with AI-Powered Analysis</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.divider()

    # Two columns layout for JD and Keyword Configuration
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Job Description")
        use_default_jd = st.checkbox("Use default Configuration", value=True)

        # Get job description based on selected role
        if st.session_state.selected_job_role == "REACT_DEVELOPER":
            default_jd = JOB_DESC_FOR_REACT_DEVELOPER
        else:  # Default to Java Developer
            default_jd = JOB_DESC_FOR_JAVA_DEVELOPER

        if use_default_jd:
            job_description = default_jd
            st.text_area(
                f"",
                job_description,
                height=250,
                disabled=True,
            )
        else:
            job_description = st.text_area(
                "Enter Custom Job Description",
                default_jd,
                height=200,
                placeholder="Paste the job description here...",
            )
            st.session_state.global_state.job_description = job_description
            if job_description and st.button("Generate Keywords from Job Description"):
                with st.spinner(
                    "Analyzing Job Description for generating Screening Parameters..."
                ):
                    state = PipelineStateManager()

                    # Update global state with job description
                    st.session_state.global_state.job_description = job_description

                    # Create pipeline with just the JD processor
                    pipeline = PipelineOrchestrator(
                        [
                            (
                                "LLM Job Description Processor",
                                LLMJobDescriptionProcessor(),
                            )
                        ]
                    )

                    # Execute pipeline
                    result = pipeline.orchestrate(
                        state=state, global_state=st.session_state.global_state
                    )

                    if result and isinstance(result, PipelineStateManager):
                        st.session_state.use_llm_keywords = True
                        st.session_state.keywords_configured = True
                        st.success(
                            "✨ Screening Parameters were automatically generated by AI based on the Job Description."
                        )
                    else:
                        st.error(
                            "Failed to generate Screening Parameters from job description"
                        )

    with col2:
        st.subheader("Screening Parameters")

        tab1, tab2, tab3 = st.tabs(
            ["Mandatory Parameters", "Optional Parameters", "Settings"]
        )

        with tab1:
            st.write(
                "These parameters are essential - resumes without them will be filtered out."
            )

            edited_mandatory = st.text_input(
                "Mandatory Parameters (comma-separated)",
                value=", ".join(
                    st.session_state.global_state.mandatory_screening_params
                ),
                help="Edit the mandatory parameters. These are critical skills without which a candidate will be automatically disqualified.",
            )

            if edited_mandatory:
                updated_mandatory_keywords = [
                    k.strip() for k in edited_mandatory.split(",") if k.strip()
                ]
            else:
                updated_mandatory_keywords = []

            if (
                updated_mandatory_keywords
                != st.session_state.global_state.mandatory_screening_params
            ):
                st.session_state.global_state.mandatory_screening_params = (
                    updated_mandatory_keywords
                )
                st.session_state.keywords_configured = True

        with tab2:
            st.write(
                "These are grouped parameters with weights. Higher weights mean more importance."
            )

            optional_keywords = st.session_state.global_state.optional_screening_params

            if optional_keywords:
                optional_keywords_json = json.dumps(optional_keywords, indent=2)
                edited_optional = st.text_area(
                    "Optional Parameters (JSON format)",
                    value=optional_keywords_json,
                    height=300,
                    help="Edit the optional parameters in JSON format",
                )

                try:
                    updated_optional_keywords = json.loads(edited_optional)
                    if updated_optional_keywords != optional_keywords:
                        st.session_state.global_state.optional_screening_params = (
                            updated_optional_keywords
                        )
                        st.session_state.keywords_configured = True
                except json.JSONDecodeError:
                    st.error("Invalid JSON format")
            else:
                st.info("No optional parameters defined.")

        with tab3:
            col1, col2 = st.columns(2)

            with col1:
                new_partial_matching = st.checkbox(
                    "Use partial matching",
                    value=st.session_state.global_state.use_partial_matching,
                    help="Enable to match base keywords (e.g., 'React' will match 'React.js', 'ReactJS')",
                )

                if (
                    new_partial_matching
                    != st.session_state.global_state.use_partial_matching
                ):
                    st.session_state.global_state.use_partial_matching = (
                        new_partial_matching
                    )
                    st.session_state.keywords_configured = True

            with col2:
                new_use_strict_experience_check = st.checkbox(
                    "Use strict experience check",
                    value=st.session_state.global_state.use_strict_experience_check,
                    help="Enable to check if the candidate has the exact experience required for the position",
                )

                if (
                    new_use_strict_experience_check
                    != st.session_state.global_state.use_strict_experience_check
                ):
                    st.session_state.global_state.use_strict_experience_check = (
                        new_use_strict_experience_check
                    )
                    st.session_state.keywords_configured = True

            new_experience_criteria = st.number_input(
                "Minimum experience requirement (years)",
                min_value=0.0,
                max_value=20.0,
                value=float(st.session_state.global_state.working_exp_criteria),
                step=0.5,
                help="Minimum years of experience required for the position",
            )

            if (
                new_experience_criteria
                != st.session_state.global_state.working_exp_criteria
            ):
                st.session_state.global_state.working_exp_criteria = (
                    new_experience_criteria
                )
                st.session_state.keywords_configured = True

        col1, col2 = st.columns([1, 1])
        with col2:

            if st.button("Reset to Default", key="reset_config_btn"):
                st.session_state.reset_config_btn_clicked = True
                current_role = st.session_state.selected_job_role

                # Create a new global state with default values for the current role
                st.session_state.global_state = GlobalStateManager(
                    job_role=current_role,
                    mandatory_screening_params=ROLE_MATCHING_DEFINITIONS[current_role][
                        "mandatory"
                    ],
                    optional_screening_params=ROLE_MATCHING_DEFINITIONS[current_role][
                        "optional_groups"
                    ],
                    job_description=(
                        JOB_DESC_FOR_REACT_DEVELOPER
                        if current_role == "REACT_DEVELOPER"
                        else JOB_DESC_FOR_JAVA_DEVELOPER
                    ),
                )

                st.session_state.keywords_configured = False

    st.divider()

    # Upload Resumes section (full width)
    st.subheader("Upload Resume")
    st.text("You can upload multiple resumes at once")
    uploaded_resumes = st.file_uploader(
        "Choose PDF files",
        type="pdf",
        accept_multiple_files=True,
        key="resume_uploader",
    )

    if uploaded_resumes:
        st.session_state.uploaded_resumes = uploaded_resumes
    elif "uploaded_resumes" in st.session_state:
        uploaded_resumes = st.session_state.uploaded_resumes

    # Process button
    if uploaded_resumes:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("▶️ Begin Resume Analysis", key="begin_analysis_btn"):
                process_resumes(
                    st.session_state.uploaded_resumes,
                    use_default_jd,
                    job_description,
                    st.session_state.global_state,
                )

    # Display results if available
    if st.session_state.results:
        st.subheader("Screening Analysis Results")

        comparison_data = []
        for resume_name, result, view_path in st.session_state.results:
            if result is None:
                continue

            # Check if pipeline stopped early
            if result.skip_pipeline_from_execution:
                comparison_data.append(
                    {
                        "Resume": resume_name,
                        "Status": "❌ Failed",
                        "Experience (years)": "N/A",
                        "Matching Score": "0/100",
                        "Core Competencies Matched": "N/A",
                        "Additional Competencies Matched": "N/A",
                        "Screening Outcome": result.pipeline_skip_reason,
                        "View Path": view_path,
                        "Processed Content": (
                            result.processed_content_of_resume
                            if hasattr(result, "processed_content_of_resume")
                            else ""
                        ),
                    }
                )
                continue

            # Prepare optional categories string
            optional_categories_str = ""
            for category, matched_terms in result.matched_optional_groups.items():
                optional_categories_str += f"({category}): {', '.join(matched_terms)}"
                optional_categories_str += "\n\n"

            comparison_data.append(
                {
                    "Resume": resume_name,
                    "Status": f"{'✅ Passed' if result.passed else '❌ Failed'}",
                    "Experience (years)": (
                        str(result.extracted_working_exp)
                        if hasattr(result, "extracted_working_exp")
                        and result.extracted_working_exp
                        else "Unknown"
                    ),
                    "Matching Score": f"{result.score:.2f}/100",
                    "Core Competencies Matched": f"{', '.join(result.mandatory_keyword_matches)}",
                    "Additional Competencies Matched": optional_categories_str,
                    "Screening Outcome": (
                        result.pipeline_skip_reason
                        if hasattr(result, "pipeline_skip_reason")
                        and result.pipeline_skip_reason
                        else "N/A"
                    ),
                    "View Path": view_path,
                    "Processed Content": (
                        result.processed_content_of_resume
                        if hasattr(result, "processed_content_of_resume")
                        else ""
                    ),
                }
            )

        # Sort comparison_data by matching score first, then by experience (handling 'Unknown' experience)
        comparison_data = sorted(
            comparison_data,
            key=lambda x: (
                float(
                    x["Matching Score"].split("/")[0]
                ),  # Convert "XX.XX/100" to float
                (
                    float(x["Experience (years)"])
                    if not isinstance(x["Experience (years)"], str)
                    else -1
                ),
            ),
            reverse=True,
        )

        # Add a rank column to the comparison_data
        comparison_data = [
            {
                "Rank": i + 1,
                **item,
            }
            for i, item in enumerate(comparison_data)
        ]

        # Convert to DataFrame
        comparison_df = pd.DataFrame(comparison_data)

        # Initialize the view_resume session state if needed
        if "view_resume_path" not in st.session_state:
            st.session_state.view_resume_path = None

        # Display the DataFrame without on_click parameter
        event = st.dataframe(
            comparison_df.drop(columns=["View Path", "Processed Content"]),
            use_container_width=True,
            hide_index=True,
            selection_mode="multi-row",
            on_select="rerun",
            column_config={
                "Resume": st.column_config.Column(
                    "Resume",
                    help="Resume name",
                    width="medium",
                ),
                "Status": st.column_config.Column(
                    "Status",
                    help="Result status",
                    width="medium",
                ),
            },
        )

        selected_rows = event.selection.rows

        if selected_rows:
            selected_resumes_content = []
            for i in selected_rows:
                if (
                    "Processed Content" in comparison_df.iloc[i]
                    and comparison_df.iloc[i]["Processed Content"]
                ):
                    selected_resumes_content.append(
                        comparison_df.iloc[i]["Processed Content"]
                    )

            if selected_resumes_content:
                st.session_state.global_state.resumes_for_llm_analysis = (
                    selected_resumes_content
                )

        # Add a 2-column layout for resume selection and viewing
        st.subheader("View Resumes")

        # Create columns layout - first for dropdown, second for viewer
        select_col, viewer_col = st.columns([1, 3])

        with select_col:
            # Create a list of resume options with status indicators
            resume_options = []
            resume_path_map = {}

            for _, row in comparison_df.iterrows():
                status_indicator = "✅ " if "passed" in row["Status"].lower() else "❌ "
                display_name = f"{status_indicator}{row['Resume']}"
                resume_options.append(display_name)
                resume_path_map[display_name] = row["View Path"]

            if resume_options:

                # Callback to update the view_resume_path when dropdown changes
                def on_resume_select():
                    selected_option = st.session_state.resume_selector
                    if selected_option in resume_path_map:
                        st.session_state.view_resume_path = resume_path_map[
                            selected_option
                        ]

                # Auto-select first resume when loading the page
                if st.session_state.view_resume_path is None and resume_options:
                    st.session_state.view_resume_path = resume_path_map[
                        resume_options[0]
                    ]

                # Create a searchable dropdown for resume selection with callback
                selected_resume = st.selectbox(
                    "Search and select a resume to view",
                    options=resume_options,
                    index=0 if resume_options else None,
                    key="resume_selector",
                    on_change=on_resume_select,
                )

                # Show additional metadata for the selected resume
                if selected_resume:
                    selected_idx = resume_options.index(selected_resume)
                    selected_row = comparison_df.iloc[selected_idx]

                    st.markdown(
                        f"**Status:** {selected_row['Status']}", unsafe_allow_html=True
                    )
                    st.markdown(f"**Score:** {selected_row['Matching Score']}")
                    st.markdown(f"**Experience:** {selected_row['Experience (years)']}")

                    with st.expander("Core Competencies"):
                        st.markdown(f"{selected_row['Core Competencies Matched']}")

                    with st.expander("Additional Competencies"):
                        st.markdown(
                            f"{selected_row['Additional Competencies Matched']}",
                            unsafe_allow_html=True,
                        )
            else:
                st.info("No resumes available to view")

        # Display PDF viewer in the viewer column if a resume is selected
        with viewer_col:
            if st.session_state.view_resume_path:
                # Remove the resume preview heading to match screenshot
                # Display PDF in a container with fixed height
                pdf_container = st.container()

                with pdf_container:
                    try:
                        # Read the PDF file as bytes
                        with open(st.session_state.view_resume_path, "rb") as f:
                            pdf_bytes = f.read()

                        # Use base64 encoding to display the PDF
                        import base64

                        b64_pdf = base64.b64encode(pdf_bytes).decode("utf-8")

                        # Apply fullscreen PDF viewer without white background
                        pdf_display = f"""
                        <div class="pdf-viewer-container">
                            <iframe src="data:application/pdf;base64,{b64_pdf}" type="application/pdf"></iframe>
                        </div>
                        """
                        st.markdown(pdf_display, unsafe_allow_html=True)
                    except Exception as e:
                        st.error(f"Error displaying PDF: {str(e)}")
            else:
                st.info("Select a resume from the dropdown to view it here")

    # LLM Analysis section
    if st.session_state.global_state.resumes_for_llm_analysis:
        st.divider()
        st.subheader("AI Analysis")

        st.write(
            f"Number of resumes selected for detailed analysis: {len(st.session_state.global_state.resumes_for_llm_analysis)}"
        )

        if st.button("Run AI Analysis", key="run_llm_analysis_btn"):
            with st.spinner("Running AI analysis for selected candidates..."):
                state = PipelineStateManager()

                # Create LLM analyzer pipeline
                pipeline = PipelineOrchestrator(
                    [("LLM Resumes Analyzer", LLMResumesAnalyzer())]
                )

                # Execute pipeline
                result = pipeline.orchestrate(
                    state=state,
                    global_state=st.session_state.global_state,
                )

            # Check for analysis results
            if (
                hasattr(st.session_state.global_state, "output_from_llm_analysis")
                and st.session_state.global_state.output_from_llm_analysis
            ):
                try:
                    output_json = json.loads(
                        st.session_state.global_state.output_from_llm_analysis
                    )

                    # Store in session state for persistence between reruns
                    st.session_state.llm_analysis_results = output_json

                except Exception as e:
                    st.error(f"Error parsing AI analysis results: {str(e)}")
                    st.text(st.session_state.global_state.output_from_llm_analysis)

        # If we have results stored in session state, display them
        if hasattr(st.session_state, "llm_analysis_results"):
            try:
                output_json = st.session_state.llm_analysis_results

                # Create tabs for different views
                tabCandidates, tabInsights = st.tabs(
                    ["Candidate Profiles", "Comparative Insights"]
                )

                with tabCandidates:
                    # Transform candidates data into a dataframe
                    if "candidates" in output_json:
                        candidates = output_json["candidates"]

                        # Create main candidate dataframe with key metrics
                        candidate_df = pd.DataFrame(
                            [
                                {
                                    "Candidate ID": f"#{c['resume_id']}",
                                    "Name": c["candidate_name"],
                                    "Email": c["candidate_email"],
                                    "Phone": c["candidate_phone"],
                                    "Technical Match": c["technical_match_score"],
                                    "Experience Match": c["experience_relevance_score"],
                                    "Overall Score": round(
                                        (
                                            c["technical_match_score"]
                                            + c["experience_relevance_score"]
                                        )
                                        / 2,
                                        1,
                                    ),
                                    "Standout Strength": c["standout_strength"],
                                    "Focus Area": c["interview_focus_area"],
                                    "Confidence": c["confidence_score"],
                                }
                                for c in candidates
                            ]
                        )

                        # Calculate a ranking score for sorting
                        candidate_df["Ranking Score"] = (
                            candidate_df["Technical Match"] * 0.5
                            + candidate_df["Experience Match"] * 0.5
                        )

                        # Sort by overall score (descending)
                        candidate_df = candidate_df.sort_values(
                            by="Ranking Score", ascending=False
                        )
                        candidate_df = candidate_df.drop(columns=["Ranking Score"])

                        # Display the dataframe with formatting
                        st.dataframe(
                            candidate_df,
                            use_container_width=True,
                            hide_index=True,
                            column_config={
                                "Technical Match": st.column_config.ProgressColumn(
                                    "Technical Match",
                                    help="Score out of 10",
                                    format="%d/10",
                                    min_value=0,
                                    max_value=10,
                                ),
                                "Experience Match": st.column_config.ProgressColumn(
                                    "Experience Match",
                                    help="Score out of 10",
                                    format="%d/10",
                                    min_value=0,
                                    max_value=10,
                                ),
                                "Overall Score": st.column_config.ProgressColumn(
                                    "Overall Score",
                                    help="Average of technical and experience scores",
                                    format="%.1f/10",
                                    min_value=0,
                                    max_value=10,
                                ),
                                "Confidence": st.column_config.ProgressColumn(
                                    "Confidence",
                                    help="AI confidence in assessment (1-5)",
                                    format="%d/5",
                                    min_value=0,
                                    max_value=5,
                                ),
                            },
                        )

                with tabInsights:
                    if "comparative_insights" in output_json:
                        insights = output_json["comparative_insights"]

                        # Create columns for visual separation
                        st.subheader("Candidate Comparison Insights")

                        # Create a dataframe for the insights
                        insights_data = []
                        for category, data in insights.items():
                            display_category = " ".join(
                                word.capitalize() for word in category.split("_")
                            )

                            # Get candidate name from resume ID
                            candidate_name = ""
                            for c in output_json["candidates"]:
                                if c["resume_id"] == data["resume_id"]:
                                    candidate_name = c["candidate_name"]
                                    break

                            insights_data.append(
                                {
                                    "Category": display_category,
                                    "Top Candidate": f"#{data['resume_id']} - {candidate_name}",
                                    "Reason": data["reason"],
                                }
                            )

                        # Create and display the insights dataframe
                        insights_df = pd.DataFrame(insights_data)
                        st.dataframe(
                            insights_df, use_container_width=True, hide_index=True
                        )
                    else:
                        st.warning(
                            "No comparative insights found in the AI analysis results."
                        )

            except Exception as e:
                st.error(f"Error displaying AI analysis results: {str(e)}")


if __name__ == "__main__":
    main()
