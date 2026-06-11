// RoutesDB is a global object containing route information for popular Brazilian city pairs.
// Each route object includes origin, destination, and an approximate distance in kilometers.
const RoutesDB = {
  routes: [
    { origin: "São Paulo, SP", destination: "Rio de Janeiro, RJ", distanceKm: 430 },
    { origin: "São Paulo, SP", destination: "Brasília, DF", distanceKm: 1015 },
    { origin: "Rio de Janeiro, RJ", destination: "Brasília, DF", distanceKm: 1148 },
    { origin: "Belo Horizonte, MG", destination: "Ouro Preto, MG", distanceKm: 100 },
    { origin: "São Paulo, SP", destination: "Campinas, SP", distanceKm: 95 },
    { origin: "Rio de Janeiro, RJ", destination: "Niterói, RJ", distanceKm: 13 },
    { origin: "Curitiba, PR", destination: "São Paulo, SP", distanceKm: 408 },
    { origin: "Curitiba, PR", destination: "Florianópolis, SC", distanceKm: 300 },
    { origin: "Porto Alegre, RS", destination: "Florianópolis, SC", distanceKm: 700 },
    { origin: "Salvador, BA", destination: "Fortaleza, CE", distanceKm: 1118 },
    { origin: "Salvador, BA", destination: "Recife, PE", distanceKm: 805 },
    { origin: "Fortaleza, CE", destination: "Natal, RN", distanceKm: 536 },
    { origin: "Manaus, AM", destination: "Belém, PA", distanceKm: 1610 },
    { origin: "Belém, PA", destination: "São Luís, MA", distanceKm: 1026 },
    { origin: "Teresina, PI", destination: "São Luís, MA", distanceKm: 440 },
    { origin: "Goiânia, GO", destination: "Brasília, DF", distanceKm: 210 },
    { origin: "Campinas, SP", destination: "Ribeirão Preto, SP", distanceKm: 220 },
    { origin: "Campinas, SP", destination: "Santos, SP", distanceKm: 79 },
    { origin: "São Paulo, SP", destination: "Santos, SP", distanceKm: 72 },
    { origin: "Curitiba, PR", destination: "Londrina, PR", distanceKm: 398 },
    { origin: "Porto Alegre, RS", destination: "Curitiba, PR", distanceKm: 710 },
    { origin: "Fortaleza, CE", destination: "São Paulo, SP", distanceKm: 2845 },
    { origin: "Recife, PE", destination: "Salvador, BA", distanceKm: 805 },
    { origin: "Belo Horizonte, MG", destination: "Brasília, DF", distanceKm: 748 },
    { origin: "Belém, PA", destination: "Brasília, DF", distanceKm: 1700 },
    { origin: "Natal, RN", destination: "Recife, PE", distanceKm: 290 },
    { origin: "Porto Alegre, RS", destination: "São Paulo, SP", distanceKm: 1130 },
    { origin: "Goiânia, GO", destination: "São Paulo, SP", distanceKm: 920 },
    { origin: "Maceió, AL", destination: "Recife, PE", distanceKm: 247 },
    { origin: "João Pessoa, PB", destination: "Natal, RN", distanceKm: 180 },
    { origin: "Campo Grande, MS", destination: "Goiânia, GO", distanceKm: 712 },
    { origin: "Vitória, ES", destination: "Rio de Janeiro, RJ", distanceKm: 520 },
    { origin: "Belém, PA", destination: "Manaus, AM", distanceKm: 1610 },
    { origin: "São Luís, MA", destination: "Fortaleza, CE", distanceKm: 1024 },
    { origin: "Florianópolis, SC", destination: "Porto Alegre, RS", distanceKm: 700 },
    { origin: "Belo Horizonte, MG", destination: "Rio de Janeiro, RJ", distanceKm: 435 },
    { origin: "São Paulo, SP", destination: "Belo Horizonte, MG", distanceKm: 586 },
    { origin: "Recife, PE", destination: "Natal, RN", distanceKm: 292 },
    { origin: "Fortaleza, CE", destination: "Belém, PA", distanceKm: 1680 },
    { origin: "Angra dos Reis, RJ", destination: "Rio de Janeiro, RJ", distanceKm: 160 },
    { origin: "Cabo Frio, RJ", destination: "Rio de Janeiro, RJ", distanceKm: 155 },
    { origin: "Juiz de Fora, MG", destination: "Belo Horizonte, MG", distanceKm: 260 },
    { origin: "Feira de Santana, BA", destination: "Salvador, BA", distanceKm: 100 },
    { origin: "Foz do Iguaçu, PR", destination: "Curitiba, PR", distanceKm: 640 },
    { origin: "Juazeiro do Norte, CE", destination: "Fortaleza, CE", distanceKm: 530 },
    { origin: "Caxias do Sul, RS", destination: "Porto Alegre, RS", distanceKm: 130 }
  ],

  // Return unique sorted array of all city names from origin and destination fields.
  getAllCities: function () {
    const cities = this.routes.reduce(function (acc, route) {
      if (acc.indexOf(route.origin) === -1) {
        acc.push(route.origin);
      }
      if (acc.indexOf(route.destination) === -1) {
        acc.push(route.destination);
      }
      return acc;
    }, []);
    return cities.sort(function (a, b) {
      return a.localeCompare(b, "pt-BR");
    });
  },

  // CORREÇÃO: Função aprimorada para remover múltiplos espaços em branco e normalizar strings de forma idêntica
  findDistance: function (origin, destination) {
    if (!origin || !destination) return null;

    // Converte para letras minúsculas e remove espaços nas pontas e duplicados internamente
    const normalizedOrigin = origin.trim().toLowerCase().replace(/\s+/g, ' ');
    const normalizedDestination = destination.trim().toLowerCase().replace(/\s+/g, ' ');

    for (let i = 0; i < this.routes.length; i += 1) {
      const route = this.routes[i];
      const routeOrigin = route.origin.trim().toLowerCase().replace(/\s+/g, ' ');
      const routeDestination = route.destination.trim().toLowerCase().replace(/\s+/g, ' ');

      // Verifica correspondência exata em ambas as direções da rota
      if (
        (routeOrigin === normalizedOrigin && routeDestination === normalizedDestination) ||
        (routeOrigin === normalizedDestination && routeDestination === normalizedOrigin)
      ) {
        return route.distanceKm;
      }
    }

    return null;
  }
};