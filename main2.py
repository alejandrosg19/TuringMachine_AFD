#!/usr/bin/python3
import sys

def cargar_programa(archivo_programa):
    dict_command = {}
    finally_state = set()

    with open(archivo_programa) as programa:
        for linea in programa:
            validate_linea = linea.split()

            if len(validate_linea) == 3:
                current_state, current_value, new_state = validate_linea
            else:
                current_state, current_value, new_value, move, new_state = validate_linea


            if '*' in current_state:
                current_state = current_state.strip('*')
                finally_state.add(current_state)
                
            if len(validate_linea) == 3:
                dict_command[current_state, current_value] = new_state
            else:
                dict_command[current_state, current_value] = [new_value, move, new_state]

    return dict_command, finally_state

def AFD(archivo_cintas, d, F):
    mensaje = {True: 'Aceptada', False: 'Rechazada'}
    
    with open(archivo_cintas) as cintas:
        for cinta in cintas:
            cinta = cinta.strip()
            q = '0'
            for simbolo in cinta:
                q = d[q, simbolo]
            print(f'La entrada {cinta} es {mensaje[q in F]}')

def turing_machine(archivo_cintas, dict_command):
    current_state = '0'
    cabeza = 0
    band = True
    more_cinta = 0

    with open(archivo_cintas) as cintas:
        for cinta in cintas:
            cinta = cinta.strip()
            cabeza = cinta.index('*')
            cinta = cinta.replace('*','')

            while(band):
                if ((current_state, cinta[cabeza]) in dict_command):
                    new_value, move, new_state = dict_command[(current_state,cinta[cabeza])]
                    cinta = cinta[:cabeza] + new_value + cinta[cabeza+1:]
                    current_state = new_state

                    if move == 'r':
                        cabeza += 1
                    else:
                        cabeza -= 1
                    
                    if cabeza == (len(cinta) -1):
                        cinta += '_'
                        more_cinta += 1
                    elif cabeza == 0:
                        cinta = '_' + cinta
                        more_cinta += 1


                    if more_cinta == 10:
                        band = False
                else:
                    band = False
                
                print("cinta: ", cinta[:cabeza] + '*' + cinta[cabeza:])

def main():
    if len(sys.argv) < 3:
        print("Error: No se proporcionaron suficientes argumentos.")
        print("Uso: ./simulador programa.txt cintas.txt")
        sys.exit(1)

    archivo_programa, archivo_cintas = sys.argv[1], sys.argv[2]
    dict_command, final_states = cargar_programa(archivo_programa)

    if final_states:
        AFD(archivo_cintas, dict_command, final_states)
    else:
        turing_machine(archivo_cintas, dict_command)

if __name__ == "__main__":
    main()
