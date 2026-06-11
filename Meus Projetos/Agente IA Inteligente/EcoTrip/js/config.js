const CONFIG = {
  EMISSION_FACTORS: {
    bicycle: 0,
    car: 0.12,
    bus: 0.098,
    truck: 0.96
  },

  TRANSPORT_MODES: {
    bicycle: { label: "Bicicleta", icon: "🚴", color: "#10b981" },
    car:     { label: "Carro",     icon: "🚗", color: "#059669" },
    bus:     { label: "Ônibus",    icon: "🚌", color: "#3b82f6" },
    truck:   { label: "Caminhão",  icon: "🚚", color: "#f59e0b" }
  },

  CARBON_CREDIT: {
    KG_PER_CREDIT: 1000,
    PRICE_MIN_BRL: 50,
    PRICE_MAX_BRL: 150
  },

  populateDatalist: function () {
    if (typeof RoutesDB === "undefined" || typeof RoutesDB.getAllCities !== "function") {
      console.error("❌ populateDatalist: RoutesDB não encontrado.");
      return;
    }

    const datalist = document.getElementById("cities-list");
    if (!datalist) {
      console.error("❌ populateDatalist: elemento #cities-list não encontrado no DOM.");
      return;
    }

    const cities = RoutesDB.getAllCities();
    datalist.innerHTML = "";
    cities.forEach(function (city) {
      const option = document.createElement("option");
      option.value = city;
      datalist.appendChild(option);
    });

    console.log("✅ populateDatalist: " + cities.length + " cidades carregadas.");
  },

  setupDistanceAutofill: function () {
    const originInput      = document.getElementById("origin");
    const destinationInput = document.getElementById("destination");
    const distanceInput    = document.getElementById("distance");
    const manualCheckbox   = document.getElementById("manual-distance");
    let helperText = null;

    if (!originInput || !destinationInput || !distanceInput || !manualCheckbox) {
      return;
    }

    const distanceGroup = distanceInput.closest(".form__group");
    if (distanceGroup) {
      helperText = distanceGroup.querySelector(".form__help");
    }

    function updateHelper(text, color) {
      if (helperText) {
        helperText.textContent = text;
        helperText.style.color = color || "var(--text-light)";
      }
    }

    function tryAutofillDistance() {
      const originValue      = originInput.value.trim();
      const destinationValue = destinationInput.value.trim();

      if (!originValue || !destinationValue) {
        distanceInput.value = "";
        distanceInput.readOnly = true;
        updateHelper("A distância será preenchida automaticamente", "var(--text-light)");
        return;
      }

      if (manualCheckbox.checked) {
        distanceInput.readOnly = false;
        updateHelper("Você pode inserir a distância manualmente", "var(--text-light)");
        return;
      }

      let distance = null;
      if (typeof RoutesDB !== "undefined" && typeof RoutesDB.findDistance === "function") {
        distance = RoutesDB.findDistance(originValue, destinationValue);
      }

      if (distance !== null) {
        distanceInput.value = distance;
        distanceInput.readOnly = true;
        updateHelper("Distância encontrada automaticamente", "#10b981");
      } else {
        distanceInput.value = "";
        distanceInput.readOnly = true;
        updateHelper("Rota não encontrada. Marque 'Inserir distância manualmente' para entrar com o valor.", "var(--danger)");
      }
    }

    // CORREÇÃO: adicionado "change" além de "input".
    // Quando o usuário clica numa opção do datalist, o browser dispara
    // o evento "change" — não "input". Sem esse listener, a função
    // rodava antes do valor final ser preenchido e não encontrava a rota.
    originInput.addEventListener("input",  tryAutofillDistance);
    originInput.addEventListener("change", tryAutofillDistance);
    destinationInput.addEventListener("input",  tryAutofillDistance);
    destinationInput.addEventListener("change", tryAutofillDistance);

    manualCheckbox.addEventListener("change", function () {
      if (manualCheckbox.checked) {
        distanceInput.readOnly = false;
        updateHelper("Você pode inserir a distância manualmente", "var(--text-light)");
      } else {
        tryAutofillDistance();
      }
    });

    tryAutofillDistance();
  }
};