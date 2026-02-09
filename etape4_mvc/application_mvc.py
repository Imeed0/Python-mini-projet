from datetime import datetime
class CompteBancaireModel:
    def __init__(self, titulaire, solde_initial=0.0):
        self._titulaire = titulaire
        self._solde = solde_initial
        self._historique = []
        
        if solde_initial > 0:
            self._enregistrer("OUVERTURE", solde_initial)
    
    def _enregistrer(self, type_op, montant):
        self._historique.append({
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": type_op,
            "montant": montant,
            "solde_apres": self._solde
        })
    
    def deposer(self, montant):
        if montant <= 0:
            return False, "Montant doit être positif"
        self._solde += montant
        self._enregistrer("DEPOT", montant)
        return True, f"Dépôt de {montant:.2f}DT effectué"
    
    def retirer(self, montant):
        if montant <= 0:
            return False, "Montant doit être positif"
        if montant > self._solde:
            return False, f"Solde insuffisant ({self._solde:.2f}DT)"
        self._solde -= montant
        self._enregistrer("RETRAIT", montant)
        return True, f"Retrait de {montant:.2f}DT effectué"

class Vue:
    def __init__(self, model):
        self._model = model
    
    def afficher_solde(self):
        print(f"\n SOLDE ")
        print(f"Titulaire: {self._model._titulaire}")
        print(f"Solde: {self._model._solde:.2f}DT")
    
    def afficher_historique(self):
        print(f"\n HISTORIQUE ")
        if not self._model._historique:
            print("Aucune opération")
        else:
            for i, op in enumerate(self._model._historique, 1):
                print(f"  {i}. [{op['date']}] {op['type']}: {op['montant']:.2f}DT")
    
    def afficher_menu(self):
        print("\n--- Menu MVC ---")
        print("1. Déposer")
        print("2. Retirer")
        print("3. Afficher solde")
        print("4. Afficher historique")
        print("0. Quitter")
    
    def demander_montant(self, operation):
        return float(input(f"Montant à {operation}: "))
    
    def afficher_message(self, message, succes):
        print(f"\n{'✓' if succes else '✗'} {message}")


class Controller:
    def __init__(self, model, vue):
        self._model = model
        self._vue = vue
    
    def deposer(self, montant):
        succes, message = self._model.deposer(montant)
        self._vue.afficher_message(message, succes)
        if succes:
            print(f"  [Notification] {self._model._titulaire}, vous avez déposé {montant:.2f}DT avec succès!")
    
    def retirer(self, montant):
        succes, message = self._model.retirer(montant)
        self._vue.afficher_message(message, succes)
        if succes:
            print(f"  [Notification] {self._model._titulaire}, vous avez retiré {montant:.2f}DT avec succès!")
    
    def afficher_solde(self):
        self._vue.afficher_solde()
    
    def afficher_historique(self):
        self._vue.afficher_historique()
    
    def executer(self):
        while True:
            self._vue.afficher_menu()
            choix = input("\nVotre choix: ")
            
            if choix == "1":
                montant = self._vue.demander_montant("déposer")
                self.deposer(montant)
            
            elif choix == "2":
                montant = self._vue.demander_montant("retirer")
                self.retirer(montant)
            
            elif choix == "3":
                self.afficher_solde()
            
            elif choix == "4":
                self.afficher_historique()
            
            elif choix == "0":
                break
            
            else:
                print("Choix invalide")

if __name__ == "__main__":
    print("ÉTAPE 4: Architecture MVC Pure\n")
    
    nom = input("Entrez le nom du titulaire: ")
    solde = float(input("Entrez le solde initial: "))
    
    model = CompteBancaireModel(nom, solde)
    vue = Vue(model)
    controller = Controller(model, vue)
    
    print(f"Compte créé pour {nom}")
    controller.executer()
