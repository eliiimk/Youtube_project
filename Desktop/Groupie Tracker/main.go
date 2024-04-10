package main

import (
	"fyne.io/fyne/v2"
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/container"
    "fyne.io/fyne/v2/widget"
)

var suggestions []string // Déclarer la variable suggestions à un niveau global

func main() {
    // Initialise une nouvelle application Fyne
    myApp := app.New()

    // Crée une nouvelle fenêtre avec un titre
    myWindow := myApp.NewWindow("Groupie Tracker GUI")

    // Crée un widget Entry pour la barre de recherche
    searchBar := widget.NewEntry()
    searchBar.SetPlaceHolder("Entrez votre recherche")

    // Crée un widget List pour afficher les suggestions de recherche
    suggestionList := widget.NewList(
        func() int {
            return len(suggestions)// Retourne la longueur des suggestions
        },
        func() fyne.CanvasObject {
            return widget.NewLabel("") // Créer un label vide pour chaque élément de la liste
        },
		func(i int, obj fyne.CanvasObject) {
            // Mettre à jour le label avec le texte de la suggestion
            obj.(*widget.Label).SetText(suggestions[i])
        },
		
    )

    // Crée un conteneur pour organiser les widgets
    content := container.NewVBox(
        searchBar,
        suggestionList,
    )

    // Ajoute un événement de saisie à la barre de recherche pour afficher les suggestions
	searchBar.OnChanged = func(text string) {
        suggestions = generateSuggestions(text) // Fonction factice pour générer des suggestions
        suggestionList.Refresh()
    }

    // Définit le contenu de la fenêtre
    myWindow.SetContent(content)

    // Affiche la fenêtre et démarre la boucle principale de l'interface utilisateur
    myWindow.ShowAndRun()
}

// Fonction factice pour générer des suggestions de recherche
func generateSuggestions(text string) []string {
	// Si le texte de recherche est vide, retourner un tableau vide
	if text == "" {
		return []string{}
	}
    // Implémentez votre logique de génération de suggestions ici
    // Cela peut inclure la recherche dans une base de données, un fichier, ou tout autre source de données
    // Pour cet exemple, je retourne simplement une liste de suggestions statiques
    return []string{
        "Phil Collins - membre",
        "Phil Collins - artiste/groupe",
        "Queen - artiste/groupe",
        "John Deacon - membre",
        "Brian May - membre",
    }
}
