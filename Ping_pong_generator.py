from random import randint

def generuj_macierz(n):
    A = [[0 for _ in range(n)] for _ in range(n)]
    for i in range(n):
        A[i][i] = 1
        for j in range(i + 1, n):
            A[j][i] = randint(0, 1)
            A[i][j] = 1 - A[j][i]
    return A

def main():
    # liczba zawodników
    while True:
            try:
                n = int(input("Podaj liczbe zawodnikow (n >= 2): ").strip())
                if n < 2:
                    print("  Liczba zawodnikow musi byc >= 2 \n")
                    continue
                break
            except ValueError:
                print("  Niepoprawna wartosc. Podaj liczbe calkowita.\n")

    A = generuj_macierz(n)
    name = input("Podaj nazwę pliku .txt do zapisu danych wejściowych: ")
    if not name.endswith(".txt"):
        name += ".txt"
    with open(f"dane_testowe/{name}", "w") as f:
        f.write(str(len(A)))
        for i in range(len(A)):
            f.write("\n" + str(A[i]))

if __name__ == "__main__":
    main()