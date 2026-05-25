import contextlib

# ---------------- Funkcje pomocnicze --------------------
def dodaj(A, B):
    n = len(A)
    m = len(A[0])
    return [[A[i][j] + B[i][j] for j in range(m)] for i in range(n)]

def odejmij(A, B):
    n = len(A)
    m = len(A[0])
    return [[A[i][j] - B[i][j] for j in range(m)] for i in range(n)]

def czy_potega_2(n):
    return n > 0 and (n & (n - 1)) == 0

def najmniejsza_potega_2(n):
    if n <= 0:
        raise ValueError("n musi być dodatnie.")
    m = 1
    while m < n:
        m *= 2
    return m

def dop_macierz_zerami(A, m):
    n = len(A)
    A_dop = [[0] * m for _ in range(m)]
    for i in range(n):
        for j in range(n):
            A_dop[i][j] = A[i][j]
    return A_dop

def obetnij_macierz(A, n):
    return [wiersz[:n] for wiersz in A[:n]]

def polacz(C11, C12, C21, C22):
    k = len(C11)
    n = 2 * k
    C = [[0] * n for _ in range(n)]
    for i in range(k):
        for j in range(k):
            C[i][j] = C11[i][j]
            C[i][j + k] = C12[i][j]
            C[i + k][j] = C21[i][j]
            C[i + k][j + k] = C22[i][j]
    return C

def podzial_macierzy(A):
    n = len(A)
    k = n // 2
    A11 = [[0]*k for _ in range(k)]
    A12 = [[0]*k for _ in range(k)]
    A21 = [[0]*k for _ in range(k)]
    A22 = [[0]*k for _ in range(k)]
    for i in range(k):
        for j in range(k):
            A11[i][j] = A[i][j]
            A12[i][j] = A[i][j + k]
            A21[i][j] = A[i + k][j]
            A22[i][j] = A[i + k][j + k]
    return A11, A12, A21, A22

# ---------------- Funkcje główne --------------------

def strassen(A, B):
    n = len(A)
    if n == 1:
        return [[A[0][0] * B[0][0]]]
    A11, A12, A21, A22 = podzial_macierzy(A)
    B11, B12, B21, B22 = podzial_macierzy(B)
    M1 = strassen(dodaj(A11, A22), dodaj(B11, B22))
    M2 = strassen(dodaj(A21, A22), B11)
    M3 = strassen(A11, odejmij(B12, B22))
    M4 = strassen(A22, odejmij(B21, B11))
    M5 = strassen(dodaj(A11, A12), B22)
    M6 = strassen(odejmij(A21, A11), dodaj(B11, B12))
    M7 = strassen(odejmij(A12, A22), dodaj(B21, B22))
    C11 = dodaj(odejmij(dodaj(M1, M4), M5), M7)
    C12 = dodaj(M3, M5)
    C21 = dodaj(M2, M4)
    C22 = dodaj(odejmij(dodaj(M1, M3), M2), M6)
    return polacz(C11, C12, C21, C22)

def strassen_dop(A, B):
    n = len(A)
    m = najmniejsza_potega_2(n)
    if m == n:
        return strassen(A, B)
    A_dop = dop_macierz_zerami(A, m)
    B_dop = dop_macierz_zerami(B, m)
    C_dop = strassen(A_dop, B_dop)
    return obetnij_macierz(C_dop, n)

def znajdz_X(A):
    A_sq = strassen_dop(A, A)
    X_zawodnicy = []
    for i, wiersz in enumerate(A_sq):
        if 0 not in wiersz:
            X_zawodnicy.append(i + 1)  # numeracja od 1
    return X_zawodnicy

def wyswietl_macierz(A, naglowek="Macierz:"):
    n = len(A)
    print(f"{naglowek}")
    # Naglowek kolumn
    print("     " + "  ".join(f"Z{j+1:>2}" for j in range(n)))
    print("     " + "----" * n)
    for i, wiersz in enumerate(A):
        print(f"Z{i+1:>2} | " + "   ".join(str(x) for x in wiersz))

