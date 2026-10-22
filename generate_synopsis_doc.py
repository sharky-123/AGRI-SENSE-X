"""
Generate Smart Agriculture Expert System Synopsis as a professional Word document.
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "Smart_Agriculture_Expert_System_Synopsis.docx")

doc = Document()

# ─── Page Setup ───
for section in doc.sections:
    section.top_margin = Cm(2.54)
    section.bottom_margin = Cm(2.54)
    section.left_margin = Cm(3.17)
    section.right_margin = Cm(2.54)

# ─── Style Definitions ───
style = doc.styles['Normal']
font = style.font
font.name = 'Times New Roman'
font.size = Pt(12)
style.paragraph_format.line_spacing = 1.5
style.paragraph_format.space_after = Pt(6)

# Heading styles
for level in range(1, 5):
    h_style = doc.styles[f'Heading {level}']
    h_style.font.name = 'Times New Roman'
    h_style.font.color.rgb = RGBColor(0, 0, 0)
    h_style.font.bold = True
    if level == 1:
        h_style.font.size = Pt(16)
    elif level == 2:
        h_style.font.size = Pt(14)
    elif level == 3:
        h_style.font.size = Pt(13)
    else:
        h_style.font.size = Pt(12)


def add_centered(text, size=14, bold=True, space_after=6):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    p.paragraph_format.space_after = Pt(space_after)
    return p


def add_normal(text, bold=False, italic=False, size=12, align=None, space_after=6):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic
    p.paragraph_format.space_after = Pt(space_after)
    return p


def add_justified(text, size=12, space_after=8):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.5
    return p


def add_bullet(text, bold_prefix="", size=12):
    p = doc.add_paragraph(style='List Bullet')
    if bold_prefix:
        r1 = p.add_run(bold_prefix)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(size)
        r1.bold = True
    r2 = p.add_run(text)
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(size)
    return p


def set_cell_shading(cell, color):
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)


def format_table_cell(cell, text, bold=False, size=11, align=WD_ALIGN_PARAGRAPH.LEFT):
    cell.text = ""
    p = cell.paragraphs[0]
    p.alignment = align
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(size)
    run.bold = bold


def add_table(headers, rows, col_widths=None):
    table = doc.add_table(rows=1 + len(rows), cols=len(headers))
    table.style = 'Table Grid'
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    # Header row
    for i, h in enumerate(headers):
        cell = table.rows[0].cells[i]
        format_table_cell(cell, h, bold=True, size=11, align=WD_ALIGN_PARAGRAPH.CENTER)
        set_cell_shading(cell, "D9E2F3")

    # Data rows
    for r_idx, row in enumerate(rows):
        for c_idx, val in enumerate(row):
            cell = table.rows[r_idx + 1].cells[c_idx]
            format_table_cell(cell, val, size=11)

    if col_widths:
        for i, w in enumerate(col_widths):
            for row in table.rows:
                row.cells[i].width = Cm(w)

    doc.add_paragraph()
    return table


# ════════════════════════════════════════════════════════════
# TITLE PAGE
# ════════════════════════════════════════════════════════════

doc.add_paragraph()
doc.add_paragraph()

add_centered("SMART AGRICULTURE EXPERT SYSTEM", size=20, bold=True, space_after=20)
add_centered("A Synopsis", size=14, bold=False, space_after=4)
add_centered("for", size=12, bold=False, space_after=4)
add_centered("Minor Project", size=14, bold=True, space_after=20)
add_centered("BACHELOR OF TECHNOLOGY", size=14, bold=True, space_after=4)
add_centered("in", size=12, bold=False, space_after=4)
add_centered("COMPUTER SCIENCE & ENGINEERING", size=14, bold=True, space_after=30)

add_centered("BY", size=12, bold=True, space_after=12)

add_table(
    ["Name", "Enrollment Number"],
    [
        ["Saksham Tomar", "EN24CS3T10021"],
        ["Shareen Khan", "EN23CS301948"],
        ["Sharyu Dhamne", "EN23CS301951"],
    ],
    col_widths=[8, 6]
)

add_centered("Under the Guidance of", size=12, bold=True, space_after=8)
add_centered("Prof. Jyotsana Goyal Ma'am", size=12, bold=False, space_after=4)
add_centered("Prof. Subhrata Kanungo Ma'am", size=12, bold=False, space_after=20)

add_centered("Department of Computer Science & Engineering", size=12, bold=True, space_after=4)
add_centered("Faculty of Engineering", size=12, bold=False, space_after=4)
add_centered("MEDICAPS UNIVERSITY, INDORE \u2014 453331", size=13, bold=True, space_after=8)
add_centered("March 2026", size=12, bold=True, space_after=0)

doc.add_page_break()


# ════════════════════════════════════════════════════════════
# 1. INTRODUCTION
# ════════════════════════════════════════════════════════════

doc.add_heading('1. Introduction', level=1)

add_justified(
    "Agriculture continues to be a foundation of the Indian economy, with over fifty-eight percent of "
    "rural households depending directly on farming for their primary livelihood (Ministry of Agriculture "
    "& Farmers Welfare, Government of India). Despite this significance, a considerable proportion of "
    "farming communities still follow conventional practices when evaluating field health, deciding on "
    "pest management strategies, and scheduling irrigation cycles. These choices tend to emerge from "
    "accumulated generational experience rather than from structured analytical reasoning. Such reliance "
    "on subjective observation often leads to delayed interventions, unnecessary chemical usage, avoidable "
    "crop losses, and lowered seasonal yields."
)

add_justified(
    "Parallel developments in computational intelligence \u2014 spanning supervised classification, deep "
    "convolutional feature extraction, and real-time environmental data retrieval \u2014 have created "
    "practical openings for building intelligent advisory platforms tailored to agricultural contexts. "
    "Systems that combine structured domain knowledge with statistical pattern recognition can bridge "
    "the gap between expert agronomic judgment and data-informed field management."
)

add_justified(
    "The present work introduces a hybrid intelligent agricultural advisory system that integrates "
    "three complementary reasoning pathways: a deterministic heuristic rule engine modelled on "
    "established agronomic safety constraints, a calibrated gradient-boosted tabular classifier "
    "trained on structured field observation logs, and a multi-backbone convolutional neural network "
    "ensemble trained on labelled leaf imagery for visual disease identification. These three pathways "
    "converge through a weighted confidence fusion mechanism that produces a single, interpretable "
    "recommendation for the farmer."
)

add_justified(
    "Beyond static analysis, the system incorporates a live environmental intelligence layer that "
    "retrieves real-time meteorological measurements \u2014 temperature, wind velocity, and precipitation "
    "status \u2014 from public geocoding and forecast application programming interfaces, thereby anchoring "
    "its recommendations in current atmospheric conditions rather than farmer-reported approximations."
)

add_justified(
    "The system archives every consultation into a persistent relational data store, enabling longitudinal "
    "trend analysis and outbreak alerting across repeated visits. A structured digital advisory report \u2014 "
    "containing the recommended action, supporting rationale, confidence metrics, chemical and organic "
    "treatment prescriptions, spray timing windows, and follow-up schedules \u2014 is generated for each "
    "session and exported as a portable text document."
)


# ════════════════════════════════════════════════════════════
# 2. LITERATURE REVIEW
# ════════════════════════════════════════════════════════════

doc.add_heading('2. Literature Review', level=1)

add_justified(
    "The intersection of computational methods and agricultural decision-making has been the subject "
    "of growing scholarly attention over the past decade."
)

doc.add_heading('Machine Learning for Agricultural Prediction', level=3)
add_justified(
    "Supervised learning algorithms \u2014 including Random Forest, Support Vector Machines, and "
    "gradient-boosted decision trees \u2014 have demonstrated reliable performance in structured "
    "agricultural classification tasks such as crop yield estimation, irrigation scheduling, and pest "
    "outbreak prediction. Kamilaris and Prenafeta-Boldu (2018) presented a comprehensive survey "
    "highlighting the applicability of deep learning across multiple agricultural domains, noting that "
    "ensemble methods and gradient boosting approaches frequently outperform single-model baselines "
    "when the input feature space is heterogeneous and moderately sized [1]. XGBoost, in particular, "
    "has shown strong results in tabular agricultural prediction tasks due to its regularization "
    "properties and handling of missing values (Chen and Guestrin, 2016) [12]."
)

doc.add_heading('Convolutional Neural Networks for Plant Disease Detection', level=3)
add_justified(
    "The visual identification of plant diseases through leaf image analysis has been significantly "
    "advanced by deep convolutional architectures. Mohanty, Hughes, and Salath\u00e9 (2016) demonstrated "
    "that convolutional neural networks trained on the PlantVillage benchmark dataset could distinguish "
    "between multiple disease categories with classification accuracy exceeding ninety percent under "
    "controlled imaging conditions [2]. Subsequent work by Ferentinos (2018) extended these results "
    "across broader crop species and disease combinations, confirming the generalizability of transfer "
    "learning from ImageNet-pretrained feature extractors [7]. Sladojevic et al. (2016) further "
    "validated the viability of deep neural network architectures for automated leaf disease "
    "recognition, achieving strong per-class precision metrics [5]. Recent ensemble strategies \u2014 "
    "combining multiple pretrained backbones such as EfficientNet, ResNet, and MobileNet through "
    "logit-level or probability-level fusion \u2014 have been shown to reduce variance and improve "
    "robustness relative to single-architecture baselines."
)

doc.add_heading('Expert Systems and Rule-Based Agricultural Advisors', level=3)
add_justified(
    "Knowledge-based expert systems that encode domain-specific agronomic rules have a long history "
    "in agricultural informatics. Zhang and Kovacs (2012) discussed the integration of sensor-based "
    "field observations with rule-driven reasoning engines for precision agriculture applications [3]. "
    "While purely rule-based systems provide transparent and interpretable outputs, they may lack the "
    "statistical adaptability needed when environmental conditions deviate from the patterns encoded "
    "in their rule sets."
)

doc.add_heading('Hybrid Intelligent Systems', level=3)
add_justified(
    "Wolfert et al. (2017) reviewed the convergence of big data analytics, machine learning, and "
    "domain expertise within smart farming platforms, arguing that hybrid architectures combining "
    "structured expert knowledge with data-driven statistical models yield more reliable "
    "recommendations than either approach in isolation [4]. The present work aligns with this hybrid "
    "paradigm by fusing heuristic safety constraints with calibrated probabilistic ML outputs through "
    "a weighted confidence index."
)

doc.add_heading('Probability Calibration', level=3)
add_justified(
    "In decision-critical agricultural contexts, it is essential that a classifier's predicted "
    "probability faithfully reflects the true likelihood of the predicted outcome. Isotonic "
    "regression-based probability calibration, as implemented through the Platt scaling and isotonic "
    "calibration methods available in scikit-learn's CalibratedClassifierCV, has been shown to improve "
    "the reliability of confidence estimates from boosted tree classifiers (Niculescu-Mizil and "
    "Caruana, 2005) [13]."
)

doc.add_heading('Real-Time Environmental Data Integration', level=3)
add_justified(
    "Modern weather forecast APIs \u2014 including Open-Meteo and OpenWeatherMap \u2014 provide programmatic "
    "access to current atmospheric observations with global geographic coverage. Integrating live "
    "environmental data into agricultural advisory pipelines enables context-aware recommendations "
    "that account for real-time wind drift risk, precipitation interference, and temperature "
    "suitability for chemical application."
)


# ════════════════════════════════════════════════════════════
# 3. PROBLEM DEFINITION
# ════════════════════════════════════════════════════════════

doc.add_heading('3. Problem Definition', level=1)

add_justified(
    "Field-level crop management decisions \u2014 including the timing, method, and intensity of pest "
    "control interventions \u2014 depend on the simultaneous evaluation of multiple interacting "
    "environmental and biological variables. Soil moisture content, standing water availability, "
    "insect population density, leaf surface condition, ambient wind intensity, precipitation "
    "probability, crop growth stage, and cultivated area all influence whether a chemical or organic "
    "intervention is warranted, safe, and likely to be effective."
)

add_justified(
    "Manual evaluation of these parameters is inherently limited by subjective variability, "
    "incomplete observation, and the absence of quantitative benchmarks. Spraying chemical pesticides "
    "during high-wind conditions may result in hazardous aerosol drift beyond the target area. "
    "Applying treatments immediately before anticipated rainfall diminishes active-ingredient "
    "retention on leaf surfaces. Blanket spraying across an entire field when only localized damage "
    "is present wastes resources and increases soil contamination. Conversely, failing to act "
    "promptly when disease symptoms are visually apparent can allow pathogen spread beyond "
    "recoverable thresholds."
)

add_justified(
    "Existing agricultural advisory tools typically adopt one of two isolated approaches: static "
    "rule-based systems that apply predetermined thresholds to individual parameters without learning "
    "from accumulated data, or purely statistical machine learning models that may produce accurate "
    "predictions but lack the interpretive transparency and domain safety constraints that farmers "
    "and extension officers require."
)

add_justified(
    "There is therefore a demonstrated need for an integrated intelligent system that can "
    "simultaneously analyze multiple field parameters through complementary analytical pathways \u2014 "
    "combining transparent rule-based safety evaluation with calibrated probabilistic machine "
    "learning classification and optional visual disease identification \u2014 and synthesize these "
    "perspectives into a single, confidence-weighted recommendation that the farmer can act upon "
    "with an informed understanding of the supporting rationale."
)


# ════════════════════════════════════════════════════════════
# 4. OBJECTIVES
# ════════════════════════════════════════════════════════════

doc.add_heading('4. Objectives', level=1)

add_justified(
    "The principal objectives of the Smart Agriculture Expert System are enumerated below:"
)

objectives = [
    "To architect and implement a modular, production-grade hybrid intelligent system for agricultural "
    "decision support, following object-oriented software engineering principles with centralized "
    "configuration management, structured logging, and persistent data archival.",

    "To design a multi-parameter field observation intake pipeline capable of capturing nine "
    "categorical agricultural variables: soil condition, field water availability, insect presence "
    "intensity, leaf surface condition, wind intensity, weather status, crop type, crop growth stage, "
    "and cultivated field size.",

    "To construct a deterministic rule-based expert engine that evaluates field observations against "
    "established agronomic safety constraints \u2014 including wind drift risk thresholds and heavy rain "
    "chemical washout guards \u2014 and produces an interpretable heuristic confidence score.",

    "To train and calibrate a gradient-boosted tabular classification model (XGBoost) on structured "
    "agricultural observation logs, employing Stratified K-Fold cross-validation for stability "
    "assessment and Isotonic regression for probability calibration.",

    "To develop a multi-architecture convolutional neural network ensemble \u2014 comprising "
    "EfficientNet-B0, ResNet-18, and MobileNetV3 backbones with weighted logit-level fusion \u2014 "
    "for visual leaf disease classification across a standardized thirty-eight-class plant disease "
    "taxonomy.",

    "To implement a weighted hybrid decision fusion mechanism (Custom Confidence Index) that "
    "synthesizes rule-engine heuristic confidence and calibrated ML probability into a unified "
    "decision score.",

    "To integrate a live environmental intelligence service that retrieves real-time temperature, "
    "wind speed, and sky condition data from public geocoding and weather forecast APIs, eliminating "
    "dependence on farmer-reported weather approximations.",

    "To generate structured farmer advisory outputs \u2014 including recommended action labels, chemical "
    "and organic pesticide prescriptions with dosage guidelines, spray timing windows, follow-up "
    "schedules, and technical diagnostic reports \u2014 and to export these as persistent digital "
    "receipt documents.",

    "To maintain a relational consultation archive with indexed spatial-temporal queries, enabling "
    "longitudinal trend analysis and repeated-disease outbreak alerting."
]

for i, obj in enumerate(objectives, 1):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_num = p.add_run(f"{i}. ")
    r_num.font.name = 'Times New Roman'
    r_num.font.size = Pt(12)
    r_num.bold = True
    r_text = p.add_run(obj)
    r_text.font.name = 'Times New Roman'
    r_text.font.size = Pt(12)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.5


# ════════════════════════════════════════════════════════════
# 5. SYSTEM ARCHITECTURE
# ════════════════════════════════════════════════════════════

doc.add_heading('5. System Architecture', level=1)

add_justified(
    "The Smart Agriculture Expert System is structured as a modular pipeline architecture consisting "
    "of interconnected subsystems. The following diagram illustrates the high-level data flow across "
    "the system components:"
)

doc.add_heading('5.1 System Data Flow', level=2)

add_justified(
    "The system operates through a six-stage pipeline: (1) Real-time weather satellite synchronization "
    "via Open-Meteo and OpenWeatherMap REST APIs; (2) Multi-parameter field observation collection "
    "through an interactive CLI interface; (3) Optional leaf image analysis through a triple-CNN "
    "vision ensemble; (4) Parallel evaluation through the rule-based expert engine and calibrated "
    "XGBoost ML predictor; (5) Hybrid confidence fusion via the Custom Confidence Index (CCI) "
    "weighted mechanism; and (6) Advisory report generation, database archival, and digital "
    "prescription export."
)

doc.add_heading('5.2 Module Inventory', level=2)

add_table(
    ["Module", "Source File", "Responsibility"],
    [
        ["Centralized Configuration", "config.py", "Dataclass-based system paths, API keys, model parameters, fusion thresholds, pesticide knowledge base"],
        ["Feature Mapping", "mapper.py", "Categorical-to-numeric encoding for ML-compatible feature representation"],
        ["Rule-Based Expert Engine", "decision_engine.py", "Deterministic heuristic evaluation with wind drift and rain safety guardrails"],
        ["Tabular ML Predictor", "predict_action.py", "Calibrated XGBoost classification with feature alignment and probability output"],
        ["Vision Ensemble", "ensemble_predict.py", "Multi-backbone PyTorch CNN ensemble (EfficientNet-B0 + ResNet-18 + MobileNetV3)"],
        ["Weather Intelligence", "run_agri_sense.py", "Real-time geocoding and meteorological data retrieval via REST APIs"],
        ["Hybrid Fusion Engine", "run_agri_sense.py", "Weighted CCI computation combining rule confidence and ML probability"],
        ["Advisory Reporter", "run_agri_sense.py", "Farmer advisory card rendering, technical report, digital receipt export"],
        ["Database Manager", "database_manager.py", "SQLite schema management, transactional logging, indexed historical queries"],
        ["Synthetic Data Generator", "generate_synthetic_data.py", "Randomized agricultural observation log generation for model training"],
        ["Training Pipelines", "train_tabular.py, train_cv.py, calibrate.py", "XGBoost training, 5-Fold stratified CV, Isotonic calibration"],
        ["CNN Training Pipelines", "train_pest_cnn.py, train_pest_cv.py", "Keras CNN and EfficientNet-based pest model training"],
        ["Consultation Log Viewer", "view_logs.py", "Terminal dashboard for historical consultation analysis"],
        ["Application Entry Point", "run_agri_sense.py", "CLI argument parsing, pipeline orchestration, end-to-end execution"],
    ],
    col_widths=[4, 4.5, 7]
)


# ════════════════════════════════════════════════════════════
# 6. METHODOLOGY
# ════════════════════════════════════════════════════════════

doc.add_heading('6. Methodology', level=1)

# 6.1
doc.add_heading('6.1 Data Collection and Synthetic Augmentation', level=2)

add_justified(
    "The system operates on structured field observation records comprising nine categorical "
    "agricultural parameters: soil moisture condition (Wet / Normal / Dry / Hard-Dry), field water "
    "availability (Too much / Normal / Low / Very low), insect presence intensity (Many / Few / None "
    "/ Not sure), leaf surface condition (Holes-eaten / Spots-color change / Curled leaves / Leaves "
    "normal), wind intensity (Strong / Light / No wind), weather status (Clear / Cloudy / Light rain "
    "/ Heavy rain / Not sure), crop type (Maize / Wheat / Rice / Cotton / Vegetables / Other), crop "
    "growth stage (Early / Mid / Late), and cultivated field size (Small / Medium / Large)."
)

add_justified(
    "For model training and validation, a synthetic data generation module produces realistic "
    "observation samples by randomly sampling from the defined categorical option space, computing "
    "rule-engine decisions for each generated sample, and appending the resulting records to a "
    "persistent CSV log file. This bootstrap strategy ensures sufficient sample diversity for "
    "robust classifier training even in the absence of large-scale field-collected datasets."
)

add_justified(
    "For the visual disease detection pathway, leaf imagery is drawn from the publicly available "
    "PlantVillage benchmark dataset, which contains labelled images spanning thirty-eight disease "
    "and healthy-plant categories across fourteen crop species (Mohanty et al., 2016) [2]."
)

# 6.2
doc.add_heading('6.2 Feature Preprocessing and Encoding', level=2)

add_justified(
    "Raw categorical field observations are transformed into quantitative numerical representations "
    "through a deterministic mapping module. Each categorical level is assigned a domain-informed "
    "numeric value: for instance, soil moisture categories map to estimated volumetric moisture "
    "percentages (Wet \u2192 47.0, Normal \u2192 35.0, Dry \u2192 22.0, Hard-Dry \u2192 10.0), while insect "
    "presence maps to estimated count densities (Many \u2192 20.0, Few \u2192 7.0, None \u2192 0.0). Crop type "
    "is encoded via one-hot dummy variable expansion to preserve nominal category structure. This "
    "combined numeric representation is aligned against the trained model's expected feature column "
    "ordering before inference."
)

# 6.3
doc.add_heading('6.3 Rule-Based Expert Engine', level=2)

add_justified(
    "A deterministic heuristic evaluation engine assesses field observations against structured "
    "agronomic safety rules. The engine computes a cumulative risk score by evaluating insect "
    "activity levels (contributing 2.0 points if insects are present), leaf damage indicators "
    "(contributing 2.0 points if abnormal leaf conditions are observed), soil moisture deficits "
    "(contributing 1.0 point if soil is dry), and water availability shortfalls (contributing 1.0 "
    "point if field water is low)."
)

add_justified(
    "Two absolute safety guardrails operate as early-exit constraints: if heavy rainfall is detected "
    "or reported, the engine immediately returns a \"No Spray - Monitor\" recommendation with minimal "
    "confidence (0.10), recognizing that chemical application would be washed away. Similarly, if "
    "wind intensity is classified as strong, the engine returns a monitoring recommendation with "
    "reduced confidence (0.20) to prevent hazardous spray drift."
)

add_justified(
    "Based on the cumulative risk score, the engine assigns one of three action labels \u2014 "
    "\"Spray (patch only)\" for scores at or above 4.0, \"Monitor & Spot-Treat\" for scores between "
    "2.0 and 4.0, and \"No Spray - Monitor\" for scores below 2.0 \u2014 along with a corresponding "
    "heuristic confidence value."
)

# 6.4
doc.add_heading('6.4 Calibrated Machine Learning Classification', level=2)

add_justified(
    "A gradient-boosted decision tree classifier (XGBoost, Chen and Guestrin, 2016 [12]) is trained "
    "on the structured observation log dataset to predict crop management action labels. The model "
    "configuration employs 200 estimators with a maximum tree depth of four and a learning rate of "
    "0.1, using multiclass logarithmic loss as the optimization objective."
)

add_justified(
    "Model stability is assessed through Stratified 5-Fold Cross-Validation, measuring weighted "
    "F1-score consistency across partitions. Following base model training, Isotonic regression-based "
    "probability calibration is applied using scikit-learn's CalibratedClassifierCV with 5-fold "
    "internal cross-validation. This calibration step adjusts the raw predicted probabilities to "
    "better reflect true class frequencies, producing more reliable confidence estimates for "
    "downstream fusion. Calibration quality is evaluated using a multiclass Brier score and "
    "visualized through reliability diagrams plotting predicted confidence against observed accuracy."
)

add_justified(
    "When the XGBoost library is unavailable in the runtime environment, the system gracefully "
    "falls back to scikit-learn's HistGradientBoostingClassifier, ensuring operational continuity "
    "across deployment configurations."
)

# 6.5
doc.add_heading('6.5 Multi-Architecture Convolutional Neural Network Ensemble', level=2)

add_justified(
    "The visual disease detection subsystem employs a triple-backbone ensemble architecture "
    "implemented in PyTorch and the Timm model library. Three pretrained ImageNet feature "
    "extractors \u2014 EfficientNet-B0, ResNet-18, and MobileNetV3-Large \u2014 are independently fine-tuned "
    "on the thirty-eight-class PlantVillage leaf disease taxonomy. At inference time, input leaf "
    "images are resized to 224\u00d7224 pixels, normalized using ImageNet channel statistics "
    "(mean = [0.485, 0.456, 0.406], standard deviation = [0.229, 0.224, 0.225]), and passed through "
    "all three backbone networks simultaneously."
)

add_justified(
    "The resulting logit vectors are combined through weighted averaging \u2014 40% EfficientNet-B0, "
    "30% ResNet-18, 30% MobileNetV3 \u2014 and converted to probability distributions via softmax "
    "normalization. The class with the highest fused probability is selected as the predicted "
    "disease category. This ensemble strategy reduces individual model variance and leverages "
    "the complementary feature extraction characteristics of each architecture family."
)

add_justified(
    "The ensemble checkpoint file stores individual state dictionaries for all three backbones, "
    "enabling atomic checkpoint loading and deterministic reproducibility. When PyTorch dependencies "
    "are absent from the deployment environment, the vision layer degrades gracefully to a skip "
    "mode, allowing the remaining analytical pathways to operate independently."
)

# 6.6
doc.add_heading('6.6 Hybrid Decision Fusion \u2014 Custom Confidence Index (CCI)', level=2)

add_justified(
    "The outputs from the rule-based expert engine and the calibrated tabular ML predictor are "
    "synthesized through a weighted fusion mechanism termed the Custom Confidence Index (CCI). "
    "The CCI is computed as:"
)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
run = p.add_run("CCI = (0.40 \u00d7 Rule_Confidence) + (0.60 \u00d7 ML_Probability)")
run.font.name = 'Times New Roman'
run.font.size = Pt(12)
run.bold = True
run.italic = True
p.paragraph_format.space_before = Pt(8)
p.paragraph_format.space_after = Pt(8)

add_justified(
    "This weighting assigns greater influence to the data-driven calibrated ML component while "
    "preserving the transparent safety constraints encoded in the rule engine. The final action "
    "label is selected as the ML prediction when CCI exceeds a configurable decision threshold "
    "(default 0.55), and defaults to the rule-engine recommendation otherwise. This design ensures "
    "that when the ML model exhibits high calibrated confidence, its prediction guides the final "
    "output, but when statistical confidence is low, the deterministic rule-engine assessment prevails."
)

add_justified(
    "When the optional vision ensemble detects a high-confidence disease match (confidence \u2265 0.80), "
    "the system overrides the leaf condition parameter to \"Holes / eaten\" before rule and ML "
    "evaluation, ensuring that strong visual evidence of disease propagates through both analytical "
    "pathways."
)

# 6.7
doc.add_heading('6.7 Real-Time Atmospheric Telemetry & Microclimate Risk Engine', level=2)

add_justified(
    "A key scientific contribution of this architecture is its real-time atmospheric telemetry service "
    "anchored on the Open-Meteo satellite and global reanalysis infrastructure. Rather than relying on "
    "subjective, farmer-reported estimates, the system automatically resolves geographical coordinates via "
    "high-precision geocoding and retrieves live surface parameters: 2-meter air temperature (\u00b0C), "
    "apparent temperature (\u00b0C), relative humidity (%), precipitation rate (mm/h), rainfall accumulations, "
    "and 10-meter wind vectors (m/s). Weather codes are mapped to standardized environmental categories."
)

add_justified(
    "To counter chemical drift hazards and washout losses, the system computes a dynamic Microclimate Drift "
    "Risk Index (MDRI). When wind velocity exceeds safety thresholds or imminent precipitation is identified, "
    "the decision engine initiates safety interlocks, blocking chemical spray windows and recalculating safe "
    "application intervals."
)

add_justified(
    "If the primary Open-Meteo service is unreachable, the system falls back to the OpenWeatherMap "
    "REST API as a secondary data source. If both services are unavailable, the system transitions "
    "to manual input mode, prompting the farmer to select wind and weather conditions from "
    "structured menus. This multi-tiered degradation strategy ensures operational continuity "
    "regardless of network connectivity."
)

add_justified(
    "When live weather data is successfully retrieved, the system automatically configures wind "
    "intensity and weather status parameters, bypassing the corresponding manual input prompts and "
    "ensuring that recommendations are anchored in measured atmospheric conditions."
)

# 6.8
doc.add_heading('6.8 Persistent Data Archival and Trend Intelligence', level=2)

add_justified(
    "Every consultation session is archived in a SQLite relational database with a structured schema "
    "capturing field identifier, timestamp, farmer name, location, crop type, detected disease "
    "label, AI confidence score, final recommended action, CCI score, weather status, and wind "
    "condition. The database schema includes composite indexes on (farmer_name, location) and "
    "(timestamp DESC) to support efficient historical retrieval and spatial-temporal querying."
)

add_justified(
    "A trend intelligence module queries the most recent consultation records for a given farmer "
    "and location combination. If two or more recent records indicate active disease detection, "
    "the system generates a proactive alert notifying the farmer of potential recurring pest "
    "activity, supporting early intervention and outbreak containment."
)

# 6.9
doc.add_heading('6.9 Advisory Report and Digital Prescription Generation', level=2)

add_justified(
    "The system produces three structured output artifacts for each consultation:"
)

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r1 = p.add_run("Farmer Advisory Card: ")
r1.bold = True
r1.font.name = 'Times New Roman'
r1.font.size = Pt(12)
r2 = p.add_run(
    "A terminal-rendered summary containing the date, time, field identifier, detected disease "
    "category and AI confidence (if applicable), crop and field condition summary, recommended "
    "action with plain-language instructions, CCI confidence percentage, optimal spray timing "
    "window, and next recommended field inspection schedule. The spray window is dynamically "
    "blocked if heavy rain or strong wind conditions are detected."
)
r2.font.name = 'Times New Roman'
r2.font.size = Pt(12)
p.paragraph_format.line_spacing = 1.5

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r1 = p.add_run("Expert Prescription: ")
r1.bold = True
r1.font.name = 'Times New Roman'
r1.font.size = Pt(12)
r2 = p.add_run(
    "A structured chemical and organic treatment recommendation derived from an internal "
    "pesticide knowledge base indexed by disease category. Each prescription specifies a recommended "
    "chemical agent with concentration dosage, an organic alternative treatment, and safety precautions."
)
r2.font.name = 'Times New Roman'
r2.font.size = Pt(12)
p.paragraph_format.line_spacing = 1.5

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
r1 = p.add_run("Technical Diagnostic Report: ")
r1.bold = True
r1.font.name = 'Times New Roman'
r1.font.size = Pt(12)
r2 = p.add_run(
    "A research-grade audit trace presenting individual component outputs \u2014 vision ensemble "
    "prediction with probability, rule engine decision with heuristic confidence and contributing "
    "reasons, calibrated ML prediction with probability, and hybrid fusion final label with CCI "
    "score \u2014 enabling transparent post-hoc review of the system's reasoning process."
)
r2.font.name = 'Times New Roman'
r2.font.size = Pt(12)
p.paragraph_format.line_spacing = 1.5

add_justified(
    "All three outputs are additionally consolidated into a portable text-format digital receipt "
    "exported to a designated reports directory with a standardized filename incorporating the "
    "farmer name, location, date, and timestamp."
)


# ════════════════════════════════════════════════════════════
# 7. IMPLEMENTATION DETAILS
# ════════════════════════════════════════════════════════════

doc.add_heading('7. Implementation Details', level=1)

doc.add_heading('7.1 Technology Stack', level=2)

add_table(
    ["Layer", "Technology", "Version / Specification"],
    [
        ["Programming Language", "Python", "3.12+"],
        ["Gradient Boosting", "XGBoost", "3.4+"],
        ["Deep Learning Framework", "PyTorch", "2.x (CPU/CUDA)"],
        ["Model Architecture Library", "Timm (PyTorch Image Models)", "1.0+"],
        ["Alternative DL Framework", "TensorFlow / Keras", "2.x"],
        ["Scientific Computing", "NumPy, Pandas", "Standard"],
        ["Machine Learning Toolkit", "Scikit-Learn", "1.7+"],
        ["Probability Calibration", "CalibratedClassifierCV", "Isotonic, 5-Fold"],
        ["Image Processing", "Pillow (PIL), TorchVision", "Standard"],
        ["Visualization", "Matplotlib", "3.x"],
        ["Database", "SQLite3", "Built-in (Python stdlib)"],
        ["HTTP Client", "Requests", "Standard"],
        ["Model Serialization", "Joblib", "Standard"],
        ["Configuration", "Python Dataclasses", "Frozen, Centralized"],
        ["Weather APIs", "Open-Meteo (Primary), OpenWeatherMap (Fallback)", "REST / JSON"],
        ["CLI Framework", "argparse", "Standard"],
        ["Logging", "Python logging module", "File + Console handlers"],
    ],
    col_widths=[4, 5.5, 4.5]
)

doc.add_heading('7.2 Project Directory Structure', level=2)

structure_lines = [
    "agri-sense-x/",
    "  src/                              Source modules",
    "    run_agri_sense.py               Main application pipeline",
    "    config.py                       Centralized configuration",
    "    mapper.py                       Feature encoding",
    "    decision_engine.py              Rule-based expert engine",
    "    predict_action.py               Calibrated ML predictor",
    "    ensemble_predict.py             PyTorch vision ensemble",
    "    predict_pest.py                 Keras pest predictor (standalone)",
    "    database_manager.py             SQLite persistence",
    "    generate_synthetic_data.py      Synthetic data generator",
    "    train_tabular.py                XGBoost training pipeline",
    "    train_cv.py                     5-Fold cross-validation",
    "    calibrate.py                    Isotonic calibration pipeline",
    "    train_pest_cnn.py              Basic Keras CNN training",
    "    train_pest_cv.py               EfficientNet fine-tuning (Keras)",
    "    view_logs.py                    Database consultation viewer",
    "    utils.py                        Shared utility functions",
    "  models/                           Serialized model artifacts",
    "    ensemble_pest_model.pth         PyTorch triple-CNN checkpoint (~75 MB)",
    "    pest_model_final.h5             Keras EfficientNet model (~76 MB)",
    "    model_calibrated.pkl            Calibrated XGBoost model",
    "    calibration_plot.png            Reliability diagram",
    "  data/                             Datasets and database",
    "    logs.csv                        Training observation logs",
    "    agri_sense.db                   SQLite consultation archive",
    "  reports/                          Exported digital prescriptions",
    "  test_images/                      Sample leaf images for testing",
    "  logs/                             Application runtime logs",
    "  requirements.txt                  Python dependency manifest",
    "  README.md                         Project documentation",
]

for line in structure_lines:
    p = doc.add_paragraph()
    run = p.add_run(line)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.0


# ════════════════════════════════════════════════════════════
# 8. RESULTS AND OBSERVATIONS
# ════════════════════════════════════════════════════════════

doc.add_heading('8. Results and Observations', level=1)

doc.add_heading('8.1 Tabular Classification Performance', level=2)
add_justified(
    "The calibrated XGBoost classifier achieved a test-set classification accuracy of 90% on the "
    "structured observation log dataset, with a multiclass Brier score of 0.1557 indicating "
    "well-calibrated probability estimates. The reliability diagram confirmed close alignment "
    "between predicted confidence values and observed accuracy across ten calibration bins."
)

doc.add_heading('8.2 Vision Ensemble Inference', level=2)
add_justified(
    "The PyTorch triple-CNN ensemble successfully performed leaf disease classification on test "
    "images, producing disease category predictions with associated probability scores. The "
    "ensemble correctly identified disease categories from the thirty-eight-class PlantVillage "
    "taxonomy and the weighted fusion strategy (40/30/30) produced stable probability distributions "
    "across backbone architectures."
)

doc.add_heading('8.3 End-to-End System Validation', level=2)
add_justified(
    "Complete end-to-end pipeline execution was validated with real-time Open-Meteo weather data "
    "retrieval for the city of Indore, India (resolved coordinates: latitude 22.72, longitude "
    "75.86). The system successfully retrieved live atmospheric measurements (temperature: "
    "25.5\u00b0C, wind speed: 4.0 m/s, sky condition: Cloudy), applied automatic weather parameter "
    "configuration, executed all three analytical pathways (rule engine, calibrated ML, vision "
    "ensemble), computed the hybrid CCI score (0.73), generated a complete advisory card with "
    "expert pesticide prescription, archived the consultation record in the SQLite database, and "
    "exported a digital receipt file."
)


# ════════════════════════════════════════════════════════════
# 9. CONCLUSION AND FUTURE SCOPE
# ════════════════════════════════════════════════════════════

doc.add_heading('9. Conclusion and Future Scope', level=1)

add_justified(
    "The Smart Agriculture Expert System demonstrates a practical implementation of hybrid "
    "artificial intelligence for agricultural decision support. By combining transparent rule-based "
    "safety constraints with calibrated machine learning classification and multi-architecture deep "
    "learning disease detection, the system provides farmers with actionable, confidence-weighted "
    "recommendations grounded in both domain expertise and statistical evidence."
)

doc.add_heading('Future Enhancements', level=2)

future_items = [
    ("Mobile Application Interface: ", "Developing an Android-based front-end to enable field-level "
     "usage with smartphone camera integration for real-time leaf image capture."),
    ("Regional Language Support: ", "Extending advisory outputs to local Indian languages (Hindi, "
     "Marathi, Gujarati) to improve accessibility for non-English-speaking farming communities."),
    ("IoT Sensor Integration: ", "Incorporating direct readings from soil moisture sensors, humidity "
     "probes, and weather stations deployed at the field level."),
    ("Expanded Disease Taxonomy: ", "Training the vision ensemble on broader and more region-specific "
     "crop disease datasets beyond the PlantVillage benchmark."),
    ("Cloud Deployment: ", "Deploying the advisory pipeline as a REST API service for scalable, "
     "multi-user concurrent access."),
]

for bold_part, normal_part in future_items:
    add_bullet(normal_part, bold_prefix=bold_part)


# ════════════════════════════════════════════════════════════
# 10. REFERENCES
# ════════════════════════════════════════════════════════════

doc.add_heading('10. References', level=1)

doc.add_heading('Journal References', level=2)

refs_journal = [
    "[1] Kamilaris A., Prenafeta-Boldu F.X., \"Deep Learning in Agriculture: A Survey\", "
    "Computers and Electronics in Agriculture, Volume 147, pp. 70\u201390, 2018.",

    "[2] Mohanty S.P., Hughes D.P., Salath\u00e9 M., \"Using Deep Learning for Image-Based Plant "
    "Disease Detection\", Frontiers in Plant Science, Volume 7, Article 1419, 2016.",

    "[3] Zhang C., Kovacs J.M., \"The Application of Small Unmanned Aerial Systems for Precision "
    "Agriculture: A Review\", Precision Agriculture, Volume 13, pp. 693\u2013712, 2012.",

    "[4] Wolfert S., Ge L., Verdouw C., Bogaardt M., \"Big Data in Smart Farming \u2014 A Review\", "
    "Agricultural Systems, Volume 153, pp. 69\u201380, 2017.",

    "[5] Sladojevic S., Arsenovic M., Anderla A., Culibrk D., Stefanovic D., \"Deep Neural Networks "
    "Based Recognition of Plant Diseases by Leaf Image Classification\", Computational Intelligence "
    "and Neuroscience, Volume 2016, Article ID 3289801, 2016.",
]

for ref in refs_journal:
    add_justified(ref, size=11, space_after=4)

doc.add_heading('Conference References', level=2)

refs_conf = [
    "[6] Liakos K.G., Busato P., Moshou D., Pearson S., Bochtis D., \"Machine Learning in "
    "Agriculture: A Review\", Sensors, Volume 18, Issue 8, Article 2674, 2018.",

    "[7] Ferentinos K.P., \"Deep Learning Models for Plant Disease Detection and Diagnosis\", "
    "Computers and Electronics in Agriculture, Volume 145, pp. 311\u2013318, 2018.",
]

for ref in refs_conf:
    add_justified(ref, size=11, space_after=4)

doc.add_heading('Book References', level=2)

refs_books = [
    "[8] Russell S., Norvig P., Artificial Intelligence: A Modern Approach, "
    "Pearson Education, Fourth Edition, 2020.",

    "[9] Goodfellow I., Bengio Y., Courville A., Deep Learning, "
    "MIT Press, First Edition, 2016.",
]

for ref in refs_books:
    add_justified(ref, size=11, space_after=4)

doc.add_heading('Technical References', level=2)

refs_tech = [
    "[10] Tan M., Le Q.V., \"EfficientNet: Rethinking Model Scaling for Convolutional Neural "
    "Networks\", Proceedings of the 36th International Conference on Machine Learning (ICML), "
    "pp. 6105\u20136114, 2019.",

    "[11] Howard A.G. et al., \"Searching for MobileNetV3\", Proceedings of the IEEE/CVF "
    "International Conference on Computer Vision (ICCV), pp. 1314\u20131324, 2019.",

    "[12] Chen T., Guestrin C., \"XGBoost: A Scalable Tree Boosting System\", Proceedings of the "
    "22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, "
    "pp. 785\u2013794, 2016.",

    "[13] Niculescu-Mizil A., Caruana R., \"Predicting Good Probabilities with Supervised Learning\", "
    "Proceedings of the 22nd International Conference on Machine Learning (ICML), "
    "pp. 625\u2013632, 2005.",
]

for ref in refs_tech:
    add_justified(ref, size=11, space_after=4)

doc.add_heading('Online References', level=2)

refs_online = [
    "[14] Food and Agriculture Organization (FAO), Smart Agriculture Technologies, "
    "https://www.fao.org, accessed on 04/03/2026.",

    "[15] Kaggle PlantVillage Disease Dataset, https://www.kaggle.com/datasets, "
    "accessed on 04/03/2026.",

    "[16] Ministry of Agriculture & Farmers Welfare, Government of India, "
    "https://agricoop.nic.in, accessed on 04/03/2026.",

    "[17] Open-Meteo Weather API Documentation, https://open-meteo.com, "
    "accessed on 03/09/2026.",
]

for ref in refs_online:
    add_justified(ref, size=11, space_after=4)


# ────────────────────────────────────────────────
# SAVE DOCUMENT
# ────────────────────────────────────────────────

doc.save(OUTPUT_PATH)
print(f"\n[SUCCESS] Synopsis document saved to: {OUTPUT_PATH}")
print(f"File size: {os.path.getsize(OUTPUT_PATH):,} bytes")
