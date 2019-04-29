# Divera-Monitor-Raspberry-Pi
In diesem Tutorial wird auf einem Raspberry Pi eine autommatische Steuerung des Divera Monitors eingerichtet. Der Raspberry schaltet bei Alarmen sowie zu Dienstzeiten den Monitor an und im Anschluss wieder aus. Hier werden 2 Versionen präsentiert. Die erste Version schaltet bei Alarmen und Dienstzeiten den Monitor an bzw. wieder aus. Die zweite Version integriert außerdem einen Bewegungsmelder. Hierbei wird zu Dienstzeiten, wenn sich niemand vor dem Monitor befindet, der Bildschirmschoner eingeschaltet. Außerhalb der Dienstzeiten wird bei der Detektion von Bewegung der Monitor eingeschaltet.

Das Folgende ist eine Schritt für Schritt Anleitung, die vom Kauf des Raspberrys bis zum fertigen Monitor geht.

# Raspberry Pi
Dieses Tutorial basiert auf den aktuellen Raspberry 3 B+. Falls noch keiner gekauft wurde, kann bspw. von ABOX ein Komplettpacket mit Ladegerät, SD-Karte und weiterem Zubehör gekauft werden. Als Betriebssystem Image wurde *Raspbian Stretch with desktop* verwendet.

# Erster Start in NOOBS (Dieser Absatz bezieht sich darauf, dass eine SD-Karte mit NOOBS verwendet wird)
Beim ersten Start in NOOBS sollte zuerst eine Internet Verbindung aufgebaut werden (Wlan oder Lan). Dies ist nötig, damit kein veraltetes Image, sondern das aktuelle Rasbian aufgespielt wird. Nun muss Raspbian in der Empfohlenen Version (*Raspbian Stretch with desktop*) ausgewählt werden, sodass NOOBS das aktuelle Raspbian Image installiert.

# Erster Start von Rasbian
Zuerst muss das "Welcome to Raspberry Pi" Tutorial durchlaufen werden mit anschließendem Aktualisieren der Softwarepakete. Dafür muss ebenfalls eine Internetverbindung bestehen. Zum Ende des Tutorials den Raspberry neu starten, wie auch bei der Einrichtung empfohlen wird.

# Installation von Anwendungen
Im Folgenden werden einige Anwendungen benötigt die nun installiert werden. Dafür muss ein Terminal geöffnet werden. Dies kann z.B. durch die Tastenkombination STRG-ALT-t geschehen. Im Terminal muss nun Folgendes eingegeben und mit Enter bestätigt werden.

```sh
sudo apt install jq unclutter cec-utils xscreensaver
```

Jq wird dabei für die Bash Variante des Skripts benötigt. Mittels unclutter wird der Mauszeiger ausgeblendet. Cec-utils wird verwendet um einige Fernsehr ein bzw. aus zu schalten. Xscreensaver wird für die Version mit Bewegungsmelder benötigt.

# Monitor und Bildschirm Befehle hinzufügen
Als nächstes werden bash-Befehle die den Fernseher bzw. den Monitor an/aus schalten können hinzugefügt.
Im Terminal wird nun der Editor *nano* verwendet um eine neue Datei mit folgendem Befehl anzulegen:

```sh
nano .divera_commands.sh
```

In diese Datei kommt der Inhalt der folgenden Datei (am besten copy-paste nutzen und nicht abtippen):


[.divera_commands.sh](.divera_commands.sh)

Hierbei muss die Variable MONITOR die url des Monitores enthalten. Außerdem gibt es, abhängig vom Bildschirm den man ein/aus schalten möchte, mehr oder weniger Probleme. Deshalb wurden hier zwei verschiedene Optionen eingefügt wie sich ein Bildschirm ein bzw. aus schalten lässt. Falls das An-/Ausschalten des Bildschirms Probleme bereitet, kann in der [Problembehandlung](Problembehandlung.md) ein Lösungsansatz gefunden werden.


Mit STRG-o wird eine Datei nach einem weiteren Enter gespeichert und mit STRG-x wird nano verlassen.

Diese Datei enthält die Befehle um den Divera Monitor an

```sh
monitor on
```
und aus zu schalten
```sh
monitor off
```
.
Sowie den Bildschirm an
```sh
screen on
```
und aus zu schalten
```sh
screen off
```
.



Damit die Befehle nun auch im Terminal verwendet werden können, muss die Datei in der bashrc gesourced werden. Dafür wird im Terminal die bashrc geöffnet

```sh
nano .bashrc
```

und am Ende der Datei wird in einer neuen Zeile Folgendes hinzugefügt:

```sh
source .divera_commands.sh
```

Nachdem die Zeile hinzugefügt wurde kann die bashrc im Terminal neu geladen werden mit dem Befehl:

```sh
. ~/.bashrc
```

Nun sollten die vier Kommandos in der bash ausführbar sein (Achtung: Beim Ausführen von ```screen off``` wird der Bildschirm ausgeschaltet und die Eingabe der Tastatur wird nicht mehr erkannt. Deswegen muss, wenn das Kommando aus der Kommandozeile ausgeführt wird, im Anschluss der Raspberry neu gestartet werden).

# Skript hinzufügen

Im Folgenden kann nun zwischen dem Skript mit Bewegungsmelder oder ohne Bewegungsmelder entschieden werden.


[Mit Bewegungsmelder](Motion_Detection.md)


[Ohne Bewegungsmelder](Without_Motion_Detection.md)

Nach dem Hinzufügen des Skripts kann hier fortgefahren werden.

# Autostart einrichten

Damit das Skript nun automatisch startet, muss eine Autostartdatei hinzugefügt werden. Dies geschieht mit folgenden Befehlen:

```sh
cd .config
mkdir -p ./lxsession/LXDE-pi
touch ./lxsession/LXDE-pi/autostart
nano ./lxsession/LXDE-pi/autostart
```

In die Autostartdatei wird folgender Inhalt hinzugefügt:

```sh
# remove the next three diamonds to use the desktop again
#@lxpanel --profile LXDE-pi
#@pcmanfm --desktop --profile LXDE-pi
#point-rpi
# start screensaver
#@xscreensaver -no-splash
# stops displaying mouse after five seconds without moving
@unclutter -display :0 -noevents - grab
# does not allow the raspberry to go to sleep
@xset s off
@xset s noblank
@xset -dpms
#starts script
#./.divera_script.sh
./.divera_script.py
```

Mit dieser veränderten Autostartdatei wird zum einen der Desktop nicht mehr gestartet (dies kann Rückgängig gemacht werden indem die ersten drei Kommandos wieder einkommentiert werden) zum anderen wird der Mauszeiger nach 5 Sekunden ausgeblendet.

Abhängig davon, ob ein Python oder Bash-Skript verwendet wird, muss eine der letzten beiden Zeilen auskommentiert werden. Das heißt, wenn das Python-Skript verwendet wird, darf die Zeile *./.divera_script.py* keine Raute am Anfang enthalten und *#./.divera_script.py* muss mit einer Raute anfangen. Im Falle des Bash-Skripts muss es *#./.divera_script.py* und *./.divera_script.sh* sein.

Wird das Script mit Bewegungsmelder verwendet muss die Zeile *#@xscreensaver -no-splash* auskommentiert werden!


# Problembehandlung

[Übliche Probleme und Lösungsansätze](Problembehandlung.md)
