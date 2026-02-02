from datetime import datetime
from typing import List, Dict, Optional
import threading

class CompteBancaireSingleton:
    _instance: Optional['CompteBancaireSingleton'] = None
    _lock: threading.Lock = threading.Lock()  # Pour la thread-safety
    _initialise: bool = False
    
    def __new__(cls, titulaire: str = "", solde_initial: float = 0.0):
        if cls._instance is None:
            with cls._lock:
                # Double vérification pour éviter les conditions de course
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, titulaire: str = "", solde_initial: float = 0.0):
        if CompteBancaireSingleton._initialise:
            return
        
        self._titulaire = titulaire
        self._solde = solde_initial
        self._historique: List[Dict] = []
        
        if solde_initial > 0:
            self._enregistrer_operation("OUVERTURE", solde_initial)
        
        CompteBancaireSingleton._initialise = True
        print(f"Instance unique du compte créée pour {titulaire}")
    
    @classmethod
    def get_instance(cls) -> 'CompteBancaireSingleton':
        if cls._instance is None:
            raise RuntimeError("Le compte n'a pas encore été créé. "
                             "Utilisez d'abord CompteBancaireSingleton(titulaire, solde)")
        return cls._instance
    
    @classmethod
    def reset_instance(cls) -> None:
        with cls._lock:
            cls._instance = None
            cls._initialise = False
    
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
            print(f"Erreur: Le montant du dépôt doit être positif.")
            return False
        
        with self._lock:  
            self._solde += montant
            self._enregistrer_operation("DEPOT", montant)
        
        print(f"Dépôt de {montant:.2f}€ effectué. Nouveau solde: {self._solde:.2f}€")
        return True
    
    def retirer(self, montant: float) -> bool:
        if montant <= 0:
            print(f"Erreur: Le montant du retrait doit être positif.")
            return False
        
        with self._lock:  
            if montant > self._solde:
                print(f"Erreur: Solde insuffisant. Solde: {self._solde:.2f}€")
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
    
    def __str__(self) -> str:
        return f"Compte de {self._titulaire} - Solde: {self._solde:.2f}€"

class ModuleAffichage:
    def afficher(self) -> None:
        compte = CompteBancaireSingleton.get_instance()
        print(f"\n[Module Affichage] {compte}")


class ModuleHistorique:
    def afficher_historique(self) -> None:
        compte = CompteBancaireSingleton.get_instance()
        print("\n[Module Historique]")
        compte.afficher_historique()


class ModuleAlerte:
    def __init__(self, seuil: float = 100.0):
        self.seuil = seuil
    
    def verifier_solde(self) -> None:
        compte = CompteBancaireSingleton.get_instance()
        if compte.solde < self.seuil:
            print(f"\n  [Module Alerte] ATTENTION: Solde bas! "
                  f"({compte.solde:.2f}€ < {self.seuil:.2f}€)")
        else:
            print(f"\n [Module Alerte] Solde OK: {compte.solde:.2f}€")


class ModuleControle:
    def rapport(self) -> None:
        compte = CompteBancaireSingleton.get_instance()
        print(f"\n[Module Contrôle] Rapport")
        print(f"  - Titulaire: {compte.titulaire}")
        print(f"  - Solde actuel: {compte.solde:.2f}€")
        print(f"  - Nombre d'opérations: {len(compte.historique)}")


def test_acces_multiples():
    print("Test: Accès multiples au même compte")

    module_affichage = ModuleAffichage()
    module_alerte = ModuleAlerte(seuil=200.0)
    module_controle = ModuleControle()
    module_affichage.afficher()
    module_alerte.verifier_solde()
    module_controle.rapport()


def test_singleton():
    print("Test: Vérification du pattern Singleton")

    compte1 = CompteBancaireSingleton()
    compte2 = CompteBancaireSingleton()
    compte3 = CompteBancaireSingleton.get_instance()
    
    


def test_thread_safety():
    import concurrent.futures
    print("Test: Thread-safety")
    
    def faire_operation(id_thread: int):
        compte = CompteBancaireSingleton.get_instance()
        compte.deposer(100.0)
        return f"Thread {id_thread}: Dépôt effectué"
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        futures = [executor.submit(faire_operation, i) for i in range(5)]
        for future in concurrent.futures.as_completed(futures):
            print(future.result())
    
    compte = CompteBancaireSingleton.get_instance()
    print(f"\nSolde final après 5 dépôts de 100€: {compte.solde:.2f}€")


if __name__ == "__main__":
    print("ÉTAPE 2: Système avec Pattern Singleton")
    compte = CompteBancaireSingleton("Imed Zayet", 1000.0)
    print("\n  État initial  ")
    compte.consulter_solde()
    print("\n  Opérations  ")
    compte.deposer(500.0)
    compte.retirer(300.0)
    test_singleton()
    test_acces_multiples()
    test_thread_safety()
    ModuleHistorique().afficher_historique()
    

