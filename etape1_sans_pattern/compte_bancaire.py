from datetime import datetime
from typing import List, Dict

class CompteBancaire:
    def __init__(self, titulaire: str, solde_initial: float = 0.0):
        self._titulaire = titulaire
        self._solde = solde_initial
        self._historique: List[Dict] = []

        if solde_initial > 0:
            self._enregistrer_operation("OUVERTURE", solde_initial)
    
    @property
    def titulaire(self) -> str:
        return self._titulaire
    
    @property
    def solde(self) -> float:
        return self._solde
    
    @property
    def historique(self) -> List[Dict]:
        return self._historique.copy()
    
    def _enregistrer_operation(self, type_operation: str, montant: float) -> None:
        operation = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": type_operation,
            "montant": montant,
            "solde_apres": self._solde
        }
        self._historique.append(operation)
    
    def deposer(self, montant: float) -> bool:
        if montant <= 0:
            print(f"Erreur: Le montant du dépôt doit être positif. Montant fourni: {montant}")
            return False
        
        self._solde += montant
        self._enregistrer_operation("DEPOT", montant)
        print(f"Dépôt de {montant:.2f}€ effectué. Nouveau solde: {self._solde:.2f}€")
        return True
    
    def retirer(self, montant: float) -> bool:
        if montant <= 0:
            print(f"Erreur: Le montant du retrait doit être positif. Montant fourni: {montant}")
            return False
        
        if montant > self._solde:
            print(f"Erreur: Solde insuffisant. Solde actuel: {self._solde:.2f}€, Retrait demandé: {montant:.2f}€")
            return False
        
        self._solde -= montant
        self._enregistrer_operation("RETRAIT", montant)
        print(f"Retrait de {montant:.2f}€ effectué. Nouveau solde: {self._solde:.2f}€")
        return True
    
    def consulter_solde(self) -> float:
        print(f"Solde du compte de {self._titulaire}: {self._solde:.2f}€")
        return self._solde
    
    def afficher_historique(self) -> None:
        print(f"Historique du compte de {self._titulaire}")
        
        if not self._historique:
            print("Aucune opération enregistrée.")
            return
        
        for i, op in enumerate(self._historique, 1):
            print(f"{i}. [{op['date']}] {op['type']}: {op['montant']:.2f}€ "
                  f"(Solde: {op['solde_apres']:.2f}€)")
        
        print(f"{'='*60}\n")
    
    def __str__(self) -> str:
        return f"Compte de {self._titulaire} - Solde: {self._solde:.2f}€"

class ModuleAffichage:
    def __init__(self, compte: CompteBancaire):
        self.compte = compte

    def afficher(self) -> None:
        print(f"\n[Module Affichage] {self.compte}")

class ModuleHistorique:
    def __init__(self, compte: CompteBancaire):
        self.compte = compte
    
    def afficher_historique(self) -> None:
        print("\n[Module Historique]")
        self.compte.afficher_historique()


class ModuleAlerte:
    def __init__(self, compte: CompteBancaire, seuil: float = 100.0):
        self.compte = compte
        self.seuil = seuil
    
    def verifier_solde(self) -> None:
        if self.compte.solde < self.seuil:
            print(f"\n  [Module Alerte] ATTENTION: Solde bas! "
                  f"Solde actuel: {self.compte.solde:.2f}€ (seuil: {self.seuil:.2f}€)")
        else:
            print(f"\n [Module Alerte] Solde OK: {self.compte.solde:.2f}€")


class ModuleControle:
    def __init__(self, compte: CompteBancaire):
        self.compte = compte
    
    def rapport(self) -> None:
        print(f"\n[Module Contrôle] Rapport")
        print(f"  - Titulaire: {self.compte.titulaire}")
        print(f"  - Solde actuel: {self.compte.solde:.2f}€")
        print(f"  - Nombre d'opérations: {len(self.compte.historique)}")



if __name__ == "__main__":
    print("ÉTAPE 1: Système sans Design Pattern")
    compte = CompteBancaire("Imed Zayet", 1000.0)
    module_affichage = ModuleAffichage(compte)
    module_historique = ModuleHistorique(compte)
    module_alerte = ModuleAlerte(compte, seuil=200.0)
    module_controle = ModuleControle(compte)
    print("\n  État initial  ")
    module_affichage.afficher()
    module_alerte.verifier_solde()
    print("\n  Opérations  ")
    compte.deposer(500.0)
    compte.retirer(300.0)
    compte.retirer(1000.0)  
    print("\n  État après opérations  ")
    module_affichage.afficher()
    module_alerte.verifier_solde()
    module_controle.rapport()
    module_historique.afficher_historique()
    compte2 = CompteBancaire("Imed Zayet", 500.0)
    
