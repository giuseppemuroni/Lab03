from operator import attrgetter

class Strumento:
    def __init__(self, codice, tipo, marca, anno_acquisto, valore):
        self.codice = codice
        self.tipo = tipo
        self.marca = marca
        self.anno_acquisto = int(anno_acquisto)
        self.valore = float(valore)

    def __str__(self):
        return f"[{self.codice}] {self.tipo} {self.marca} {self.anno_acquisto} - {self.valore}"

class Prestito:
    def __init__(self, codice, data, id_strumento, cognome_allievo):
        self.codice = codice
        self.data = data
        self.id_strumento = id_strumento
        self.cognome_allievo = cognome_allievo


    def __str__(self):
        return f"Prestito {self.codice}: Strumenti {self.id_strumento} allievo {self.cognome_allievo} in data {self.data}"



class DepositoStrumenti:
    def __init__(self, nome, responsabile):
        """Inizializza gli attributi e le strutture dati"""
        self.nome = nome
        self._responsabile = responsabile
        self.strumenti = {}
        self.prestiti = {}
        self.contatore_prestiti = 1

    @property
    def responsabile(self):
        return self._responsabile

    @responsabile.setter
    def responsabile(self,nuovo_nome):
        self._responsabile = nuovo_nome



    def carica_file_strumenti(self, file_path):
        """Carica gli strumenti dal file"""
        with open(file_path,"r",encoding='utf-8') as f:
            for riga in f:
                riga = riga.strip()
                if not riga:
                    continue

                pezzi = riga.split(",")
                codice = pezzi[0]
                s = Strumento(codice, pezzi[1], pezzi[2], pezzi[3], pezzi[4])
                self.strumenti[codice] = s


    def aggiungi_strumento(self, tipo, marca, anno_acquisto, valore):
        """Aggiunge uno strumento nel deposito: aggiunge solo nel sistema e non aggiorna il file"""
        max_id = 0
        for cod in self.strumenti.keys():
            numero = int(cod[1:])
            if numero > max_id:
                max_id = numero

        nuovo_codice = f"S{max_id+1}"
        nuovo_strumento = Strumento(nuovo_codice, tipo, marca, anno_acquisto, valore)
        self.strumenti[nuovo_codice] = nuovo_strumento

        return nuovo_strumento

    def strumenti_ordinati_per_marca(self):
        """Ordina gli strumenti per marca in ordine alfabetico"""
        lista_strumenti = list(self.strumenti.values())
        lista_strumenti.sort(key=attrgetter('marca'))
        return lista_strumenti


    def nuovo_prestito(self, data, id_strumento, cognome_allievo):
        """Crea un nuovo prestito"""
        if id_strumento not in self.strumenti:
            raise Exception("Errore: lo strumento richiesto non esiste nel sistema.")

        for p in self.prestiti.values():
            if p.id_strumento == id_strumento:
                raise Exception("Errore: lo strumento è già attualmente in prestito.")

        codice_prestito = f"P{self.contatore_prestiti}"
        self.contatore_prestiti +=1

        nuovo = Prestito(codice_prestito, data,id_strumento, cognome_allievo)
        self.prestiti[codice_prestito] = nuovo

        return nuovo

    def termina_prestito(self, id_prestito):
        """Termina un prestito in atto"""
        if id_prestito not in self.prestiti:
            raise Exception("Errore: nessun prestito trovato con questo ID.")

        del self.prestiti[id_prestito]
