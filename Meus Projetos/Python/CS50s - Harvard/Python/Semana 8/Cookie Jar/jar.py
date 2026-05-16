class Jar:
    # Método inicializador com capacidade padrão 12
    def __init__(self, capacity=12):
        self.capacity = capacity
        # Atributo privado para armazenar o número de biscoitos
        self._cookies = 0

    # Método especial para representação em string (exibe emojis)
    def __str__(self):
        return "🍪" * self._cookies

    # Método personalizado para adicionar biscoitos
    def deposit(self, n):
        # Validação: n deve ser positivo e não exceder a capacidade
        if n < 0 or self._cookies + n > self.capacity:
            raise ValueError("Exceeds capacity")
        self._cookies += n

    # Método personalizado para remover biscoitos
    def withdraw(self, n):
        # Validação: n deve ser positivo e não exceder a quantidade atual
        if n < 0 or n > self._cookies:
            raise ValueError("Exceeds current cookies")
        self._cookies -= n

    # Propriedade capacity (getter com validação no setter implícito)
    @property
    def capacity(self):
        return self._capacity

    # Setter implicito com validação
    @capacity.setter
    def capacity(self, capacity):
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be a positive integer")
        self._capacity = capacity

    # Propriedade size (getter para a quantidade atual de biscoitos)
    @property
    def size(self):
        return self._cookies

# Exemplo de uso (para você testar)
def main():
    pote = Jar(10)
    print(f"Capacidade: {pote.capacity}")
    pote.deposit(5)
    print(f"Pote: {pote}")
    pote.withdraw(2)
    print(f"Pote: {pote}")
    pote.deposit(6) # Deve lançar ValueError "Exceeds capacity"
    print(f"Pote: {pote}")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(f"Erro: {e}")