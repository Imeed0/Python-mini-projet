import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
def print_menu():
    print("SYSTÈME DE GESTION DE COMPTE BANCAIRE")
    print("1. Étape 1 - Développement sans Design Pattern")
    print("2. Étape 2 - Pattern Singleton")
    print("3. Étape 3 - Pattern Observer")
    print("4. Étape 4 - Architecture MVC")
    print("q. Quitter")


def run_etape1():
    print("ÉTAPE 1 : DÉVELOPPEMENT SANS DESIGN PATTERN")
    
    from etape1_sans_pattern.compte_bancaire import (
        CompteBancaire, ModuleAffichage, ModuleHistorique, 
        ModuleAlerte, ModuleControle
    )
    print("\n Configuration du compte ")
    titulaire = input("Nom du titulaire: ").strip()
    while True:
        try:
            solde_initial = float(input("Solde initial: "))
            if solde_initial < 0:
                print("Le solde ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
    
    while True:
        try:
            seuil_alerte = float(input("Seuil d'alerte: "))
            if seuil_alerte < 0:
                print("Le seuil ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
    
    compte = CompteBancaire(titulaire, solde_initial)
    module_affichage = ModuleAffichage(compte)
    module_historique = ModuleHistorique(compte)
    module_alerte = ModuleAlerte(compte, seuil=seuil_alerte)
    module_controle = ModuleControle(compte)
    print("\n  État initial  ")
    module_affichage.afficher()
    module_alerte.verifier_solde()
    while True:
        print("\n--- Menu des opérations ---")
        print("1. Effectuer un dépôt")
        print("2. Effectuer un retrait")
        print("3. Consulter le solde")
        print("4. Afficher l'historique")
        print("5. Vérifier les alertes")
        print("6. Afficher le rapport")
        print("0. Terminer")
        
        choix = input("Votre choix: ").strip()
        
        if choix == "1":
            while True:
                try:
                    montant = float(input("Montant du dépôt: "))
                    break
                except ValueError:
                    print("Montant invalide. Veuillez entrer un nombre.")
            compte.deposer(montant)
        elif choix == "2":
            while True:
                try:
                    montant = float(input("Montant du retrait: "))
                    break
                except ValueError:
                    print("Montant invalide. Veuillez entrer un nombre.")
            compte.retirer(montant)
        elif choix == "3":
            module_affichage.afficher()
        elif choix == "4":
            module_historique.afficher_historique()
        elif choix == "5":
            module_alerte.verifier_solde()
        elif choix == "6":
            module_controle.rapport()
        elif choix == "0":
            break
        else:
            print("Choix invalide!")
    
    print("\n  État final  ")
    module_affichage.afficher()
    module_alerte.verifier_solde()
    module_controle.rapport()
    module_historique.afficher_historique()
    compte2 = CompteBancaire(titulaire, 500.0)


def run_etape2():
    print("ÉTAPE 2 : PATTERN SINGLETON")

    from etape2_singleton.compte_singleton import (
        CompteBancaireSingleton, ModuleAffichage, ModuleHistorique,
        ModuleAlerte, ModuleControle
    )
    print("\n  Configuration du compte  ")
    titulaire = input("Nom du titulaire: ").strip()
    while True:
        try:
            solde_initial = float(input("Solde initial: "))
            if solde_initial < 0:
                print("Le solde ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
    
    while True:
        try:
            seuil_alerte = float(input("Seuil d'alerte: "))
            if seuil_alerte < 0:
                print("Le seuil ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
    
    CompteBancaireSingleton.reset_instance()
    compte = CompteBancaireSingleton(titulaire, solde_initial)
    
    
    compte2 = CompteBancaireSingleton()
    compte3 = CompteBancaireSingleton.get_instance()
    while True:
        print("\n--- Menu des opérations ---")
        print("1. Effectuer un dépôt")
        print("2. Effectuer un retrait")
        print("3. Consulter le solde")
        print("4. Afficher l'historique")
        print("5. Vérifier les alertes")
        print("6. Afficher le rapport")
        print("0. Terminer")
        
        choix = input("Votre choix: ").strip()
        
        if choix == "1":
            while True:
                try:
                    montant = float(input("Montant du dépôt: "))
                    break
                except ValueError:
                    print("Montant invalide. Veuillez entrer un nombre.")
            compte.deposer(montant)
        elif choix == "2":
            while True:
                try:
                    montant = float(input("Montant du retrait: "))
                    break
                except ValueError:
                    print("Montant invalide. Veuillez entrer un nombre.")
            compte.retirer(montant)
        elif choix == "3":
            ModuleAffichage().afficher()
        elif choix == "4":
            ModuleHistorique().afficher_historique()
        elif choix == "5":
            ModuleAlerte(seuil=seuil_alerte).verifier_solde()
        elif choix == "6":
            ModuleControle().rapport()
        elif choix == "0":
            break
        else:
            print("Choix invalide!")
    
    print("\n  Modules utilisant le Singleton  ")
    ModuleAffichage().afficher()
    ModuleAlerte(seuil=seuil_alerte).verifier_solde()
    ModuleControle().rapport()


def run_etape3():
    print("ÉTAPE 3 : PATTERN OBSERVER")
    
    from etape3_observer.compte_observer import (
        CompteBancaireObservable, ObservateurAffichage, ObservateurHistorique,
        ObservateurAlerte, ObservateurControle, ObservateurNotificationEmail
    )
    print("\n  Configuration du compte  ")
    titulaire = input("Nom du titulaire: ").strip()
    while True:
        try:
            solde_initial = float(input("Solde initial: "))
            if solde_initial < 0:
                print("Le solde ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
    
    while True:
        try:
            seuil_alerte = float(input("Seuil d'alerte: "))
            if seuil_alerte < 0:
                print("Le seuil ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
    
    while True:
        try:
            limite_retrait = float(input("Limite de retrait: "))
            if limite_retrait < 0:
                print("La limite ne peut pas être négative.")
                continue
            break
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
    
    email = input("Email de notification: ").strip()
    
    CompteBancaireObservable.reset_instance()
    compte = CompteBancaireObservable(titulaire, solde_initial)

    while True:
        print("\n--- Menu des opérations ---")
        print("1. Effectuer un dépôt")
        print("2. Effectuer un retrait")
        print("3. Consulter le solde")
        print("4. Afficher l'historique")
        print("0. Terminer")
        
        choix = input("Votre choix: ").strip()
        
        if choix == "1":
            while True:
                try:
                    montant = float(input("Montant du dépôt: "))
                    break
                except ValueError:
                    print("Montant invalide. Veuillez entrer un nombre.")
            print(f"\n>>> Dépôt de {montant}DT")
            compte.deposer(montant)
        elif choix == "2":
            while True:
                try:
                    montant = float(input("Montant du retrait: "))
                    break
                except ValueError:
                    print("Montant invalide. Veuillez entrer un nombre.")
            print(f"\n>>> Retrait de {montant}DT")
            compte.retirer(montant)
        elif choix == "3":
            print(f"\nSolde actuel: {compte.solde:.2f}DT")
        elif choix == "4":
            compte.afficher_historique()
        elif choix == "0":
            break
        else:
            print("Choix invalide!")


def run_etape4():
    print("ÉTAPE 4 : ARCHITECTURE MVC")
    
    from etape4_mvc.application_mvc import (
        CompteBancaireModel, CompteBancaireController,
        VueSolde, VueHistorique, VueAlerte
    )
    print("\n  Configuration du compte  ")
    titulaire = input("Nom du titulaire: ").strip()
    while True:
        try:
            solde_initial = float(input("Solde initial: "))
            if solde_initial < 0:
                print("Le solde ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
    
    while True:
        try:
            seuil_alerte = float(input("Seuil d'alerte: "))
            if seuil_alerte < 0:
                print("Le seuil ne peut pas être négatif.")
                continue
            break
        except ValueError:
            print("Montant invalide. Veuillez entrer un nombre.")
    
    CompteBancaireModel.reset_instance()
    print("\n  Configuration MVC  ")
    model = CompteBancaireModel(titulaire, solde_initial)
    controller = CompteBancaireController(model)
    vue_solde = VueSolde(model)
    vue_historique = VueHistorique(model)
    vue_alerte = VueAlerte(model, seuil_alerte=seuil_alerte)
    
    print("Modèle créé")
    print("Contrôleur créé")
    print("Vues créées et attachées au modèle")
    print("\n  État initial  ")
    vue_solde.afficher()
    while True:
        print("\n--- Menu des opérations ---")
        print("1. Effectuer un dépôt")
        print("2. Effectuer un retrait")
        print("3. Consulter le solde")
        print("4. Afficher l'historique")
        print("5. Vérifier les alertes")
        print("0. Terminer")
        
        choix = input("Votre choix: ").strip()
        
        if choix == "1":
            while True:
                try:
                    montant = float(input("Montant du dépôt: "))
                    break
                except ValueError:
                    print("Montant invalide. Veuillez entrer un nombre.")
            print(f"\n>>> Dépôt de {montant}DT")
            succes, msg = controller.effectuer_depot(montant)
            print(f"   Résultat: {msg}")
        elif choix == "2":
            while True:
                try:
                    montant = float(input("Montant du retrait: "))
                    break
                except ValueError:
                    print("Montant invalide. Veuillez entrer un nombre.")
            print(f"\n>>> Retrait de {montant}DT")
            succes, msg = controller.effectuer_retrait(montant)
            print(f"   Résultat: {msg}")
        elif choix == "3":
            vue_solde.afficher()
        elif choix == "4":
            vue_historique.afficher()
        elif choix == "5":
            vue_alerte.afficher()
        elif choix == "0":
            break
        else:
            print("Choix invalide!")
    
    print("\n  État final  ")
    vue_solde.afficher()
    vue_historique.afficher()
    vue_alerte.afficher()


def main():
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        if arg == "1":
            run_etape1()
        elif arg == "2":
            run_etape2()
        elif arg == "3":
            run_etape3()
        elif arg == "4":
            run_etape4()
        elif arg == "all":
            run_etape1()
            input("\nAppuyez sur Entrée pour continuer...")
            run_etape2()
            input("\nAppuyez sur Entrée pour continuer...")
            run_etape3()
            input("\nAppuyez sur Entrée pour continuer...")
            run_etape4()
        else:
            print(f"Argument inconnu: {arg}")
            print("Usage: python main.py [1|2|3|4|all]")
    else:
        while True:
            print_menu()
            choix = input("Votre choix: ").strip().lower()
            
            if choix == "1":
                run_etape1()
            elif choix == "2":
                run_etape2()
            elif choix == "3":
                run_etape3()
            elif choix == "4":
                run_etape4()
            elif choix == "all":
                run_etape1()
                input("\nAppuyez sur Entrée pour continuer...")
                run_etape2()
                input("\nAppuyez sur Entrée pour continuer...")
                run_etape3()
                input("\nAppuyez sur Entrée pour continuer...")
                run_etape4()
            elif choix == "q":
                print("\n Au revoir!")
                break
            else:
                print(" Choix invalide!")
            
            input("\nAppuyez sur Entrée pour revenir au menu...")


if __name__ == "__main__":
    main()
