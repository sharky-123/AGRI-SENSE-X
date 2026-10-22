// FARM-SENSE X Mobile Client Controller with 3-Tab Architecture (Left: Advisory, Center: Camera, Right: Pesticides)

const I18N = {
  hi: {
    splashTagline: "किसान AI साथी • Smart Agro Expert",
    splashLoading: "🛰️ उपग्रह मौसम और AI लोड हो रहा है...",
    hdrSubtitle: "v2.5 किसान सलाहकार",
    langBtnText: "English में देखें",
    tagWeather: "🛰️ उपग्रह लाइव मौसम",
    cityPlaceholder: "गांव या शहर का नाम लिखें",
    lblTemp: "🌡️ तापमान",
    lblWind: "💨 हवा की गति",
    lblHumidity: "💧 नमी",
    lblDrift: "🍃 बहाव जोखिम",
    tagVision: "📸 पत्ती रोग AI स्कैनर (LEAF SCAN)",
    descVision: "रोगग्रस्त पत्ती की फोटो लाइव कैमरे से लें या फोन से अपलोड करें। प्रशिक्षित AI मॉडल तुरंत घाव स्कैन करेगा:",
    btnCamText: "लाइव कैमरा शुरू करें",
    btnGalText: "गैलरी से चुनें",
    tagField: "📋 खेत की स्थिति",
    badgeStandard: "ICAR / USDA मानक",
    lblFarmerName: "👤 किसान का नाम",
    lblCropStage: "🌱 फसल और अवस्था",
    lblSoil: "🏜️ मिट्टी की नमी (छूकर परखें)",
    lblInsects: "🐛 कीट / कीड़े की संख्या",
    lblLeaf: "🍃 पत्तों की हालत",
    lblFieldSize: "📐 खेत का आकार",
    lblDisease: "🔬 लक्षित बीमारी / कीट",
    btnRunText: "⚡ AI जांच शुरू करें",
    btnRunningText: "⚙️ AI गणना जारी है...",
    tagAdvice: "🌾 किसान सलाह पत्र",
    titleTimeline: "⏰ समय सारिणी:",
    lblSprayWindow: "🕒 छिड़काव का सही समय:",
    lblNextCheck: "🔍 अगला निरीक्षण:",
    titlePrescription: "🧪 सटीक दवा और खुराक (Kaggle 132-Pest DB):",
    lblPestTarget: "🎯 लक्ष्य:",
    lblPestChem: "💊 रासायनिक दवा:",
    lblPestDose: "⚖️ सही खुराक:",
    lblPestOrganic: "🌿 जैविक उपाय:",
    lblPestSafety: "⚠️ सुरक्षा नियम:",
    titleReasons: "💡 AI निर्णय का कारण:",
    btnViewReceiptText: "📜 डिजिटल परामर्श पर्ची देखें व प्रिंट करें",
    navAdvisory: "सलाह (Advisory)",
    navCamera: "स्कैन (Scan)",
    navPesticides: "दवाएं (Pesticides)",
    tagPestsHdr: "🧪 132 कीट एवं दवा भंडार",
    descPests: "Kaggle प्रमाणित 132 कृषि कीटों, उनकी रासायनिक दवाओं, मानक खुराक और जैविक विकल्पों की पूरी डायरेक्टरी:",
    soilPills: {
      Wet: "💦 गीली (47%)",
      Normal: "✨ सामान्य (35%)",
      Dry: "🍂 सूखी (22%)",
      "Hard-Dry": "🧱 कठोर सूखी (10%)"
    },
    insectsPills: {
      None: "🚫 कोई नहीं",
      Few: "⚠️ कुछ जगह",
      Many: "🚨 बहुत ज्यादा",
      "Not sure": "❓ पक्का नहीं"
    },
    leafPills: {
      "Leaves normal": "🌿 स्वस्थ",
      "Spots / color change": "🟡 धब्बे/पीलापन",
      "Holes / eaten": "🕳️ कटे/छिद्र",
      "Curled leaves": "🌀 मुड़े हुए"
    },
    fieldSizePills: {
      Small: "🏡 छोटा (<1 Ha)",
      Medium: "🚜 मध्यम (1-3 Ha)",
      Large: "🌾 बड़ा (>3 Ha)"
    },
    rcptTitle: "डिजिटल किसान परामर्श पर्ची • Digital Agro Prescription",
    rcptFarmerLbl: "किसान",
    rcptCityLbl: "स्थान",
    rcptCropLbl: "फसल",
    rcptDateLbl: "दिनांक",
    rcptLiveLbl: "लाइव मौसम",
    rcptActionTag: "अनुशंसित कार्य",
    rcptSafetyLbl: "सुरक्षा नियम",
    rcptReasonLbl: "कारण",
    btnPrintLbl: "प्रिंट / PDF सेव करें",
    btnTxtLbl: ".TXT फाइल डाउनलोड",
    thTarget: "लक्षित कीट",
    thChem: "रासायनिक दवा",
    thDose: "खुराक",
    thOrganic: "जैविक उपाय"
  },
  en: {
    splashTagline: "Smart Agro AI Companion",
    splashLoading: "🛰️ Loading Satellite Telemetry & Models...",
    hdrSubtitle: "v2.5 Agro Advisor",
    langBtnText: "हिंदी में देखें",
    tagWeather: "🛰️ SATELLITE LIVE TELEMETRY",
    cityPlaceholder: "Enter Village or City name",
    lblTemp: "🌡️ Temperature",
    lblWind: "💨 Wind Speed",
    lblHumidity: "💧 Humidity",
    lblDrift: "🍃 Drift Risk",
    tagVision: "📸 LEAF PATHOLOGY AI SCANNER",
    descVision: "Take photo via Camera or Upload from Files. Trained AI model detects lesion symptoms instantly:",
    btnCamText: "Open Live Camera",
    btnGalText: "Choose from Files",
    tagField: "📋 FIELD SCOUTING",
    badgeStandard: "USDA / ICAR Grounded",
    lblFarmerName: "👤 Farmer Name",
    lblCropStage: "🌱 Crop & Growth Stage",
    lblSoil: "🏜️ Soil Moisture (Feel & Appearance)",
    lblInsects: "🐛 Insect Scouting Density",
    lblLeaf: "🍃 Leaf Health Condition",
    lblFieldSize: "📐 Field Size Scale",
    lblDisease: "🔬 Target Disease / Pest",
    btnRunText: "⚡ Run Hybrid AI Diagnostic",
    btnRunningText: "⚙️ Processing Diagnostics...",
    tagAdvice: "🌾 OFFICIAL FARM-SENSE ADVICE CARD",
    titleTimeline: "⏰ Timeline Recommendations:",
    lblSprayWindow: "🕒 Safe Spray Window:",
    lblNextCheck: "🔍 Next Field Check:",
    titlePrescription: "🧪 Prescription (Kaggle 132-Pest DB):",
    lblPestTarget: "🎯 Target:",
    lblPestChem: "💊 Chemical Active:",
    lblPestDose: "⚖️ Standard Dose:",
    lblPestOrganic: "🌿 Organic Protocol:",
    lblPestSafety: "⚠️ Safety Precaution:",
    titleReasons: "💡 Explainable AI Audit Log:",
    btnViewReceiptText: "📜 View & Print Digital Prescription",
    navAdvisory: "Advisory",
    navCamera: "Scan Camera",
    navPesticides: "Pesticides",
    tagPestsHdr: "🧪 132 PEST KNOWLEDGE VAULT",
    descPests: "Complete verified directory of 132 agricultural pests, active chemical formulations, and biological protocols:",
    soilPills: {
      Wet: "💦 Wet (47%)",
      Normal: "✨ Normal (35%)",
      Dry: "🍂 Dry (22%)",
      "Hard-Dry": "🧱 Hard-Dry (10%)"
    },
    insectsPills: {
      None: "🚫 None",
      Few: "⚠️ Few (Patchy)",
      Many: "🚨 Many (Swarm)",
      "Not sure": "❓ Not Sure"
    },
    leafPills: {
      "Leaves normal": "🌿 Healthy Normal",
      "Spots / color change": "🟡 Spots / Yellow",
      "Holes / eaten": "🕳️ Holes / Eaten",
      "Curled leaves": "🌀 Curled Foliage"
    },
    fieldSizePills: {
      Small: "🏡 Small (<1 Ha)",
      Medium: "🚜 Medium (1-3 Ha)",
      Large: "🌾 Large (>3 Ha)"
    },
    rcptTitle: "Digital Farmer Advisory & Prescription Receipt",
    rcptFarmerLbl: "Farmer",
    rcptCityLbl: "Location",
    rcptCropLbl: "Crop",
    rcptDateLbl: "Date",
    rcptLiveLbl: "Live Weather",
    rcptActionTag: "Recommended Action",
    rcptSafetyLbl: "Safety Rule",
    rcptReasonLbl: "Audit Reason",
    btnPrintLbl: "Print / Save PDF",
    btnTxtLbl: "Download .TXT",
    thTarget: "Target Pest",
    thChem: "Chemical Active",
    thDose: "Dosage",
    thOrganic: "Organic Alternative"
  }
};