def wczytaj_macierz():
    print("=" * 55)
    print("  WŁASNOŚĆ X W TURNIEJU ")
    print("=" * 55)
    print()

    while True:
        try:
            n = int(input("Podaj liczbę zawodników (n >= 2): ").strip())
            if n < 2:
                print("  Liczba zawodników musi być >= 2 \n")
                continue
            break
        except ValueError:
            print("  Niepoprawna wartość. Podaj liczbę całkowitą.\n")

    print()
    print(f"Podaj wyniki meczów:")
    print()

    A = [[1]*n for _ in range(n)]
    i = 0
    j = 1
    while i < n:
        while j < n:
            try:
                wynik_meczu = int(input(f"Czy zawodnik Z{i+1} wygrał z zawodnikiem Z{j+1}? (1-tak, 0-nie): "))
                if wynik_meczu not in [0,1]:
                    print("Niepoprawny wynik meczu")
                    continue
                A[i][j], A[j][i] = wynik_meczu, 1-wynik_meczu
                j += 1
            except ValueError:
                print(" Błąd. Wynik meczu musi być liczbą całkowitą 0 lub 1.")
        i += 1
        j = i+1
    return A

def main():
    while True:
        try:
            print("Wybierz sposób wprowadzania danych:\n > Dane z pliku - p\n > Dane wpisane ręcznie - r")
            wybor = input("Twój wybor: ")
            while wybor not in ("p", "r"):
                print("Wybierz jedną z opcji p/r:")
                wybor = input("Twój wybor: ")

            if wybor == "p":
                name = input("Podaj nazwę pliku .txt z danymi wejściowymi: ")
                folder = input("Czy plik pochodzi z folderu dane_testowe? t/n (tak/nie)")
                if folder in ["t", "tak"]:
                    name = "dane_testowe" + "/" + name
                if not name.endswith(".txt"):
                    name += ".txt"
                with open(name, "r") as f:
                    n = int(f.readline())
                    A = []
                    for _ in range(n):
                        A.append(eval(f.readline()))
                    #print(A)
            if wybor == "r":
                A = wczytaj_macierz()
                n = len(A)
            print()
            wyswietl_macierz(A, "Wprowadzona macierz zwycięstw:")

            print("\nObliczanie...")
            wynik = znajdz_X(A)

            print("\n" + "=" * 55)
            if wynik:
                zawodnicy_str = ", ".join(f"Z{z}" for z in wynik)
                print(f"Zawodnicy z własnością X: {zawodnicy_str}")
                print(f"(indeksy: {wynik})")
            else:
                print("Żaden zawodnik nie spełnia własności X.")
            print("=" * 55)

            # Zapis do pliku
            out = input("Czy chcesz zapisać wynik do pliku? t/n (tak/nie): ")
            if out in ["t", "tak"]:
                name_out = input("Podaj nazwę pliku, w którym chcesz zapisać wynik: ")
                if not name_out.endswith(".txt"):
                    name_out += ".txt"
                with open(f"wyniki/{name_out}", "w", encoding = "utf-8") as f:
                    with contextlib.redirect_stdout(f):
                        wyswietl_macierz(A, "Wprowadzona macierz zwycięstw:")
                    f.write("\n" + "=" * 55 + "\n")
                    f.write(f"Zawodnicy z własnością X: {zawodnicy_str}\n")
                    f.write(f"Indeksy: {wynik}")

        except KeyboardInterrupt:
            print("\n\nPrzerwano przez użytkownika.")
        except Exception as e:
            print(f"\nBŁĄD: {e}")

        exit = input("\nCzy chcesz zamknąć program? t/n (tak/nie)")
        if exit in ["t", "tak"]:
            break
        print("=" * 55, "\n")

if __name__ == "__main__":
    main()