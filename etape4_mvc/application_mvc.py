from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional, Callable
import threading

class Observer(ABC):
    
    
    @abstractmethod
    def update(self, sujet: 'Observable', **kwargs) -> None:
        pass


class Observable(ABC):
    def __init__(self):
        self._observers: List[Observer] = []
        self._lock = threading.Lock()
    
    def attacher(self, observer: Observer) -> None:
        with self._lock:
            if observer not in self._observers:
                self._observers.append(observer)
    
    def detacher(self, observer: Observer) -> None:
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
    
    def notifier(self, **kwargs) -> None:
        with self._lock:
            observers_copy = self._observers.copy()
        for observer in observers_copy:
            observer.update(self, **kwargs)


class CompteBancaireModel(Observable):
    _instance: Optional['CompteBancaireModel'] = None
    _singleton_lock: threading.Lock = threading.Lock()
    _initialise: bool = False
    
    def __new__(cls, titulaire: str = "", solde_initial: float = 0.0):
        if cls._instance is None:
            with cls._singleton_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, titulaire: str = "", solde_initial: float = 0.0):
        if CompteBancaireModel._initialise:
            return
        
        super().__init__()
        self._titulaire = titulaire
        self._solde = solde_initial
        self._historique: List[Dict] = []
        
        if solde_initial > 0:
            self._enregistrer_operation("OUVERTURE", solde_initial)
        
        CompteBancaireModel._initialise = True
    
    @classmethod
    def get_instance(cls) -> 'CompteBancaireModel':
        if cls._instance is None:
            raise RuntimeError("Le modèle n'a pas été initialisé.")
        return cls._instance
    
    @classmethod
    def reset_instance(cls) -> None:
        with cls._singleton_lock:
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
    
    def effectuer_depot(self, montant: float) -> tuple[bool, str]:
        if montant <= 0:
            return False, "Le montant doit être positif"
        
        self._solde += montant
        self._enregistrer_operation("DEPOT", montant)
        self.notifier(type_operation="DEPOT", montant=montant, solde=self._solde)
        
        return True, f"Dépôt de {montant:.2f}DT effectué"
    
    def effectuer_retrait(self, montant: float) -> tuple[bool, str]:
        if montant <= 0:
            return False, "Le montant doit être positif"
        
        if montant > self._solde:
            return False, f"Solde insuffisant ({self._solde:.2f}DT)"
        
        self._solde -= montant
        self._enregistrer_operation("RETRAIT", montant)
        self.notifier(type_operation="RETRAIT", montant=montant, solde=self._solde)
        
        return True, f"Retrait de {montant:.2f}DT effectué"
class VueBase(Observer, ABC):
    def __init__(self, model: CompteBancaireModel):
        self._model = model
        self._model.attacher(self)
    
    @abstractmethod
    def afficher(self) -> None:
        pass
    
    @abstractmethod
    def update(self, sujet: Observable, **kwargs) -> None:
        pass


class VueSolde(VueBase): 
    def afficher(self) -> None:
        print(f"SOLDE DU COMPTE")
        print(f"Titulaire: {self._model.titulaire}")
        print(f"Solde actuel: {self._model.solde:.2f}DT")

    
    def update(self, sujet: Observable, **kwargs) -> None:
        type_op = kwargs.get('type_operation', '')
        montant = kwargs.get('montant', 0)
        print(f"   [Vue Solde]  {type_op}: {montant:.2f}DT → Solde: {self._model.solde:.2f}DT")


class VueHistorique(VueBase):
    def afficher(self) -> None:
        print(f"HISTORIQUE DES OPÉRATIONS - {self._model.titulaire}")
        
        historique = self._model.historique
        if not historique:
            print("Aucune opération")
        else:
            for i, op in enumerate(historique, 1):
                symbole = "↑" if op['type'] in ["DEPOT", "OUVERTURE"] else "↓"
                print(f"│ {i}. {symbole} [{op['date']}] {op['type']}: "
                      f"{op['montant']:.2f}DT (Solde: {op['solde_apres']:.2f}DT)")
        
    
    def update(self, sujet: Observable, **kwargs) -> None:
        type_op = kwargs.get('type_operation', '')
        print(f"[Vue Historique] Nouvelle entrée: {type_op}")


class VueAlerte(VueBase):
    def __init__(self, model: CompteBancaireModel, seuil_alerte: float = 100.0):
        super().__init__(model)
        self.seuil_alerte = seuil_alerte
    
    def afficher(self) -> None:
        if self._model.solde < self.seuil_alerte:
            print(f"\n ALERTE: Solde bas ({self._model.solde:.2f}DT < {self.seuil_alerte:.2f}DT)")
        else:
            print(f"\n Solde OK: {self._model.solde:.2f}DT")
    
    def update(self, sujet: Observable, **kwargs) -> None:
        solde = kwargs.get('solde', 0)
        if solde < self.seuil_alerte:
            print(f"[Vue Alerte]  ATTENTION: Solde critique ({solde:.2f}DT)!")


