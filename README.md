### **Aufgabe: CSV-Datei transformieren und abspeichern**

**Ziel:** Erstelle einen Kubernetes Job, der eine CSV-Datei aus einem Persistent Volume liest, die Daten transformiert und sie als neue CSV-Datei speichert.

#### **Schritt-für-Schritt Anleitung:**

1. **Vorbereitung:**
    - Installiere Minikube und starte es, falls noch nicht geschehen.
    - Erstelle ein Persistent Volume (PV) und ein Persistent Volume Claim (PVC), um die CSV-Datei zu speichern.

2. **CSV-Datei erstellen:**
    - Erstelle eine einfache CSV-Datei `data.csv` mit folgendem Inhalt:

    ```csv
    Name,Alter,Stadt
    Alice,30,Berlin
    Bob,25,Hamburg
    Charlie,35,München
    ```

    - Lade diese CSV-Datei in das Persistent Volume, das du später in den Job mountest.

3. **Erstellen des Docker-Images:**
    - Schreibe ein einfaches Python-Skript, das die CSV-Datei transformiert. Zum Beispiel könnte es das Alter um 1 Jahr erhöhen:

    ```python
    import pandas as pd

    # Lade die CSV-Datei
    df = pd.read_csv('/mnt/data/data.csv')

    # Transformation: Alter um 1 Jahr erhöhen
    df['Alter'] = df['Alter'] + 1

    # Speichere die transformierte CSV-Datei
    df.to_csv('/mnt/data/transformed_data.csv', index=False)

    print("CSV transformiert und gespeichert!")
    ```

4. **Dockerfile erstellen:**
    - Erstelle ein einfaches Dockerfile, um das Python-Skript auszuführen.

    ```dockerfile
    FROM python:3.9-slim

    # Installiere pandas
    RUN pip install pandas

    # Kopiere das Skript in den Container
    COPY transform_csv.py /app/transform_csv.py

    # Setze das Arbeitsverzeichnis
    WORKDIR /app

    # Führe das Skript aus
    CMD ["python", "transform_csv.py"]
    ```

    - Baue und pushe das Docker-Image zu einer Registry (z. B. Docker Hub oder Minikube's lokalem Docker-Registry).

    ```bash
    docker build -t <dein-username>/csv-transformer .
    docker push <dein-username>/csv-transformer
    ```

5. **Kubernetes Job erstellen:**
    - Erstelle ein Kubernetes Job YAML, das das Docker-Image nutzt und das Persistent Volume einbindet.

    ```yaml
    apiVersion: batch/v1
    kind: Job
    metadata:
      name: csv-transform-job
    spec:
      template:
        spec:
          containers:
            - name: csv-transformer
              image: <dein-username>/csv-transformer:latest
              volumeMounts:
                - name: csv-volume
                  mountPath: /mnt/data
          volumes:
            - name: csv-volume
              persistentVolumeClaim:
                claimName: csv-pvc
          restartPolicy: Never
      backoffLimit: 4
    ```

    - Stelle sicher, dass der Job das PVC einbindet und auf das Verzeichnis `/mnt/data` zugreift.

6. **Erstellen des Persistent Volume (PV) und Persistent Volume Claim (PVC):**
    - Erstelle ein Persistent Volume und Persistent Volume Claim, um die CSV-Datei zu speichern.

    ```yaml
    apiVersion: v1
    kind: PersistentVolume
    metadata:
      name: csv-pv
    spec:
      capacity:
        storage: 1Gi
      accessModes:
        - ReadWriteOnce
      hostPath:
        path: /mnt/data
    ```

    ```yaml
    apiVersion: v1
    kind: PersistentVolumeClaim
    metadata:
      name: csv-pvc
    spec:
      accessModes:
        - ReadWriteOnce
      resources:
        requests:
          storage: 1Gi
    ```

7. **Durchführung der Aufgabe:**
    - Wende alle YAML-Dateien an, um die Ressourcen in Minikube zu erstellen:
    
    ```bash
    kubectl apply -f pv.yaml
    kubectl apply -f pvc.yaml
    kubectl apply -f job.yaml
    ```

8. **Überprüfung:**
    - Überprüfe den Status des Jobs mit:
    
    ```bash
    kubectl get jobs
    ```

    - Überprüfe die Logs des Jobs:
    
    ```bash
    kubectl logs -l job-name=csv-transform-job
    ```

    - Überprüfe, ob die transformierte Datei erfolgreich gespeichert wurde:
    
    ```bash
    kubectl cp <pod-name>:/mnt/data/transformed_data.csv ./transformed_data.csv
    cat transformed_data.csv
    ```

---

### **Erwartetes Ergebnis:**
Die CSV-Datei wird transformiert und gespeichert. Die Alterswerte in der transformierten Datei sollten um 1 Jahr erhöht sein.

---

### **Zusätzliche Aufgaben:**
- Füge eine Fehlerbehandlung im Python-Skript hinzu, falls die CSV-Datei nicht gefunden wird.
- Integriere eine komplexere Transformation (z. B. Berechnungen, Filterung).

---
