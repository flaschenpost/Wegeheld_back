# Wegeheld_back

Backend der Wegeheld-App. Die Produktiversionen der Apps benutzen einen hier nicht veröffentlichten Teil.

Öffentlich unter der GPLv3 Lizenz.

Ziele:
* Hilfe beim Anzeigen von Falschparkern, die öffentliche Wege blockieren
* Hilfe beim Dokumentieren solcher Fälle

## Ablauf: 
### Reporter anlegen
POST createReporter.html POST mit city, zipcode, email, nickname
### Basisdaten holen
GET getBaseData.html liefert [CarColor,Action,CarBrand, Funnysaying, Offense, Obstruction, EmailText]
### Ordnungsamt holen
GET getOffices.html Parameter postalcode: liefert zuständiges Ordnungsamt 
