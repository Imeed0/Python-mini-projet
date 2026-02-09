from datetime import datetime

class CompteBancaire:
    def __init__(self, titulaire: str, solde_initial: float = 0.0):
        self._titulaire = titulaire
        self._solde = solde_initial
        self._historique = []
        
        if solde_initial > 0:
            self._enregistrer("OUVERTURE", solde_initial)
    
    def _enregistrer(self, type_op: str, montant: float):
        self._historique.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": type_op,
            "montant": montant,
            "solde_apres": self._solde
        })
    
    def deposer(self, montant: float):
        if montant <= 0:
            print("Erreur: Le montant doit être positif")
            return False
        
        self._solde += montant
        self._enregistrer("DEPOT", montant)
        print(f"Dépôt de {montant:.2f}DT effectué. Nouveau solde: {self._solde:.2f}DT")
        return True
    
    def retirer(self, montant: float):
        if montant <= 0:
            print("Erreur: Le montant doit être positif")
            return False
        
        if montant > self._solde:
            print(f"Erreur: Solde insuffisant ({self._solde:.2f}DT)")
            return False
        
        self._solde -= montant
        self._enregistrer("RETRAIT", montant)
        print(f"Retrait de {montant:.2f}DT effectué. Nouveau solde: {self._solde:.2f}DT")
        return True
    
    def afficher_solde(self):
        print(f"Solde de {self._titulaire}: {self._solde:.2f}DT")
    
    def afficher_historique(self):
        print(f"\nHistorique de {self._titulaire}:")
        if not self._historique:
            print("Aucune opération")
            return
        for i, op in enumerate(self._historique, 1):
            print(f"  {i}. [{op['date']}] {op['type']}: {op['montant']:.2f}DT → Solde: {op['solde_apres']:.2f}DT")


if __name__ == "__main__":
    print("ÉTAPE 1: Compte Bancaire Simple\n")
    nom = input("Entrez le nom du titulaire: ")
    solde = float(input("Entrez le solde initial: "))
    compte = CompteBancaire(nom, solde)
    
    while True:
        print("\n--- Menu ---")
        print("1. Déposer")
        print("2. Retirer")
        print("3. Afficher solde")
        print("4. Afficher historique")
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
        elif choix == "0":
            break
        else:
            print("Choix invalide")
    
