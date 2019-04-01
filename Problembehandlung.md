# Problembehandlung

# Schwarze Ränder am Bildschirm:

Falls am Rand des Bildschirms schwarze Ränder vorkommen, führe folgendes Kommando aus:

```sh
sudo nano /boot/config.txt
```

Entferne dort die # vor der folgenden Zeile:

```sh
#disable_overscan=1 
```

Nach einem Neustarten des Raspberrys sollten keine schwarzen Ränder mehr vorhanden sein.

Falls dennoch welche vorhanden sein sollten oder zu wenig Rand vorhanden sein sollte, kann dieser manuell in der Datei angepasst werden. Dazu wird die config-Datei wieder geöffnet:

```sh
sudo nano /boot/config.txt
```

Die folgenden Zeilen müssen auskommentiert werden und die Werte manuell geändert werden.

```sh
#overscan_left=16
#overscan_right=16
#overscan_top=16
#overscan_bottom=16
```

Nach einem Neustarten werden die Änderungen sichtbar. Achtung: Nach jedem Ändern der Werte muss der Raspberry neu gestartet werden um die Änderung sichtbar zu machen.

# Bildschirm geht nicht aus:

Obwohl der Bildschirm ausgehen müsste, also kein Dienst ist (und keine Bewegung detektiert wurde), bleibt er an. Dies ist ein häufiges Problem bei älteren Fernsehern, die das Ein/Ausschalten des HDMI-Ports nicht erkennen. Um dies zu Beheben ist im ``` .divera_commands.sh ``` eine weitere Option, mit der es funktionieren kann. Hierbei werden cec-Signale an den Fernseher gesendet, allerdings unterstützen auch nicht alle Fernseher alle cec-Signale. Dies entspricht der Version 2 im Quellcode. Um dies zu verwenden muss die Version 1 einkommentiert und Version 2 auskommentiert werden (dies ist beim Ein/Ausschalten im Quellcode notwendig, also 2 Positionen im Quellcode).

Außerdem wurde hier noch ein manuelles Umschalten auf den HDMI-Port 1 hinzugefügt, falls der Fernseher standardmäßig auf einem anderen Eingang ist. Das heißt, dass der Monitor zwingend an HDMI-Port 1 angeschlossen werden muss oder der Port im Quellcode geändert werden muss. Das Umschalten des HDMI-Ports ist nicht in der cec-Spezifikation vorhanden, das heißt, dass dies ebenso nicht jeder Fernseher unterstützen muss. Dies entspricht der Version 2b und muss Zusätzlich zu Version 2 auskommentiert werden.