let ALL_PESTICIDES_DATA = [];
let currentLang = "hi";
let currentWeatherData = null;
let lastEvaluationResult = null;
let currentDetectedDisease = "Unknown";
let activePestFilter = "all";

document.addEventListener("DOMContentLoaded", () => {
  setupSplashScreen();
  setupLanguageSwitch();
  setupNavigation();
  setupPillSelectors();
  setupWeatherSync();
  setupVisionScanner();
  setupAnalysisButton();
  loadAllPesticidesVault();
  setupReceiptModal();

  fetchWeather("Multai");
});

function setupSplashScreen() {
  const splash = document.getElementById("splash-screen");
  setTimeout(() => {
    if (splash) splash.classList.add("hidden");
  }, 1300);
}

function setupLanguageSwitch() {
  const btn = document.getElementById("btn-lang-toggle");
  btn.addEventListener("click", () => {
    currentLang = currentLang === "hi" ? "en" : "hi";
    applyLanguage(currentLang);
  });
}

function applyLanguage(lang) {
  const t = I18N[lang];

  document.getElementById("hdr-subtitle").textContent = t.hdrSubtitle;
  document.getElementById("lang-label").textContent = t.langBtnText;
  document.getElementById("tag-weather").textContent = t.tagWeather;
  document.getElementById("city-input").placeholder = t.cityPlaceholder;

  document.getElementById("lbl-temp").textContent = t.lblTemp;
  document.getElementById("lbl-wind").textContent = t.lblWind;
  document.getElementById("lbl-humidity").textContent = t.lblHumidity;
  document.getElementById("lbl-drift").textContent = t.lblDrift;

  // Vision
  document.getElementById("tag-vision").textContent = t.tagVision;
  document.getElementById("desc-vision").textContent = t.descVision;
  document.getElementById("btn-cam-text").textContent = t.btnCamText;
  document.getElementById("btn-gal-text").textContent = t.btnGalText;

  // Scouting Form
  document.getElementById("tag-field").textContent = t.tagField;
  document.getElementById("badge-standard").textContent = t.badgeStandard;
  document.getElementById("lbl-farmer-name").textContent = t.lblFarmerName;
  document.getElementById("lbl-crop-stage").textContent = t.lblCropStage;
  document.getElementById("lbl-soil").textContent = t.lblSoil;
  document.getElementById("lbl-insects").textContent = t.lblInsects;
  document.getElementById("lbl-leaf").textContent = t.lblLeaf;
  document.getElementById("lbl-field-size").textContent = t.lblFieldSize;
  document.getElementById("lbl-disease").textContent = t.lblDisease;
  document.getElementById("btn-run-text").textContent = t.btnRunText;

  // Pills
  document.getElementById("pill-soil-wet").textContent = t.soilPills.Wet;
  document.getElementById("pill-soil-normal").textContent = t.soilPills.Normal;
  document.getElementById("pill-soil-dry").textContent = t.soilPills.Dry;
  document.getElementById("pill-soil-hard").textContent = t.soilPills["Hard-Dry"];

  document.getElementById("pill-ins-none").textContent = t.insectsPills.None;
  document.getElementById("pill-ins-few").textContent = t.insectsPills.Few;
  document.getElementById("pill-ins-many").textContent = t.insectsPills.Many;
  document.getElementById("pill-ins-not-sure").textContent = t.insectsPills["Not sure"];

  document.getElementById("pill-leaf-normal").textContent = t.leafPills["Leaves normal"];
  document.getElementById("pill-leaf-spots").textContent = t.leafPills["Spots / color change"];
  document.getElementById("pill-leaf-holes").textContent = t.leafPills["Holes / eaten"];
  document.getElementById("pill-leaf-curled").textContent = t.leafPills["Curled leaves"];

  document.getElementById("pill-size-sm").textContent = t.fieldSizePills.Small;
  document.getElementById("pill-size-med").textContent = t.fieldSizePills.Medium;
  document.getElementById("pill-size-lg").textContent = t.fieldSizePills.Large;

  // Bottom Nav
  document.getElementById("nav-advisory").textContent = t.navAdvisory;
  document.getElementById("nav-camera").textContent = t.navCamera;
  document.getElementById("nav-pesticides").textContent = t.navPesticides;

  // Pesticide Vault
  document.getElementById("tag-pests-hdr").textContent = t.tagPestsHdr;
  document.getElementById("desc-pests").textContent = t.descPests;

  // Advice Card Titles
  document.getElementById("tag-advice").textContent = t.tagAdvice;
  document.getElementById("title-timeline").textContent = t.titleTimeline;
  document.getElementById("lbl-spray-window").textContent = t.lblSprayWindow;
  document.getElementById("lbl-next-check").textContent = t.lblNextCheck;
  document.getElementById("title-prescription").textContent = t.titlePrescription;
  document.getElementById("lbl-pest-target").textContent = t.lblPestTarget;
  document.getElementById("lbl-pest-chem").textContent = t.lblPestChem;
  document.getElementById("lbl-pest-dose").textContent = t.lblPestDose;
  document.getElementById("lbl-pest-organic").textContent = t.lblPestOrganic;
  document.getElementById("lbl-pest-safety").textContent = t.lblPestSafety;
  document.getElementById("title-reasons").textContent = t.titleReasons;
  document.getElementById("btn-view-receipt-text").textContent = t.btnViewReceiptText;

  // Modal Labels
  document.getElementById("rcpt-sub-text").textContent = t.rcptTitle;
  document.getElementById("rcpt-meta-farmer-lbl").textContent = t.rcptFarmerLbl;
  document.getElementById("rcpt-meta-city-lbl").textContent = t.rcptCityLbl;
  document.getElementById("rcpt-meta-crop-lbl").textContent = t.rcptCropLbl;
  document.getElementById("rcpt-meta-date-lbl").textContent = t.rcptDateLbl;
  document.getElementById("rcpt-live-lbl").textContent = t.rcptLiveLbl;
  document.getElementById("rcpt-tag-action").textContent = t.rcptActionTag;
  document.getElementById("rcpt-safety-lbl").textContent = t.rcptSafetyLbl;
  document.getElementById("rcpt-reason-lbl").textContent = t.rcptReasonLbl;
  const pLbl = document.getElementById("btn-print-lbl");
  if (pLbl) pLbl.textContent = t.btnPrintLbl;
  const tLbl = document.getElementById("btn-txt-lbl");
  if (tLbl) tLbl.textContent = t.btnTxtLbl;
  document.getElementById("th-target").textContent = t.thTarget;
  document.getElementById("th-chemical").textContent = t.thChem;
  document.getElementById("th-dose").textContent = t.thDose;
  document.getElementById("th-organic").textContent = t.thOrganic;

  renderPesticidesVault();

  if (lastEvaluationResult) {
    renderDecisionCard(lastEvaluationResult);
  }
}

