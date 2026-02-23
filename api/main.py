import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="OPC Risk Model API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PatientData(BaseModel):
    age: int
    sex: str
    stage: str
    tumor_size: float
    lymph_n: str
    smoking: str
    alcohol: str
    hpv_status: bool

@app.post("/api/predict")
async def predict(data: PatientData):
    # Simüle edilmiş baz risk hesaplaması (Ensemble Model entegrasyonu buraya gelecek)
    base_risk = 0.20
    
    if data.stage in ["III", "IV"]: 
        base_risk += 0.25 if data.stage == "III" else 0.40
    if data.tumor_size > 4.0: 
        base_risk += 0.15
    if data.smoking == "İçmiyor": 
        base_risk -= 0.05
    else: 
        base_risk += 0.08
    if data.hpv_status: 
        base_risk -= 0.15
    if data.age > 65: 
        base_risk += 0.10
    if data.lymph_n == "Var (N+)": 
        base_risk += 0.10
        
    risk_score = min(max(base_risk, 0.01), 0.99)
    
    # SHAP Simülasyonu
    hpv_effect = -0.15 if data.hpv_status else 0.05
    stage_effect = 0.25 if data.stage in ["III", "IV"] else -0.05
    size_effect = 0.10 if data.tumor_size > 4.0 else -0.02
    lymph_effect = 0.08 if data.lymph_n == "Var (N+)" else -0.03
    age_effect = 0.05 if data.age > 60 else -0.02
    smoke_effect = -0.05 if data.smoking == "İçmiyor" else 0.08
    
    shap_values = [
        {"feature": "HPV Durumu", "value": hpv_effect},
        {"feature": "TNM Evresi", "value": stage_effect},
        {"feature": "Tümör Boyutu", "value": size_effect},
        {"feature": "Lenf Nodu", "value": lymph_effect},
        {"feature": "Yaş", "value": age_effect},
        {"feature": "Sigara", "value": smoke_effect}
    ]
    
    # Şimdilik risk durum açıklaması
    risk_level = "Yüksek Risk Grubu" if risk_score >= 0.5 else "Düşük Risk Grubu"
    
    return {
        "risk_score": risk_score,
        "risk_percentage": round(risk_score * 100, 1),
        "risk_level": risk_level,
        "shap_values": shap_values
    }

static_dir = os.path.join(os.path.dirname(__file__), "..", "static")
if os.path.exists(static_dir):
    app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
