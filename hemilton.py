def operaciones(rango):
    contpares = 0
    contimpares = 0
    pares = 0
    impares = 0
    
    for i in range(rango):
        num = int(input(f"Ingrese el número {i+1}: "))
        
        if num % 2 == 0:
            pares += num
            contpares += 1
        else:
            impares += num
            contimpares += 1
    
    print(f"Promedio de pares: ",pares / contpares)
    print(f"Promedio de impares: ",impares / contimpares)

def main():
    
    rango = int(input("Ingrese la cantidad de números a ingresar: "))
    operaciones(rango)


main()