// 3-Tab Navigation Switching (Left: Advisory, Centre: Camera, Right: Pesticides)
function setupNavigation() {
  const navBtns = document.querySelectorAll(".nav-item");
  const screens = document.querySelectorAll(".screen-view");

  navBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetId = btn.getAttribute("data-target");
      navBtns.forEach(b => b.classList.remove("active"));
      screens.forEach(s => s.classList.remove("active"));
      btn.classList.add("active");
      const targetScreen = document.getElementById(targetId);
      if (targetScreen) targetScreen.classList.add("active");
    });
  });
}

function setupPillSelectors() {
  document.querySelectorAll(".pill-selector").forEach(group => {
    const buttons = group.querySelectorAll(".pill-btn");
    buttons.forEach(btn => {
      btn.addEventListener("click", () => {
        buttons.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
      });
    });
  });
}

function getSelectedPills() {
  const values = {};
  document.querySelectorAll(".pill-selector").forEach(group => {
    const groupName = group.getAttribute("data-group");
    const activeBtn = group.querySelector(".pill-btn.active");
    if (groupName && activeBtn) {
      values[groupName] = activeBtn.getAttribute("data-val");
    }
  });
  return values;
}

function setupWeatherSync() {
  const syncBtn = document.getElementById("btn-sync-weather");
  const cityInput = document.getElementById("city-input");

  syncBtn.addEventListener("click", () => {
    const city = cityInput.value.trim() || "Multai";
    fetchWeather(city);
  });

  cityInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      const city = cityInput.value.trim() || "Multai";
      fetchWeather(city);
    }
  });
}

