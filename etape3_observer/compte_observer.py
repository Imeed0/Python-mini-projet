from abc import ABC, abstractmethod
from datetime import datetime
class Observer(ABC):
    @abstractmethod
    def update(self, compte, **kwargs):
        pass
class Observable:
    def __init__(self):
        self._observers = []
    
    def attacher(self, observer):
        if observer not in self._observers:
            self._observers.append(observer)
            
    
    def detacher(self, observer):
        if observer in self._observers:
            self._observers.remove(observer)
            
    
    def notifier(self, **kwargs):
        for observer in self._observers:
            observer.update(self, **kwargs)
class CompteBancaireObservable(Observable):
    _instance = None
    
    def __new__(cls, titulaire="", solde_initial=0.0):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialise = False
        return cls._instance
    
    def __init__(self, titulaire="", solde_initial=0.0):
        if self._initialise:
            return
        
        super().__init__()
        self._titulaire = titulaire
        self._solde = solde_initial
        self._historique = []
        
        if solde_initial > 0:
            self._enregistrer("OUVERTURE", solde_initial)
        
        self._initialise = True
        print(f"Compte créé pour {titulaire}")
    
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
        self.notifier(type_operation="DEPOT", montant=montant, solde=self._solde)
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
        self.notifier(type_operation="RETRAIT", montant=montant, solde=self._solde)
        return True
    
    def afficher_solde(self):
        print(f"Solde de {self._titulaire}: {self._solde:.2f}DT")
    
    def afficher_historique(self):
        print(f"\nHistorique de {self._titulaire}:")
        for i, op in enumerate(self._historique, 1):
            print(f"  {i}. [{op['date']}] {op['type']}: {op['montant']:.2f}DT → Solde: {op['solde_apres']:.2f}DT")


class ObservateurAffichage(Observer):
    def update(self, compte, **kwargs):
        print(f"  [Affichage] Solde: {compte._solde:.2f}DT")


class ObservateurAlerte(Observer):
    def __init__(self, seuil=100.0):
        self._seuil = seuil
    
    def update(self, compte, **kwargs):
        if compte._solde < self._seuil:
            print(f"  [ALERTE] Solde bas! {compte._solde:.2f}DT < {self._seuil:.2f}DT")


class ObservateurMessage(Observer):
    def update(self, compte, **kwargs):
        type_op = kwargs.get('type_operation', '')
        montant = kwargs.get('montant', 0)
        if type_op == 'DEPOT':
            print(f"  [Message] {compte._titulaire}, vous avez déposé {montant:.2f}DT avec succès!")
        elif type_op == 'RETRAIT':
            print(f"  [Message] {compte._titulaire}, vous avez retiré {montant:.2f}DT avec succès!")


if __name__ == "__main__":
    print("ÉTAPE 3: Pattern Observer\n")
    
    nom = input("Entrez le nom du titulaire: ")
    solde = float(input("Entrez le solde initial: "))
    seuil = float(input("Entrez le seuil d'alerte: "))
    
    compte = CompteBancaireObservable(nom, solde)
    obs_affichage = ObservateurAffichage()
    obs_alerte = ObservateurAlerte(seuil)
    obs_message = ObservateurMessage()
    
    compte.attacher(obs_affichage)
    compte.attacher(obs_alerte)
    compte.attacher(obs_message)
    
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
