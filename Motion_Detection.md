Dieses Skript ließt, im Gegensatz zum normalen Skript, einen angeschlossenen Bewegungsmelder aus. Dies wird dazu genutzt, um in Dienstzeiten, wenn niemand vor dem Monitor steht, einen Bildschirmschoner anzuzeigen und außerhalb von Dienstzeiten bei einer Bewegung den Monitor einzuschalten. Außerdem werden in diesem Skript Alarme, die das Wort "Probealarm" enthalten, explizit nicht als Alarm behandelt.

# Skript einrichten

Zu Beginn muss die Skript-Datei angelegt und befüllt werden. Dies geschieht mit Folgenden Terminalbefehl:

```sh
nano .divera_script.py
```

Weiter ist folgendes Skript einzufügen:

[.divera_script_motion.py](.divera_script_motion.py)

In dem Skript muss noch der Accesskey hinzugefügt werden und die Dienstzeiten müssen angepasst werden.

Nachdem das Skript hinzugefügt wurde, muss es mit folgendem Befehl noch ausführbar gemacht werden:

```sh
chmod +x .divera_script.py
```

Das Skript kann nun im Terminal mit folgenden Befehl aufgerufen werden:

```sh
./.divera_script.py
```

Damit das Skript funktioniert, muss noch der Bewegungsmelder angeschlossen werden und der Bildschirmschoner eingerichtet werden.

# Bewegungsmelder:

Zum einem wird der Bewegungsmelder benötigt. Dieser kann zum Beispiel [hier](https://www.amazon.de/gp/product/B01N3QE4TQ/ref=ppx_yo_dt_b_asin_title_o03_s00?ie=UTF8&psc=1) oder [hier](https://www.amazon.de/gp/product/B008AESDSY?ie=UTF8&linkCode=as2&camp=1634&creative=6738&tag=754-21&creativeASIN=B008AESDSY) erworben werden. Dazu werden noch Jumperkabel zum Verbinden benötigt. Der Anschluss der Kabel kann aus dem Abbild von [diesem](https://tutorials-raspberrypi.de/raspberry-pi-bewegungsmelder-sensor-pir/) Tutorial entnommen werden. Eine detalierte Beschreibung des Sensors ist [hier](http://elektro.turanis.de/html/prj108/index.html) zu finden. Beim Sensor sollte der Jumper set auf High gesetzt werden. Die Time On und Sensitivität müssen abhängig vom Ort des Sensors eingestellt werden.

# Bildschirmschoner:

Außerdem muss noch der Bildschirmschoner eingerichtet werden. Als Bildschirmschoner kann bspw. xscreensaver verwendet und nach Wünschen eingerichtet werden. Die Einstellungen können unter Start->Einstellungen->Bildschirmschoner gesetzt werden. Beim ersten Start muss der xscreensaver-Prozess, wie im Pop-Up empfohlen, gestartet werden. Mittels
```sh
sudo apt install xscreensaver-gl-extra
```
wird unter anderem der Bildschirmschoner GLSlideshow installiert mit dem eine einfach Slideshow von Bildern angezeigt werden kann.
