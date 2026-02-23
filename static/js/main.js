document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('#patient-form');
    const analyzeBtn = document.querySelector('#analyze-btn');
    const loading = document.querySelector('#loading');
    const emptyState = document.querySelector('#empty-state');
    const resultsState = document.querySelector('#results-state');
    const tumorSizeInput = document.querySelector('#tumor_size');
    const tumorSizeVal = document.querySelector('#tumor-size-val');

    const riskBadge = document.querySelector('#risk-badge');
    const riskPercentageText = document.querySelector('#risk-percentage-text');
    const riskProgress = document.querySelector('#risk-progress');
    const shapChartCanvas = document.querySelector('#shapChart');

    let shapChartInstance = null;

    // Range slider değeri güncelleme
    tumorSizeInput.addEventListener('input', (e) => {
        tumorSizeVal.textContent = parseFloat(e.target.value).toFixed(1);
    });

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Buton durumu
        analyzeBtn.classList.add('hidden');
        loading.classList.remove('hidden');

        // Form Verilerini Topla
        const patientData = {
            age: parseInt(document.querySelector('#age').value),
            sex: document.querySelector('#sex').value,
            stage: document.querySelector('#stage').value,
            tumor_size: parseFloat(document.querySelector('#tumor_size').value),
            lymph_n: document.querySelector('#lymph_n').value,
            smoking: document.querySelector('#smoking').value,
            alcohol: document.querySelector('#alcohol').value,
            hpv_status: document.querySelector('#hpv_status').checked
        };

        try {
            // API'ye İstek At (FastAPI aynı sunucuda olduğu için /api/predict kullanabiliriz)
            const response = await fetch('/api/predict', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(patientData)
            });

            if (!response.ok) {
                throw new Error("Sunucu ile iletişim kurulamadı.");
            }

            const data = await response.json();

            // Sonuçları Göster
            displayResults(data);

        } catch (error) {
            alert("Bir hata oluştu: " + error.message);
            console.error(error);
        } finally {
            // Buton durumunu geri al
            loading.classList.add('hidden');
            analyzeBtn.classList.remove('hidden');
        }
    });

    function displayResults(data) {
        // Ekran geçişleri
        emptyState.classList.add('hidden');
        resultsState.classList.remove('hidden');

        // Risk Metrikleri
        riskPercentageText.textContent = `%${data.risk_percentage}`;
        riskProgress.style.width = `${data.risk_percentage}%`;

        // Risk durumuna göre renk değişimi
        if (data.risk_score >= 0.5) {
            riskBadge.textContent = "Yüksek Risk Grubu";
            riskBadge.className = "badge badge-danger";
            riskProgress.style.background = "var(--red-500, #ef4444)";
        } else {
            riskBadge.textContent = "Düşük Risk Grubu";
            riskBadge.className = "badge badge-success";
            riskProgress.style.background = "var(--green-500, #10b981)";
        }

        // SHAP Grafiğini Çiz
        if (shapChartInstance) {
            shapChartInstance.destroy();
        }

        const features = data.shap_values.map(s => s.feature);
        const values = data.shap_values.map(s => s.value);

        // Değer pozitifse (riski artırır) KIRMIZI, negatifse (riski azaltır) MAVİ (TEAL uyumlu)
        const backgroundColors = values.map(v => v > 0 ? 'rgba(239, 68, 68, 0.85)' : 'rgba(34, 73, 90, 0.85)');
        const borderColors = values.map(v => v > 0 ? '#dc2626' : '#1A3642');

        shapChartInstance = new Chart(shapChartCanvas, {
            type: 'bar',
            data: {
                labels: features,
                datasets: [{
                    label: 'Etki Değeri',
                    data: values,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 1,
                    borderRadius: 4
                }]
            },
            options: {
                indexAxis: 'y', // Yatay bar
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function (context) {
                                let val = context.raw;
                                let effect = val > 0 ? 'Riski Artırır' : 'Riski Azaltır';
                                return `${effect} (${val.toFixed(2)})`;
                            }
                        }
                    }
                },
                scales: {
                    x: {
                        grid: {
                            color: 'rgba(0,0,0,0.05)'
                        }
                    },
                    y: {
                        grid: {
                            display: false
                        }
                    }
                }
            }
        });
    }
});