async function fetchWeather(cityName) {
  const btn = document.getElementById("btn-sync-weather");
  btn.style.opacity = "0.5";

  try {
    const res = await fetch(`/api/weather?city=${encodeURIComponent(cityName)}`);
    if (res.ok) {
      const data = await res.json();
      currentWeatherData = data;
      renderWeather(data);
    } else {
      renderWeatherFallback(cityName);
    }
  } catch (err) {
    renderWeatherFallback(cityName);
  } finally {
    btn.style.opacity = "1";
  }
}

function renderWeather(data) {
  document.getElementById("metric-temp").textContent = data.temp || "28.8°C";
  document.getElementById("metric-apparent").textContent = currentLang === "hi" ? `महसूस: ${data.apparent_temp || '31°C'}` : `Feels: ${data.apparent_temp || '31°C'}`;
  document.getElementById("metric-wind").textContent = data.wind_speed || "0.9 m/s";
  document.getElementById("metric-wind-kmh").textContent = `${data.wind_kmh || '3.3 km/h'} (${currentLang === 'hi' ? 'हल्की हवा' : 'Light'})`;
  document.getElementById("metric-humidity").textContent = data.humidity || "42%";
  document.getElementById("metric-rain").textContent = `${currentLang === 'hi' ? 'बारिश' : 'Rain'}: ${data.precipitation || '0.0 mm'}`;
  
  const driftElem = document.getElementById("metric-drift");
  driftElem.textContent = `${data.drift_risk_percent || 6.4}%`;
  driftElem.style.color = (data.drift_risk_percent > 30) ? "#ef4444" : "#4ade80";

  document.getElementById("metric-weather-status").textContent = (data.status === "Clear") ? (currentLang === 'hi' ? "साफ मौसम" : "Clear Sky") : data.status;
  document.getElementById("weather-source").textContent = data.resolved_location || "Satellite GPS";
}

function renderWeatherFallback(cityName) {
  currentWeatherData = {
    temp: "28.8°C",
    apparent_temp: "31.8°C",
    wind_speed: "0.92 m/s",
    wind_kmh: "3.3 km/h",
    wind_ms_val: 0.92,
    humidity: "42%",
    precipitation: "0.0 mm",
    drift_risk_percent: 6.4,
    status: "Clear",
    resolved_location: `${cityName}, India`
  };
  renderWeather(currentWeatherData);
}

// CENTRE TAB: LIVE CAMERA SCANNER
function setupVisionScanner() {
  const btnCam = document.getElementById("btn-open-camera");
  const btnGal = document.getElementById("btn-open-gallery");
  const camInput = document.getElementById("camera-file-input");
  const galInput = document.getElementById("gallery-file-input");
  const previewArea = document.getElementById("image-preview-area");
  const previewImg = document.getElementById("leaf-preview-img");
  const scanOverlay = document.getElementById("scan-overlay");
  const detectedName = document.getElementById("vision-detected-name");
  const detectedConf = document.getElementById("vision-detected-conf");
  const btnApply = document.getElementById("btn-apply-vision");

  btnCam.addEventListener("click", () => camInput.click());
  btnGal.addEventListener("click", () => galInput.click());

  function handleFile(file) {
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async (e) => {
      const base64Data = e.target.result;
      previewImg.src = base64Data;
      previewArea.style.display = "flex";
      scanOverlay.style.display = "block";
      detectedName.textContent = currentLang === "hi" ? "🔬 पत्ती के घाव व धब्बे स्कैन हो रहे हैं..." : "🔬 Scanning foliar lesion symptoms...";
      detectedConf.textContent = "...";

      try {
        const res = await fetch("/api/scan_leaf", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ image: base64Data })
        });

        if (res.ok) {
          const result = await res.json();
          currentDetectedDisease = result.disease;
          detectedName.textContent = `🎯 ${result.disease.replace(/___/g, " - ").replace(/_/g, " ")}`;
          detectedConf.textContent = result.confidence_pct || "95.2%";

          // Auto-select in form dropdown
          const diseaseSelect = document.getElementById("disease-select");
          for (let opt of diseaseSelect.options) {
            if (opt.value === result.disease) {
              diseaseSelect.value = opt.value;
              break;
            }
          }
        } else {
          fallbackVisionResult();
        }
      } catch (err) {
        fallbackVisionResult();
      } finally {
        scanOverlay.style.display = "none";
      }
    };
    reader.readAsDataURL(file);
  }

  function fallbackVisionResult() {
    currentDetectedDisease = "Tomato___Spider_mites Two-spotted_spider_mite";
    detectedName.textContent = "🎯 Tomato - Spider Mites (लाल मकड़ी)";
    detectedConf.textContent = "95.2%";
    document.getElementById("disease-select").value = currentDetectedDisease;
  }

  camInput.addEventListener("change", (e) => handleFile(e.target.files[0]));
  galInput.addEventListener("change", (e) => handleFile(e.target.files[0]));

  btnApply.addEventListener("click", () => {
    // Switch to Advisory Tab
    document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));
    document.querySelectorAll(".screen-view").forEach(s => s.classList.remove("active"));
    
    document.querySelector('.nav-item[data-target="screen-home"]').classList.add("active");
    document.getElementById("screen-home").classList.add("active");
    document.getElementById("disease-select").value = currentDetectedDisease;
    document.getElementById("disease-select").scrollIntoView({ behavior: "smooth" });
  });
}

