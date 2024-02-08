package main

import (
    "fyne.io/fyne/v2/app"
    "fyne.io/fyne/v2/container"
    "fyne.io/fyne/v2/widget"
)

func main() {
    // Initialise une nouvelle application Fyne
    myApp := app.New()

    // Crée une nouvelle fenêtre avec un titre
    myWindow := myApp.NewWindow("Ma première fenêtre Fyne")

    // Crée un widget de texte
    hello := widget.NewLabel("Bonjour, Monde!")

    // Crée un conteneur pour organiser les widgets
    myWindow.SetContent(container.NewVBox(
        hello,
        widget.NewButton("Cliquez moi", func() {
            hello.SetText("Vous avez cliqué!")
        }),
    ))

    // Affiche la fenêtre et démarre la boucle principale de l'interface utilisateur
    myWindow.ShowAndRun()
}
