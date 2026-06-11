// Calculator is a global object for emissions and carbon credit calculations.
// All methods return values rounded to the required precision.
// CORREÇÃO: todas as verificações trocadas de "window.CONFIG" para
// "typeof CONFIG !== 'undefined'", pois const não fica disponível em window.
const Calculator = {

  calculateEmission: function (distanceKm, transportMode) {
    let factor = 0;

    if (typeof CONFIG !== "undefined" && CONFIG.EMISSION_FACTORS && typeof CONFIG.EMISSION_FACTORS[transportMode] === "number") {
      factor = CONFIG.EMISSION_FACTORS[transportMode];
    }

    const result = Number(distanceKm) * factor;
    return Number(result.toFixed(2));
  },

  calculateAllModes: function (distanceKm) {
    const results = [];
    let carEmission = this.calculateEmission(distanceKm, "car");

    if (carEmission === 0) {
      carEmission = 1;
    }

    if (typeof CONFIG !== "undefined" && CONFIG.EMISSION_FACTORS) {
      Object.keys(CONFIG.EMISSION_FACTORS).forEach(function (mode) {
        const emission = Calculator.calculateEmission(distanceKm, mode);
        const percentageVsCar = (emission / carEmission) * 100;

        results.push({
          mode: mode,
          emission: Number(emission.toFixed(2)),
          percentageVsCar: Number(percentageVsCar.toFixed(2))
        });
      });
    }

    results.sort(function (a, b) {
      return a.emission - b.emission;
    });

    return results;
  },

  calculateSavings: function (emission, baselineEmission) {
    const savedKg = Number(baselineEmission) - Number(emission);
    let percentage = 0;

    if (baselineEmission !== 0) {
      percentage = (savedKg / Number(baselineEmission)) * 100;
    }

    return {
      savedKg: Number(savedKg.toFixed(2)),
      percentage: Number(percentage.toFixed(2))
    };
  },

  calculateCarbonCredits: function (emissionKg) {
    let credits = 0;

    if (typeof CONFIG !== "undefined" && CONFIG.CARBON_CREDIT && CONFIG.CARBON_CREDIT.KG_PER_CREDIT) {
      credits = Number(emissionKg) / CONFIG.CARBON_CREDIT.KG_PER_CREDIT;
    }

    return Number(credits.toFixed(4));
  },

  estimateCreditPrice: function (credits) {
    let minPrice = 0;
    let maxPrice = 0;
    let averagePrice = 0;

    if (typeof CONFIG !== "undefined" && CONFIG.CARBON_CREDIT) {
      minPrice = Number(credits) * CONFIG.CARBON_CREDIT.PRICE_MIN_BRL;
      maxPrice = Number(credits) * CONFIG.CARBON_CREDIT.PRICE_MAX_BRL;
      averagePrice = (minPrice + maxPrice) / 2;
    }

    return {
      min: Number(minPrice.toFixed(2)),
      max: Number(maxPrice.toFixed(2)),
      average: Number(averagePrice.toFixed(2))
    };
  }
};