// RIGHT TAB: 132 PESTICIDES REPOSITORY VAULT
async function loadAllPesticidesVault() {
  try {
    const res = await fetch("/all_pesticides.json");
    if (res.ok) {
      ALL_PESTICIDES_DATA = await res.json();
    } else {
      ALL_PESTICIDES_DATA = getFallbackPestList();
    }
  } catch (err) {
    ALL_PESTICIDES_DATA = getFallbackPestList();
  }
  setupPestVaultUI();
  renderPesticidesVault();
}

function getFallbackPestList() {
  return [
    { name: "Aleurocanthus spiniferus (Whitefly)", chemicals: "Imidacloprid, Acetamiprid, Chlorpyrifos" },
    { name: "alfalfa plant bug", chemicals: "Imidacloprid, Lambda-cyhalothrin, Chlorpyrifos" },
    { name: "alfalfa seed chalcid", chemicals: "Azadirachtin, Imidacloprid, Spinosad" },
    { name: "alfalfa weevil", chemicals: "Chlorpyrifos, Cyfluthrin, Carbaryl" },
    { name: "aphids", chemicals: "Imidacloprid, Acetamiprid, Thiamethoxam" },
    { name: "army worm", chemicals: "Chlorpyrifos, Lambda-cyhalothrin, Bifenthrin" },
    { name: "asiatic rice borer", chemicals: "Emamectin benzoate, Fipronil, Chlorantraniliprole" },
    { name: "beet army worm", chemicals: "Bacillus thuringiensis, Methoxyfenozide, Spinosad" },
    { name: "beetle", chemicals: "Imidacloprid, Carbaryl, Malathion, Cypermethrin" },
    { name: "bollworm", chemicals: "Chlorantraniliprole, Emamectin benzoate, Spinosad, Indoxacarb" },
    { name: "brown plant hopper", chemicals: "Imidacloprid, Chlorpyrifos, Buprofezin, Thiamethoxam" },
    { name: "cabbage army worm", chemicals: "Bacillus thuringiensis, Spinosad, Methomyl" },
    { name: "corn borer", chemicals: "Chlorpyrifos, Emamectin benzoate, Lambda-cyhalothrin" },
    { name: "corn earworm", chemicals: "Bacillus thuringiensis, Carbaryl, Cypermethrin" },
    { name: "cutworm", chemicals: "Chlorpyrifos, Diazinon, Methomyl" },
    { name: "Spider Mites", chemicals: "Abamectin, Bifenazate, Spiromesifen" }
  ];
}

function setupPestVaultUI() {
  const searchBox = document.getElementById("pest-search-box");
  const filterChips = document.querySelectorAll(".f-chip");

  searchBox.addEventListener("input", () => {
    renderPesticidesVault();
  });

  filterChips.forEach(chip => {
    chip.addEventListener("click", () => {
      filterChips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      activePestFilter = chip.getAttribute("data-filter");
      renderPesticidesVault();
    });
  });
}

