from datetime import datetime

class CompteBancaireSingleton:
    _instance = None  
    
    def __new__(cls, titulaire="", solde_initial=0.0):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialise = False
        return cls._instance
    
    def __init__(self, titulaire="", solde_initial=0.0):
        if self._initialise:
            return
        
        self._titulaire = titulaire
        self._solde = solde_initial
        self._historique = []
        
        if solde_initial > 0:
            self._enregistrer("OUVERTURE", solde_initial)
        
        self._initialise = True
        print(f"Instance unique créée pour {titulaire}")
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("Le compte n'existe pas encore")
        return cls._instance
    
    def _enregistrer(self, type_op, montant):
        self._historique.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": type_op,
            "montant": montant,
            "solde_apres": self._solde
        })
    
    def deposer(self, montant):
        if montant <= 0:
            print("Erreur: Montant doit être positif")
            return False
        self._solde += montant
        self._enregistrer("DEPOT", montant)
        print(f"Dépôt de {montant:.2f}DT. Nouveau solde: {self._solde:.2f}DT")
        return True
    
    def retirer(self, montant):
        if montant <= 0:
            print("Erreur: Montant doit être positif")
            return False
        if montant > self._solde:
            print(f"Erreur: Solde insuffisant ({self._solde:.2f}DT)")
            return False
        self._solde -= montant
        self._enregistrer("RETRAIT", montant)
        print(f"Retrait de {montant:.2f}DT. Nouveau solde: {self._solde:.2f}DT")
        return True
    
    def afficher_solde(self):
        print(f"Solde de {self._titulaire}: {self._solde:.2f}DT")
    
    def afficher_historique(self):
        print(f"\nHistorique de {self._titulaire}:")
        for i, op in enumerate(self._historique, 1):
            print(f"  {i}. [{op['date']}] {op['type']}: {op['montant']:.2f}DT → Solde: {op['solde_apres']:.2f}DT")


if __name__ == "__main__":
    print("ÉTAPE 2: Pattern Singleton\n")
    nom = input("Entrez le nom du titulaire: ")
    solde = float(input("Entrez le solde initial: "))
    compte = CompteBancaireSingleton(nom, solde)
    
    while True:
        print("\n--- Menu ---")
        print("1. Déposer")
        print("2. Retirer")
        print("3. Afficher solde")
        print("4. Afficher historique")
        print("5. Tester Singleton")
        print("0. Quitter")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            montant = float(input("Montant à déposer: "))
            compte.deposer(montant)
        elif choix == "2":
            montant = float(input("Montant à retirer: "))
            compte.retirer(montant)
        elif choix == "3":
            compte.afficher_solde()
        elif choix == "4":
            compte.afficher_historique()
        elif choix == "5":
            print("\n Test Singleton")
            nom2 = input("Entrez un AUTRE nom: ")
            solde2 = float(input("Entrez un AUTRE solde: "))
            compte2 = CompteBancaireSingleton(nom2, solde2)
            print(f"\nRésultat:")
            print(f"  Titulaire: {compte2._titulaire} (pas '{nom2}')")
            print(f"  Solde: {compte2._solde:.2f}DT (pas {solde2:.2f}DT)")
        elif choix == "0":
            break
        else:
            print("Choix invalide")
    

