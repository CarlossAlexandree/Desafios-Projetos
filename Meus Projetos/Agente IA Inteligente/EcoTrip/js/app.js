document.addEventListener("DOMContentLoaded", function () {

  // CORREÇÃO: todas as verificações trocadas de "window.VARIAVEL"
  // para "typeof VARIAVEL !== 'undefined'", pois variáveis declaradas
  // com const/let não ficam disponíveis no objeto window.

  if (typeof CONFIG !== "undefined" && typeof CONFIG.populateDatalist === "function") {
    CONFIG.populateDatalist();
  }

  if (typeof CONFIG !== "undefined" && typeof CONFIG.setupDistanceAutofill === "function") {
    CONFIG.setupDistanceAutofill();
  }

  const calculatorForm = document.getElementById("calculator-form");
  if (calculatorForm) {
    calculatorForm.addEventListener("submit", handleFormSubmit);
  }

  console.log("✅ Calculadora inicializada!");

  function handleFormSubmit(event) {
    event.preventDefault();

    const origin        = document.getElementById('origin').value.trim();
    const destination   = document.getElementById('destination').value.trim();
    const distanceInput = document.getElementById('distance').value;
    const distance      = parseFloat(distanceInput);

    const transportModeInput = document.querySelector('input[name="transport"]:checked');
    const transportMode      = transportModeInput ? transportModeInput.value : null;

    if (!origin || !destination) {
      alert('❌ Por favor, preencha a origem e o destino.');
      return;
    }

    if (!distance || distance <= 0) {
      alert('❌ Por favor, insira uma distância válida maior que zero.');
      return;
    }

    if (!transportMode) {
      alert('❌ Por favor, selecione um meio de transporte.');
      return;
    }

    const submitButton = calculatorForm.querySelector('button[type="submit"]');

    if (typeof UI !== "undefined" && typeof UI.showLoading === "function") {
      UI.showLoading(submitButton);
    }

    if (typeof UI !== "undefined" && typeof UI.hideElement === "function") {
      UI.hideElement("results");
      UI.hideElement("comparison");
      UI.hideElement("carbon-credits");
    }

    setTimeout(function () {
      try {
        if (typeof Calculator === "undefined" || typeof UI === "undefined") {
          throw new Error("Módulos necessários (Calculator ou UI) não foram encontrados.");
        }

        const selectedModeEmission       = Calculator.calculateEmission(distance, transportMode);
        const carBaselineEmission        = Calculator.calculateEmission(distance, "car");
        const savingsData                = Calculator.calculateSavings(selectedModeEmission, carBaselineEmission);
        const allModesComparisonArray    = Calculator.calculateAllModes(distance);
        const calculatedCredits          = Calculator.calculateCarbonCredits(selectedModeEmission);
        const estimatedCreditPriceObject = Calculator.estimateCreditPrice(calculatedCredits);

        const resultsDataObject = {
          origin, destination, distance,
          emission: selectedModeEmission,
          mode: transportMode,
          savings: savingsData
        };

        const carbonCreditsDataObject = {
          credits: calculatedCredits,
          price: estimatedCreditPriceObject
        };

        const resultsContentDiv = document.getElementById("results-content");
        if (resultsContentDiv) {
          resultsContentDiv.innerHTML = UI.renderResults(resultsDataObject);
        }

        const comparisonContentDiv = document.getElementById("comparison-content");
        if (comparisonContentDiv) {
          comparisonContentDiv.innerHTML = UI.renderComparison(allModesComparisonArray, transportMode);
        }

        const carbonCreditsContentDiv = document.getElementById("carbon-credits-content");
        if (carbonCreditsContentDiv) {
          carbonCreditsContentDiv.innerHTML = UI.renderCarbonCredits(carbonCreditsDataObject);
        }

        UI.showElement("results");
        UI.showElement("comparison");
        UI.showElement("carbon-credits");
        UI.scrollToElement("results");
        UI.hideLoading(submitButton);

      } catch (error) {
        console.error("Erro durante o processamento:", error);
        alert("Ocorreu um erro ao processar os seus dados. Por favor, tente novamente.");
        if (typeof UI !== "undefined" && typeof UI.hideLoading === "function") {
          UI.hideLoading(submitButton);
        }
      }
    }, 1500);
  }
});