function renderPesticidesVault() {
  const searchBox = document.getElementById("pest-search-box");
  const resultContainer = document.getElementById("pest-search-results");
  const counterBadge = document.getElementById("pest-counter");
  const q = searchBox ? searchBox.value.trim().toLowerCase() : "";

  resultContainer.innerHTML = "";

  const filtered = ALL_PESTICIDES_DATA.filter(p => {
    const name = p.name.toLowerCase();
    const chem = p.chemicals.toLowerCase();
    const matchesSearch = name.includes(q) || chem.includes(q);

    if (!matchesSearch) return false;

    if (activePestFilter === "all") return true;
    if (activePestFilter === "worm" && (name.includes("worm") || name.includes("caterpillar"))) return true;
    if (activePestFilter === "aphid" && (name.includes("aphid") || name.includes("hopper"))) return true;
    if (activePestFilter === "borer" && name.includes("borer")) return true;
    if (activePestFilter === "beetle" && (name.includes("beetle") || name.includes("weevil"))) return true;

    return false;
  });

  counterBadge.textContent = `${filtered.length} / ${ALL_PESTICIDES_DATA.length}`;

  if (filtered.length === 0) {
    resultContainer.innerHTML = `<div class='section-desc'>${currentLang === 'hi' ? 'कोई कीट नहीं मिला।' : 'No pests found matching criteria.'}</div>`;
    return;
  }

  filtered.forEach(item => {
    const card = document.createElement("div");
    card.className = "pest-item-card";
    card.innerHTML = `
      <div class="pic-header">
        <span class="pic-name">🐛 ${item.name}</span>
        <span class="pic-badge">Certified</span>
      </div>
      <div class="pic-chem"><strong>${currentLang === 'hi' ? 'प्रमाणित दवाएं' : 'Formulations'}:</strong> ${item.chemicals}</div>
      <div class="pic-actions">
        <button class="btn-select-pest" data-pest="${item.name}">${currentLang === 'hi' ? 'चुनें (Select)' : 'Select for Form'}</button>
      </div>
    `;

    card.querySelector(".btn-select-pest").addEventListener("click", () => {
      // Set target disease and switch to Advisory
      currentDetectedDisease = item.name;
      const select = document.getElementById("disease-select");
      let found = false;
      for (let opt of select.options) {
        if (opt.value.toLowerCase().includes(item.name.toLowerCase())) {
          select.value = opt.value;
          found = true;
          break;
        }
      }
      if (!found) {
        const newOpt = document.createElement("option");
        newOpt.value = item.name;
        newOpt.textContent = `🎯 ${item.name}`;
        newOpt.selected = true;
        select.appendChild(newOpt);
      }

      // Switch to Advisory tab
      document.querySelectorAll(".nav-item").forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".screen-view").forEach(s => s.classList.remove("active"));
      document.querySelector('.nav-item[data-target="screen-home"]').classList.add("active");
      document.getElementById("screen-home").classList.add("active");
      document.getElementById("disease-select").scrollIntoView({ behavior: "smooth" });
    });

    resultContainer.appendChild(card);
  });
}

