from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict, Optional
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
                print(f" Observateur {observer.__class__.__name__} attaché")
    
    def detacher(self, observer: Observer) -> None:
        with self._lock:
            if observer in self._observers:
                self._observers.remove(observer)
                print(f" Observateur {observer.__class__.__name__} détaché")
    
    def notifier(self, **kwargs) -> None:
        with self._lock:
            observers_copy = self._observers.copy()
        
        for observer in observers_copy:
            observer.update(self, **kwargs)


class CompteBancaireObservable(Observable):
    _instance: Optional['CompteBancaireObservable'] = None
    _singleton_lock: threading.Lock = threading.Lock()
    _initialise: bool = False
    
    def __new__(cls, titulaire: str = "", solde_initial: float = 0.0):
        if cls._instance is None:
            with cls._singleton_lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, titulaire: str = "", solde_initial: float = 0.0):
        if CompteBancaireObservable._initialise:
            return
        
        super().__init__()  
        
        self._titulaire = titulaire
        self._solde = solde_initial
        self._historique: List[Dict] = []
        
        if solde_initial > 0:
            self._enregistrer_operation("OUVERTURE", solde_initial)
        
        CompteBancaireObservable._initialise = True
        print(f"Compte observable créé pour {titulaire}")
    
    @classmethod
    def get_instance(cls) -> 'CompteBancaireObservable':
        if cls._instance is None:
            raise RuntimeError("Le compte n'a pas encore été créé.")
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
    
    def deposer(self, montant: float) -> bool:
        if montant <= 0:
            print(f"Erreur: Le montant du dépôt doit être positif.")
            return False
        
        self._solde += montant
        self._enregistrer_operation("DEPOT", montant)
        
        print(f"\n💰 Dépôt de {montant:.2f}DT effectué. Nouveau solde: {self._solde:.2f}DT")
        self.notifier(
            type_operation="DEPOT",
            montant=montant,
            solde=self._solde
        )
        
        return True
    
    def retirer(self, montant: float) -> bool:
        if montant <= 0:
            print(f"Erreur: Le montant du retrait doit être positif.")
            return False
        
        if montant > self._solde:
            print(f"Erreur: Solde insuffisant.")
            return False
        
        self._solde -= montant
        self._enregistrer_operation("RETRAIT", montant)
        
        print(f"\n Retrait de {montant:.2f}DT effectué. Nouveau solde: {self._solde:.2f}DT")

        self.notifier(
            type_operation="RETRAIT",
            montant=montant,
            solde=self._solde
        )
        
        return True
    
    def __str__(self) -> str:
        return f"Compte de {self._titulaire} - Solde: {self._solde:.2f}DT"


class ObservateurAffichage(Observer):
    def update(self, sujet: Observable, **kwargs) -> None:
        if isinstance(sujet, CompteBancaireObservable):
            print(f"[Affichage] Solde mis à jour: {sujet.solde:.2f}DT")


class ObservateurHistorique(Observer):
    def update(self, sujet: Observable, **kwargs) -> None:
        type_op = kwargs.get('type_operation', 'INCONNU')
        montant = kwargs.get('montant', 0)
        print(f"[Historique] Nouvelle opération: {type_op} de {montant:.2f}DT")


class ObservateurAlerte(Observer):
    def __init__(self, seuil: float = 100.0):
        self.seuil = seuil
    
    def update(self, sujet: Observable, **kwargs) -> None:
        if isinstance(sujet, CompteBancaireObservable):
            if sujet.solde < self.seuil:
                print(f"[ALERTE] Solde critique! {sujet.solde:.2f}DT < {self.seuil:.2f}DT")
            elif sujet.solde < self.seuil * 2:
                print(f"[Alerte] Solde bas: {sujet.solde:.2f}DT")


class ObservateurControle(Observer):
    def __init__(self, limite_retrait: float = 500.0):
        self.limite_retrait = limite_retrait
    
    def update(self, sujet: Observable, **kwargs) -> None:
        type_op = kwargs.get('type_operation', '')
        montant = kwargs.get('montant', 0)
        
        if type_op == "RETRAIT" and montant > self.limite_retrait:
            print(f"[Contrôle]  Retrait important détecté: {montant:.2f}DT")
        else:
            print(f"[Contrôle] Opération validée")


class ObservateurNotificationEmail(Observer):
    def __init__(self, email: str):
        self.email = email
    
    def update(self, sujet: Observable, **kwargs) -> None:
        type_op = kwargs.get('type_operation', 'INCONNU')
        montant = kwargs.get('montant', 0)
        solde = kwargs.get('solde', 0)
        
        print(f"[Email → {self.email}] "
              f"{type_op} de {montant:.2f}DT. Solde: {solde:.2f}DT")


if __name__ == "__main__":
    print("ÉTAPE 3: Système avec Pattern Observer")
    compte = CompteBancaireObservable("Imed Zayet", 1000.0)
    print("\n  Création et attachement des observateurs  ")
    obs_affichage = ObservateurAffichage()
    obs_historique = ObservateurHistorique()
    obs_alerte = ObservateurAlerte(seuil=200.0)
    obs_controle = ObservateurControle(limite_retrait=500.0)
    obs_email = ObservateurNotificationEmail("zayetimed01@gmail.com")
    compte.attacher(obs_affichage)
    compte.attacher(obs_historique)
    compte.attacher(obs_alerte)
    compte.attacher(obs_controle)
    compte.attacher(obs_email)
    print("Opérations avec notifications automatiques")
    compte.deposer(500.0)
    compte.retirer(300.0)
    compte.retirer(800.0)
    compte.retirer(200.0)

    print("Ajout dynamique d'un nouvel observateur")
    class ObservateurSMS(Observer):
        def __init__(self, numero: str):
            self.numero = numero
        
        def update(self, sujet: Observable, **kwargs) -> None:
            print(f"[SMS → {self.numero}] Notification reçue!")
    obs_sms = ObservateurSMS("06 12 34 56 78")
    compte.attacher(obs_sms)
    compte.deposer(100.0)
    print("Détachement d'un observateur")
    compte.detacher(obs_email)
    compte.deposer(50.0)
