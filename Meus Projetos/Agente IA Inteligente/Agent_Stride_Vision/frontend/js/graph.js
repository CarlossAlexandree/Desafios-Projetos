/**
 * graph.js — Renderiza um grafo simplificado da arquitetura usando Cytoscape.js,
 * destacando os componentes citados no modelo de ameaças retornado pela IA.
 *
 * Cytoscape.js foi mantido (era a lib usada no material do curso): é leve,
 * carregada via CDN sem precisar de bundler/Node, e cobre bem o caso de uso
 * de "grafo de componentes com destaque de nós" — trocar por vis.js ou
 * React Flow não traria ganho perceptível para este escopo.
 */

let cyInstance = null;

const STRIDE_COLORS = {
  "Spoofing": "#4FD1C5",
  "Tampering": "#F2B84B",
  "Repudiation": "#9B8CFF",
  "Information Disclosure": "#FF8FB1",
  "Denial of Service": "#FF6B5E",
  "Elevation of Privilege": "#6FCF97",
};

function colorForThreatType(threatType) {
  return STRIDE_COLORS[threatType] || "#8B9AAB";
}

/**
 * Constrói nós/arestas a partir da lista de "affected_component" presentes
 * no modelo de ameaças. Como não fazemos visão computacional de bounding
 * boxes, o grafo é uma representação lógica dos componentes citados pela
 * IA, conectados sequencialmente — suficiente para dar contexto visual
 * sem inventar uma topologia que a IA não confirmou.
 */
function buildElementsFromThreatModel(threatModel) {
  const components = new Map(); // nome -> { threatTypes: Set }

  threatModel.forEach((threat) => {
    const componentName = threat.affected_component || "Componente não identificado";
    if (!components.has(componentName)) {
      components.set(componentName, new Set());
    }
    components.get(componentName).add(threat.threat_type);
  });

  const nodes = Array.from(components.entries()).map(([name, threatTypes], index) => {
    const primaryType = Array.from(threatTypes)[0];
    return {
      data: {
        id: `n${index}`,
        label: name,
        threatCount: threatTypes.size,
      },
      style: {
        "background-color": colorForThreatType(primaryType),
      },
    };
  });

  const edges = [];
  for (let i = 0; i < nodes.length - 1; i++) {
    edges.push({ data: { id: `e${i}`, source: nodes[i].data.id, target: nodes[i + 1].data.id } });
  }

  return [...nodes, ...edges];
}

function renderGraph(threatModel) {
  const container = document.getElementById("cy");
  if (cyInstance) {
    cyInstance.destroy();
  }

  const elements = buildElementsFromThreatModel(threatModel);

  if (elements.length === 0) {
    container.innerHTML =
      '<p style="color:#8B9AAB;padding:1rem;font-size:0.85rem;">Nenhum componente identificável foi retornado pela análise.</p>';
    return;
  }

  cyInstance = cytoscape({
    container,
    elements,
    layout: { name: "breadthfirst", directed: true, padding: 20, spacingFactor: 1.3 },
    style: [
      {
        selector: "node",
        style: {
          label: "data(label)",
          "font-size": "11px",
          "font-family": "JetBrains Mono, monospace",
          color: "#E8EEF4",
          "text-valign": "bottom",
          "text-margin-y": 8,
          "text-wrap": "wrap",
          "text-max-width": "90px",
          width: 34,
          height: 34,
          "border-width": 2,
          "border-color": "#0D1219",
        },
      },
      {
        selector: "edge",
        style: {
          width: 1.5,
          "line-color": "#1E2733",
          "target-arrow-color": "#1E2733",
          "target-arrow-shape": "triangle",
          "curve-style": "bezier",
        },
      },
    ],
  });
}

window.STRIDEGraph = { renderGraph, STRIDE_COLORS };