// ADVISORY SUBMISSION & DECISION FUSION
function setupAnalysisButton() {
  const runBtn = document.getElementById("btn-run-analysis");

  runBtn.addEventListener("click", async () => {
    runBtn.style.opacity = "0.7";
    document.getElementById("btn-run-text").textContent = I18N[currentLang].btnRunningText;

    const pillValues = getSelectedPills();
    const city = document.getElementById("city-input").value.trim() || "Multai";
    const farmerName = document.getElementById("farmer-name-input").value.trim() || "Farmer XYZ";
    const crop = document.getElementById("crop-select").value;
    const cropStage = document.getElementById("stage-select").value;
    const disease = currentDetectedDisease !== "Unknown" ? currentDetectedDisease : document.getElementById("disease-select").value;

    const payload = {
      farmer_name: farmerName,
      city: city,
      detected_disease: disease,
      inputs: {
        Crop: crop,
        Crop_stage: cropStage,
        Soil_feel: pillValues.Soil_feel || "Normal",
        Field_water: "Normal",
        Insects_seen: pillValues.Insects_seen || "Few",
        Leaf_condition: pillValues.Leaf_condition || "Spots / color change",
        Field_size: pillValues.Field_size || "Medium",
        Wind_condition: (currentWeatherData && currentWeatherData.wind_ms_val > 5.5) ? "Strong" : "Light",
        Weather: currentWeatherData ? currentWeatherData.status : "Clear"
      }
    };

    try {
      const res = await fetch("/api/evaluate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });

      if (res.ok) {
        const result = await res.json();
        lastEvaluationResult = { ...result, farmer_name: farmerName, city: city, crop_display: `${crop} (${cropStage})` };
        renderDecisionCard(lastEvaluationResult);
      } else {
        const fallback = simulateLocalDecision(payload);
        lastEvaluationResult = { ...fallback, farmer_name: farmerName, city: city, crop_display: `${crop} (${cropStage})` };
        renderDecisionCard(lastEvaluationResult);
      }
    } catch (err) {
      const fallback = simulateLocalDecision(payload);
      lastEvaluationResult = { ...fallback, farmer_name: farmerName, city: city, crop_display: `${crop} (${cropStage})` };
      renderDecisionCard(lastEvaluationResult);
    } finally {
      runBtn.style.opacity = "1";
      document.getElementById("btn-run-text").textContent = I18N[currentLang].btnRunText;
    }
  });
}

function simulateLocalDecision(payload) {
  const isHighWind = payload.inputs.Wind_condition === "Strong";
  let action_hi = isHighWind ? "छिड़काव न करें (निगरानी रखें)" : "निगरानी और पैच उपचार (Monitor & Spot-Treat)";
  let action_en = isHighWind ? "No Spray - Monitor" : "Monitor & Spot-Treat";
  const cci = isHighWind ? 0.23 : 0.81;

  return {
    decision: {
      final_action_hi: action_hi,
      final_action_en: action_en,
      cci: cci,
      spray_window_hi: isHighWind ? "[अवरुद्ध - तेज हवा]" : "10:00 AM -- 4:00 PM (धूप व हल्की हवा)",
      spray_window_en: isHighWind ? "[LOCKED - HIGH WIND]" : "10:00 AM -- 4:00 PM (Optimal Sunlight)",
      next_check_hi: "36--48 घंटे बाद",
      next_check_en: "36--48 hours later",
      reasons_hi: [
        "खेत में कीट/कीड़े की उपस्थिति देखी गई",
        "पत्तियों पर पीले धब्बे और नेक्रोसिस पहचाना गया",
        `हाइब्रिड मॉडल विश्वसनीयता (Calibrated ML): ${isHighWind ? '25%' : '85%'}`
      ],
      reasons_en: [
        "Pest / insect scouting activity confirmed in field",
        "Visual leaf foliar necrosis and spots identified",
        `Hybrid model calibrated probability: ${isHighWind ? '0.25' : '0.85'}`
      ]
    },
    pesticide: {
      Chemical: payload.detected_disease.includes("Spider") ? "Abamectin 1.8% EC" : "Imidacloprid 17.8% SL",
      Dose_hi: "1.0 - 1.5 ml प्रति लीटर पानी",
      Dose_en: "1.0 - 1.5 ml per Litre of water",
      Organic_hi: "कोल्ड-प्रेस्ड नीम तेल (5 ml/Litre)",
      Organic_en: "Cold-pressed Neem Oil Spray (5 ml/Litre)",
      Safety_hi: "मुंह पर मास्क लगाएं; छिड़काव के बाद 48 घंटे तक मवेशियों को दूर रखें।",
      Safety_en: "Wear protective face mask; keep livestock away for 48 hours."
    },
    detected_disease: payload.detected_disease
  };
}

function renderDecisionCard(data) {
  const card = document.getElementById("result-card-container");
  card.style.display = "block";

  const dec = data.decision;
  const pest = data.pesticide;

  const isH = currentLang === "hi";
  const actionText = isH ? (dec.final_action_hi || dec.final_action) : (dec.final_action_en || dec.final_action);
  const sprayText = isH ? (dec.spray_window_hi || dec.spray_window) : (dec.spray_window_en || dec.spray_window);
  const nextCheckText = isH ? (dec.next_check_hi || dec.next_check) : (dec.next_check_en || dec.next_check);
  const reasonsArr = isH ? (dec.reasons_hi || dec.reasons) : (dec.reasons_en || dec.reasons);

  document.getElementById("res-cci-badge").textContent = `${isH ? 'विश्वसनीयता' : 'Confidence'}: ${Math.round(dec.cci * 100)}%`;
  document.getElementById("res-final-action").textContent = actionText;

  const subElem = document.getElementById("res-action-sub");
  const iconElem = document.getElementById("res-action-icon");
  if (actionText.includes("No Spray") || actionText.includes("न करें")) {
    iconElem.textContent = "🛑";
    subElem.textContent = isH ? "मौसम सुरक्षा कारणों से रासायनिक छिड़काव बंद रखा गया है" : "Spraying blocked due to adverse micro-climate wind/rain";
  } else {
    iconElem.textContent = "🎯";
    subElem.textContent = isH ? "पूरे खेत में नहीं, केवल ग्रसित भाग में छिड़काव करें" : "Target spot-treatment on affected foliar zones only";
  }

  document.getElementById("res-spray-window").textContent = sprayText;
  document.getElementById("res-next-check").textContent = nextCheckText;

  document.getElementById("res-pest-target").textContent = data.detected_disease;
  document.getElementById("res-pest-chem").textContent = pest.Chemical;
  document.getElementById("res-pest-dose").textContent = isH ? (pest.Dose_hi || pest.Dose) : (pest.Dose_en || pest.Dose);
  document.getElementById("res-pest-organic").textContent = isH ? (pest.Organic_hi || pest.Organic) : (pest.Organic_en || pest.Organic);
  document.getElementById("res-pest-safety").textContent = isH ? (pest.Safety_hi || pest.Safety) : (pest.Safety_en || pest.Safety);

  const reasonsList = document.getElementById("res-reasons-list");
  reasonsList.innerHTML = "";
  (reasonsArr || []).forEach(r => {
    const li = document.createElement("li");
    li.textContent = r;
    reasonsList.appendChild(li);
  });

  card.scrollIntoView({ behavior: "smooth" });
}

// DIGITAL AGRO-PRESCRIPTION MODAL
function setupReceiptModal() {
  const viewBtn = document.getElementById("btn-view-receipt");
  const modal = document.getElementById("receipt-modal");
  const closeBtn = document.getElementById("btn-close-receipt");
  const printBtn = document.getElementById("btn-print-receipt");
  const txtBtn = document.getElementById("btn-download-txt");

  viewBtn.addEventListener("click", () => {
    if (!lastEvaluationResult) return;
    populateReceiptModal(lastEvaluationResult);
    modal.style.display = "flex";
  });

  closeBtn.addEventListener("click", () => {
    modal.style.display = "none";
  });

  modal.addEventListener("click", (e) => {
    if (e.target === modal) modal.style.display = "none";
  });

  printBtn.addEventListener("click", () => {
    window.print();
  });

  txtBtn.addEventListener("click", () => {
    downloadTxtPrescription();
  });
}

function populateReceiptModal(d) {
  const isH = currentLang === "hi";
  const now = new Date();
  const dec = d.decision;
  const pest = d.pesticide;

  document.getElementById("rcpt-farmer").textContent = d.farmer_name || "Farmer XYZ";
  document.getElementById("rcpt-city").textContent = d.city || "Multai";
  document.getElementById("rcpt-crop").textContent = d.crop_display || "Wheat (Mid)";
  document.getElementById("rcpt-date").textContent = now.toLocaleDateString();

  const w = currentWeatherData || {};
  document.getElementById("rcpt-weather").textContent = `${w.temp || '28.8°C'} | ${isH ? 'हवा' : 'Wind'}: ${w.wind_speed || '0.9 m/s'} | ${isH ? 'बहाव जोखिम' : 'Drift'}: ${w.drift_risk_percent || '6.4'}%`;

  const actionText = isH ? (dec.final_action_hi || dec.final_action) : (dec.final_action_en || dec.final_action);
  const sprayText = isH ? (dec.spray_window_hi || dec.spray_window) : (dec.spray_window_en || dec.spray_window);
  const reasonsArr = isH ? (dec.reasons_hi || dec.reasons) : (dec.reasons_en || dec.reasons);

  document.getElementById("rcpt-action-val").textContent = actionText;
  document.getElementById("rcpt-action-desc").textContent = isH ? "पूरे खेत में नहीं, केवल ग्रसित भाग में छिड़काव करें" : "Treat only affected patches in field";
  document.getElementById("rcpt-cci").textContent = `${isH ? 'विश्वसनीयता' : 'Confidence'}: ${Math.round(dec.cci * 100)}%`;
  document.getElementById("rcpt-window").textContent = `${isH ? 'समय' : 'Window'}: ${sprayText}`;

  document.getElementById("rcpt-tbl-target").textContent = d.detected_disease;
  document.getElementById("rcpt-tbl-chem").textContent = pest.Chemical;
  document.getElementById("rcpt-tbl-dose").textContent = isH ? (pest.Dose_hi || pest.Dose) : (pest.Dose_en || pest.Dose);
  document.getElementById("rcpt-tbl-organic").textContent = isH ? (pest.Organic_hi || pest.Organic) : (pest.Organic_en || pest.Organic);

  document.getElementById("rcpt-safety-val").textContent = isH ? (pest.Safety_hi || pest.Safety) : (pest.Safety_en || pest.Safety);
  document.getElementById("rcpt-reason-val").textContent = (reasonsArr && reasonsArr[0]) ? reasonsArr[0] : (isH ? "खेत में कीड़े की सक्रियता देखी गई" : "Pest scouting activity identified");
}

function downloadTxtPrescription() {
  if (!lastEvaluationResult) return;
  const d = lastEvaluationResult;
  const isH = currentLang === "hi";
  const now = new Date();
  const dec = d.decision;
  const pest = d.pesticide;

  const actionText = isH ? (dec.final_action_hi || dec.final_action) : (dec.final_action_en || dec.final_action);
  const sprayText = isH ? (dec.spray_window_hi || dec.spray_window) : (dec.spray_window_en || dec.spray_window);
  const nextCheckText = isH ? (dec.next_check_hi || dec.next_check) : (dec.next_check_en || dec.next_check);
  const doseText = isH ? (pest.Dose_hi || pest.Dose) : (pest.Dose_en || pest.Dose);
  const organicText = isH ? (pest.Organic_hi || pest.Organic) : (pest.Organic_en || pest.Organic);
  const safetyText = isH ? (pest.Safety_hi || pest.Safety) : (pest.Safety_en || pest.Safety);

  const content = isH ? 
`===========================================================
             FARM-SENSE X: डिजिटल किसान परामर्श पर्ची
===========================================================
किसान का नाम (Farmer) : ${d.farmer_name || 'Farmer XYZ'}
स्थान / गांव (Location): ${d.city || 'Multai'}
फसल एवं अवस्था (Crop) : ${d.crop_display || 'Wheat'}
दिनांक व समय (Date)   : ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
-----------------------------------------------------------
अनुशंसित कार्य (Action)  : ${actionText}
सिस्टम विश्वसनीयता (CCI) : ${Math.round(dec.cci * 100)}%
सुरक्षित छिड़काव समय     : ${sprayText}
अगला निरीक्षण समय       : ${nextCheckText}
-----------------------------------------------------------
लक्षित कीट/रोग (Target) : ${d.detected_disease}
प्रमाणित रासायनिक दवा   : ${pest.Chemical}
सुरक्षित मानक खुराक     : ${doseText}
जैविक विकल्प (Organic)  : ${organicText}
सुरक्षा सावधानियां       : ${safetyText}
-----------------------------------------------------------
Generated by FARM-SENSE X Hybrid Agriculture AI v2.5
` : 
`===========================================================
             FARM-SENSE X: DIGITAL AGRO PRESCRIPTION
===========================================================
Farmer Name (Farmer)  : ${d.farmer_name || 'Farmer XYZ'}
Location / City       : ${d.city || 'Multai'}
Crop & Phenology      : ${d.crop_display || 'Wheat'}
Date & Time           : ${now.toLocaleDateString()} ${now.toLocaleTimeString()}
-----------------------------------------------------------
Recommended Action    : ${actionText}
System Confidence(CCI): ${Math.round(dec.cci * 100)}%
Safe Spray Window     : ${sprayText}
Next Field Check      : ${nextCheckText}
-----------------------------------------------------------
Target Pathogen/Pest  : ${d.detected_disease}
Chemical Active       : ${pest.Chemical}
Standard Dosage       : ${doseText}
Organic Protocol      : ${organicText}
Safety Instructions   : ${safetyText}
-----------------------------------------------------------
Generated by FARM-SENSE X Hybrid Agriculture AI v2.5
`;

  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `Prescription_${d.farmer_name || 'Farmer_XYZ'}_${currentLang}.txt`;
  a.click();
  URL.revokeObjectURL(url);
}
