per ogni turno:
    calcola la prossima zona desiderata di ogni drone
    ordina i droni per priorità
    rifiuta:
        - due droni sulla stessa zona
        - ingresso in una zona piena
        - scambi simultanei A -> B e B -> A
        - ingresso in una connessione piena
    applica tutti i movimenti approvati
    aggiorna code, capacità e stato dei droni