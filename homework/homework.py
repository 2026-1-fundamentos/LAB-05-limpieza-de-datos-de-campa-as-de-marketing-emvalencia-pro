"""
Escriba el codigo que ejecute la accion solicitada.
"""

# pylint: disable=import-outside-toplevel


def clean_campaign_data():
    """
    En esta tarea se le pide que limpie los datos de una campaña de
    marketing realizada por un banco, la cual tiene como fin la
    recolección de datos de clientes para ofrecerls un préstamo.

    La información recolectada se encuentra en la carpeta
    files/input/ en varios archivos csv.zip comprimidos para ahorrar
    espacio en disco.

    Usted debe procesar directamente los archivos comprimidos (sin
    descomprimirlos). Se desea partir la data en tres archivos csv
    (sin comprimir): client.csv, campaign.csv y economics.csv.
    Cada archivo debe tener las columnas indicadas.

    Los tres archivos generados se almacenarán en la carpeta files/output/.

    client.csv:
    - client_id
    - age
    - job: se debe cambiar el "." por "" y el "-" por "_"
    - marital
    - education: se debe cambiar "." por "_" y "unknown" por pd.NA
    - credit_default: convertir a "yes" a 1 y cualquier otro valor a 0
    - mortage: convertir a "yes" a 1 y cualquier otro valor a 0

    campaign.csv:
    - client_id
    - number_contacts
    - contact_duration
    - previous_campaing_contacts
    - previous_outcome: cmabiar "success" por 1, y cualquier otro valor a 0
    - campaign_outcome: cambiar "yes" por 1 y cualquier otro valor a 0
    - last_contact_day: crear un valor con el formato "YYYY-MM-DD",
        combinando los campos "day" y "month" con el año 2022.

    economics.csv:
    - client_id
    - const_price_idx
    - eurobor_three_months



    """
    import glob
    import os
    import zipfile

    import pandas as pd

    # Read all compressed files
    frames = []
    for path in sorted(glob.glob("files/input/bank-marketing-campaing-*.csv.zip")):
        with zipfile.ZipFile(path) as z:
            with z.open(z.namelist()[0]) as f:
                frames.append(pd.read_csv(f))

    df = pd.concat(frames, ignore_index=True)

    os.makedirs("files/output", exist_ok=True)

    # --- client.csv ---
    client = df[["client_id", "age", "job", "marital", "education", "credit_default", "mortgage"]].copy()
    client["job"] = client["job"].str.replace(".", "", regex=False).str.replace("-", "_", regex=False)
    client["education"] = client["education"].str.replace(".", "_", regex=False)
    client["education"] = client["education"].where(client["education"] != "unknown", other=pd.NA)
    client["credit_default"] = client["credit_default"].apply(lambda x: 1 if x == "yes" else 0)
    client["mortgage"] = client["mortgage"].apply(lambda x: 1 if x == "yes" else 0)
    client.to_csv("files/output/client.csv", index=False)

    # --- campaign.csv ---
    month_map = {
        "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
        "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
    }
    campaign = df[["client_id", "number_contacts", "contact_duration",
                   "previous_campaign_contacts", "previous_outcome",
                   "campaign_outcome", "month", "day"]].copy()
    campaign["previous_outcome"] = campaign["previous_outcome"].apply(lambda x: 1 if x == "success" else 0)
    campaign["campaign_outcome"] = campaign["campaign_outcome"].apply(lambda x: 1 if x == "yes" else 0)
    campaign["last_contact_date"] = pd.to_datetime(
        "2022-"
        + campaign["month"].map(month_map).astype(str).str.zfill(2)
        + "-"
        + campaign["day"].astype(str).str.zfill(2)
    ).dt.strftime("%Y-%m-%d")
    campaign = campaign.drop(columns=["month", "day"])
    campaign.to_csv("files/output/campaign.csv", index=False)

    # --- economics.csv ---
    economics = df[["client_id", "cons_price_idx", "euribor_three_months"]].copy()
    economics.to_csv("files/output/economics.csv", index=False)


if __name__ == "__main__":
    clean_campaign_data()
