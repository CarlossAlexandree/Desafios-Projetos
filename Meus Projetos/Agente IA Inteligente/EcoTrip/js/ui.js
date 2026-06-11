// Global UI object holding formatting utilities, rendering helpers, and loading state controls.
// Each render method returns an HTML string that can be inserted into the page.

const UI = {
  // =========================================================================
  // UTILITY METHODS
  // =========================================================================

  formatNumber: function(number, decimals) {
    let value = Number(number);
    if (Number.isNaN(value)) {
      value = 0;
    }
    // Use toFixed() for decimals
    if (decimals !== undefined) {
      value = Number(value.toFixed(decimals));
    }
    // Add thousand separators using toLocaleString('pt-BR')
    return value.toLocaleString("pt-BR", {
      minimumFractionDigits: decimals || 0,
      maximumFractionDigits: decimals || 0
    });
  },

  formatCurrency: function(value) {
    let amount = Number(value);
    if (Number.isNaN(amount)) {
      amount = 0;
    }
    // Format as R$ with pt-BR locale
    return amount.toLocaleString("pt-BR", {
      style: "currency",
      currency: "BRL"
    });
  },

  showElement: function(elementId) {
    // Get element by ID
    const element = document.getElementById(elementId);
    if (element) {
      // Remove 'hidden' class
      element.classList.remove("hidden");
    }
  },

  hideElement: function(elementId) {
    // Get element by ID
    const element = document.getElementById(elementId);
    if (element) {
      // Add 'hidden' class
      element.classList.add("hidden");
    }
  },

  scrollToElement: function(elementId) {
    // Get element by ID
    const element = document.getElementById(elementId);
    if (element) {
      // Use scrollIntoView with smooth behavior
      element.scrollIntoView({
        behavior: "smooth"
      });
    }
  },

  // =========================================================================
  // LOADING METHODS
  // =========================================================================

  showLoading: function(buttonElement) {
    if (buttonElement) {
      // Save original text in data attribute: buttonElement.dataset.originalText
      buttonElement.dataset.originalText = buttonElement.innerHTML;
      // Disable button
      buttonElement.disabled = true;
      // Change innerHTML to show spinner and "Calculando..." text
      buttonElement.innerHTML = '<span class="spinner"></span> Calculando...';
    }
  },

  hideLoading: function(buttonElement) {
    if (buttonElement) {
      // Enable button
      buttonElement.disabled = false;
      // Restore original text from data attribute
      buttonElement.innerHTML = buttonElement.dataset.originalText || "";
    }
  },

  // =========================================================================
  // RENDERING METHODS
  // =========================================================================

  renderResults: function(data) {
    // data object contains: origin, destination, distance, emission, mode, savings
    // Get mode metadata from CONFIG.TRANSPORT_MODES
    const modeMetadata = CONFIG.TRANSPORT_MODES[data.mode] || { icon: "🚗", label: data.mode };
    
    // CORREÇÃO: Utilizando o grid estruturado do CSS para envelopar e alinhar os quadros perfeitamente
    let html = `
      <div class="transport__grid">
        
        <div class="transport__option" style="cursor: default; transform: none; background: var(--white); box-shadow: var(--shadow-sm);">
          <span class="transport__icon">🗺️</span>
          <span class="transport__text">Rota</span>
          <p style="font-size: 0.95rem; margin-top: var(--spacing-xs); color: var(--text-light); font-weight: bold; word-break: break-word;">
            ${data.origin} ➔ ${data.destination}
          </p>
        </div>

        <div class="transport__option" style="cursor: default; transform: none; background: var(--white); box-shadow: var(--shadow-sm);">
          <span class="transport__icon">📏</span>
          <span class="transport__text">Distância</span>
          <p style="font-size: 1.25rem; margin-top: var(--spacing-xs); color: var(--primary); font-weight: bold;">
            ${this.formatNumber(data.distance, 0)} km
          </p>
        </div>

        <div class="transport__option" style="cursor: default; transform: none; background: var(--white); box-shadow: var(--shadow-sm);">
          <span class="transport__icon">🍃</span>
          <span class="transport__text">Emissão de CO₂</span>
          <p style="font-size: 1.25rem; margin-top: var(--spacing-xs); color: #111827; font-weight: bold;">
            ${this.formatNumber(data.emission, 2)} kg
          </p>
        </div>

        <div class="transport__option" style="cursor: default; transform: none; background: var(--white); box-shadow: var(--shadow-sm);">
          <span class="transport__icon">${modeMetadata.icon}</span>
          <span class="transport__text">Meio de Transporte</span>
          <p style="font-size: 1.25rem; margin-top: var(--spacing-xs); color: #111827; font-weight: bold;">
            ${modeMetadata.label}
          </p>
        </div>

      </div>
    `;

    // If mode is not 'car' and savings exist: savings card showing kg saved and percentage
    if (data.mode !== "car" && data.savings && (data.savings.savedKg > 0 || data.savings.kg > 0)) {
      const kgSaved = data.savings.savedKg !== undefined ? data.savings.savedKg : data.savings.kg;
      html += `
        <div class="results_card results_card--success" style="margin-top: var(--spacing-md); background: var(--white); padding: var(--spacing-md); border-radius: var(--radius-lg); box-shadow: var(--shadow-md); border-left: 5px solid var(--primary);">
          <h3 class="results_card__title" style="color: var(--primary); font-size: 1.1rem; font-weight: 700; margin-bottom: var(--spacing-xs);">💡 Economia Gerada</h3>
          <p class="results_card__value" style="font-size: 1rem; color: #111827;">
            Viajando de ${modeMetadata.label}, você evitou a emissão de <strong>${this.formatNumber(kgSaved, 2)} kg de CO₂</strong> (${data.savings.percentage}% mais eficiente do que ir de Carro).
          </p>
        </div>
      `;
    }

    // Return complete HTML string
    return html;
  },

  renderComparison: function(modesArray, selectedMode) {
    // Start HTML structure
    let html = `
      <h2 class="section-title">Comparação entre Meios de Transporte</h2>
      <div class="comparison_grid">
    `;

    // Find the maximum emission for progress bar scaling
    const maxEmission = Math.max(...modesArray.map(m => m.emission));

    // Render each transport mode
    modesArray.forEach(modeObj => {
      const modeData = CONFIG.TRANSPORT_MODES[modeObj.mode];
      const isSelected = modeObj.mode === selectedMode;

      // Calculate progress bar width (percentage of max emission)
      const barWidth = maxEmission > 0 ? (modeObj.emission / maxEmission) * 100 : 0;

      // Determine color based on percentage vs car
      let barColor;
      if (modeObj.percentageVsCar <= 25) {
        barColor = '#10b981'; // Green - very eco-friendly
      } else if (modeObj.percentageVsCar <= 75) {
        barColor = '#f59e0b'; // Yellow - moderate
      } else if (modeObj.percentageVsCar <= 100) {
        barColor = '#fb923c'; // Orange - high
      } else {
        barColor = '#ef4444'; // Red - very high
      }

      // Container div structure directly matching the repository file format
      html += `
        <div class="comparison_item${isSelected ? ' comparison_item--selected' : ''}">
          
          <div class="comparison_header">
            <span class="comparison_icon">${modeData.icon}</span>
            <span class="comparison_label">${modeData.label}</span>
            ${isSelected ? '<span class="comparison_badge">Selecionado</span>' : ''}
          </div>

          <div class="comparison_stats">
            <div class="comparison_grid_stat">
              <span class="comparison_stat-label">Emissão</span>
              <span class="comparison_stat-value">${this.formatNumber(modeObj.emission, 1)} kg CO₂</span>
            </div>
            <div class="comparison_grid_stat">
              <span class="comparison_stat-label">vs Carro</span>
              <span class="comparison_stat-value">${modeObj.percentageVsCar}%</span>
            </div>
          </div>

          <div class="comparison_progress-bar">
            <div class="comparison_progress-fill" style="width: ${barWidth}%; background-color: ${barColor}"></div>
          </div>

        </div>
      `;
    });

    html += `</div>`;

    // At the end, add tip box with helpful message
    html += `
      <div class="comparison__tip-box" style="margin-top: var(--spacing-lg); padding: var(--spacing-md); background: #eff6ff; border-left: 4px solid var(--info); border-radius: var(--radius);">
        <p style="color: #1e40af; font-size: 0.95rem;">💡 <strong>Dica Ecológica:</strong> Alternativas com menor emissão reduzem drasticamente sua pegada de carbono.</p>
      </div>
    `;

    // Return complete HTML string
    return html;
  },

  renderCarbonCredits: function(creditsData) {
    // creditsData contains: { credits, price: { min, max, average } }
    // Create HTML string with elements and format values
    const html = `
      <div class="carbon-credits__grid" style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: var(--spacing-md);">
        
        <div class="carbon-credits__card" style="background: var(--white); padding: var(--spacing-md); border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); text-align: center;">
          <div class="carbon-credits__value carbon-credits__value--large" style="font-size: 2rem; font-weight: bold; color: var(--primary);">${this.formatNumber(creditsData.credits, 4)}</div>
          <div class="carbon-credits__helper" style="font-size: 0.85rem; color: var(--text-light); margin-top: var(--spacing-xs);">1 crédito = 1000 kg CO₂</div>
        </div>
        
        <div class="carbon-credits__card" style="background: var(--white); padding: var(--spacing-md); border-radius: var(--radius-lg); box-shadow: var(--shadow-sm); text-align: center;">
          <div class="carbon-credits__value" style="font-size: 2rem; font-weight: bold; color: #111827;">${this.formatCurrency(creditsData.price.average)}</div>
          <div class="carbon-credits__range" style="font-size: 0.85rem; color: var(--text-light); margin-top: var(--spacing-xs);">Variação: ${this.formatCurrency(creditsData.price.min)} - ${this.formatCurrency(creditsData.price.max)}</div>
        </div>
        
      </div>

      <div class="carbon-credits__info-box" style="margin-top: var(--spacing-md); padding: var(--spacing-md); background: var(--white); border-radius: var(--radius); box-shadow: var(--shadow-sm);">
        <p style="font-size: 0.95rem; line-height: 1.5; color: #374151;">Créditos de carbono são ativos que comprovam que gases de efeito estufa foram evitados ou removidos da atmosfera através de projetos ambientais auditados.</p>
      </div>

      <button class="carbon-credits__button" type="button" style="margin-top: var(--spacing-md); width: 100%; background: var(--primary); color: var(--white); padding: 1rem; border: none; border-radius: var(--radius); font-weight: bold; cursor: pointer;">🛒 Compensar Emissões</button>
    `;

    // Return complete HTML string
    return html;
  }
};