class VueConsole(VueBase):
    def afficher(self) -> None:
        print(f" SYSTÈME BANCAIRE - {self._model.titulaire}")
        print(f"Solde: {self._model.solde:.2f}DT")

    
    def afficher_menu(self) -> None:
        """Affiche le menu principal."""
        print("\n┌─────────────────────────────────────┐")
        print("│           MENU PRINCIPAL            │")
        print("├─────────────────────────────────────┤")
        print("│ 1. Effectuer un dépôt               │")
        print("│ 2. Effectuer un retrait             │")
        print("│ 3. Consulter le solde               │")
        print("│ 4. Voir l'historique                │")
        print("│ 5. Vérifier les alertes             │")
        print("│ 0. Quitter                          │")
        print("└─────────────────────────────────────┘")
    
    def demander_montant(self, operation: str) -> Optional[float]:
        try:
            montant = float(input(f"Entrez le montant du {operation}: "))
            return montant
        except ValueError:
            print(" Montant invalide!")
            return None
    
    def afficher_message(self, message: str, succes: bool = True) -> None:
        """Affiche un message de résultat."""
        symbole = "✅" if succes else "❌"
        print(f"\n{symbole} {message}")
    
    def update(self, sujet: Observable, **kwargs) -> None:
        pass

class CompteBancaireController:    
    def __init__(self, model: CompteBancaireModel):
        self._model = model
        self._vues: Dict[str, VueBase] = {}
    
    def ajouter_vue(self, nom: str, vue: VueBase) -> None:
        self._vues[nom] = vue
    
    def get_vue(self, nom: str) -> Optional[VueBase]:
        return self._vues.get(nom)
    
    def effectuer_depot(self, montant: float) -> tuple[bool, str]:
        return self._model.effectuer_depot(montant)
    
    def effectuer_retrait(self, montant: float) -> tuple[bool, str]:
        return self._model.effectuer_retrait(montant)
    
    def consulter_solde(self) -> float:
        return self._model.solde
    
    def obtenir_historique(self) -> List[Dict]:
        return self._model.historique
    
    def run_console(self) -> None:
        vue_console = self._vues.get('console')
        vue_solde = self._vues.get('solde')
        vue_historique = self._vues.get('historique')
        vue_alerte = self._vues.get('alerte')
        
        if not vue_console or not isinstance(vue_console, VueConsole):
            print("Erreur: Vue console non configurée")
            return
        
        print("Bienvenue dans le Système de Gestion Bancaire MVC")
        
        while True:
            vue_console.afficher()
            vue_console.afficher_menu()
            
            try:
                choix = input("\nVotre choix: ").strip()
            except EOFError:
                break
            
            if choix == "1": 
                montant = vue_console.demander_montant("dépôt")
                if montant is not None:
                    print("\n  Notifications des vues  ")
                    succes, message = self.effectuer_depot(montant)
                    vue_console.afficher_message(message, succes)
            
            elif choix == "2":  
                montant = vue_console.demander_montant("retrait")
                if montant is not None:
                    print("\n  Notifications des vues  ")
                    succes, message = self.effectuer_retrait(montant)
                    vue_console.afficher_message(message, succes)
            
            elif choix == "3":  
                if vue_solde:
                    vue_solde.afficher()
            
            elif choix == "4":  
                if vue_historique:
                    vue_historique.afficher()
            
            elif choix == "5":  
                if vue_alerte:
                    vue_alerte.afficher()
            
            elif choix == "0":  
                print("\n Au revoir!")
                break
            
            else:
                print("\n Choix invalide!")



class ApplicationBancaire:
    
    def __init__(self, titulaire: str, solde_initial: float = 0.0):
        self._model = CompteBancaireModel(titulaire, solde_initial)
        self._controller = CompteBancaireController(self._model)
        self._setup_vues()
    
    def _setup_vues(self) -> None:
        vue_console = VueConsole(self._model)
        self._controller.ajouter_vue('console', vue_console)
        vue_solde = VueSolde(self._model)
        self._controller.ajouter_vue('solde', vue_solde)
        vue_historique = VueHistorique(self._model)
        self._controller.ajouter_vue('historique', vue_historique)
        vue_alerte = VueAlerte(self._model, seuil_alerte=200.0)
        self._controller.ajouter_vue('alerte', vue_alerte)   
    def run(self) -> None:
        self._controller.run_console()
    
    @property
    def model(self) -> CompteBancaireModel:
        return self._model
    
    @property
    def controller(self) -> CompteBancaireController:
        return self._controller


def demonstration_mvc():
    print("DÉMONSTRATION DE L'ARCHITECTURE MVC")
    print("\n1. Création du Modèle, Vues et Contrôleur")
    
    model = CompteBancaireModel("ImedZayet", 1000.0)
    controller = CompteBancaireController(model)
    vue_solde = VueSolde(model)
    vue_historique = VueHistorique(model)
    vue_alerte = VueAlerte(model, seuil_alerte=300.0)
    
    controller.ajouter_vue('solde', vue_solde)
    controller.ajouter_vue('historique', vue_historique)
    controller.ajouter_vue('alerte', vue_alerte)
    
    print(" MVC configuré!")
    print("\n2. État initial")
    vue_solde.afficher()
    print("\n3. Opérations via le Contrôleur")
    print("\n>>> Dépôt de 500DT")
    succes, msg = controller.effectuer_depot(500.0)
    print(f"   Résultat: {msg}")
    print("\n>>> Retrait de 300DT")
    succes, msg = controller.effectuer_retrait(300.0)
    print(f"   Résultat: {msg}")
    print("\n>>> Retrait de 800DT")
    succes, msg = controller.effectuer_retrait(800.0)
    print(f"   Résultat: {msg}")
    print("\n4. Affichage des différentes Vues")
    
    vue_solde.afficher()
    vue_historique.afficher()
    vue_alerte.afficher()
    


if __name__ == "__main__":
    import sys
    CompteBancaireModel.reset_instance()
    
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        demonstration_mvc()
    else:
        app = ApplicationBancaire("Imed Zayet", 1000.0)
        app.run()
