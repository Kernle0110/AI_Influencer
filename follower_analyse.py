import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Konfiguration
ACCESS_TOKEN = os.getenv("IG_ELIAS_PAGE_TOKEN")
IG_USER_ID = os.getenv("IG_ELIAS_USER_ID")

GRAPH_URL = "https://graph.facebook.com/v18.0"

# Hilfsfunktion zum API-Aufruf mit Fehlerbehandlung
def call_api(endpoint, params=None):
    if params is None:
        params = {}
    params["access_token"] = ACCESS_TOKEN
    url = f"{GRAPH_URL}/{endpoint}"
    print(f"➡️ Calling: {url}")
    response = requests.get(url, params=params)
    print(f"⬅️ Status: {response.status_code}")
    print(f"⬅️ Response: {response.text}")

    if response.status_code != 200:
        try:
            error_info = response.json().get("error", {})
            code = error_info.get("code")
            subcode = error_info.get("error_subcode")
            if code == 3006 and subcode == 2874010:
                print("⚠️ API-Daten nicht verfügbar – vermutlich zu wenig Interaktionen für Demografie-Auswertung.")
                return None
        except Exception:
            pass
        response.raise_for_status()

    return response.json()


# Herkunft der Follower
def get_followers_country():
    data = call_api(f"{IG_USER_ID}/insights", {
        "metric": "follower_demographics",
        "metric_type": "total_value",
        "breakdown": "country",
        "period": "lifetime"
    })

    if data is None:
        return pd.DataFrame()

    results = data["data"][0]["total_value"]["breakdowns"][0]["results"]
    rows = [{"Country": entry["dimension_values"][0], "Followers": entry["value"]} for entry in results]

    df = pd.DataFrame(rows).sort_values(by="Followers", ascending=False)

    sns.barplot(data=df.head(10), x="Followers", y="Country")
    plt.title("Top 10 Länder deiner Follower")
    plt.tight_layout()
    plt.show()

    return df


# Wann sind Follower aktiv
def get_active_times():
    data = call_api(f"{IG_USER_ID}/insights", {
        "metric": "online_followers",
        "period": "lifetime"
    })

    values = data['data'][0].get('values', []) if data else []
    if not values or not values[0].get("value"):
        print("⚠️ Keine Daten für online_followers verfügbar – möglicherweise zu wenige Follower oder noch keine Historie.")
        return pd.DataFrame()

    hourly_data = values[0]["value"]
    df = pd.DataFrame.from_dict(hourly_data, orient="index", columns=["Online Followers"])
    df.index = df.index.astype(int)
    df = df.sort_index()

    df.plot(kind="bar", figsize=(10, 5))
    plt.title("Wann sind deine Follower online (nach Uhrzeit)")
    plt.xlabel("Stunde (0–23)")
    plt.ylabel("Follower online")
    plt.tight_layout()
    plt.show()

    return df


# Altersstruktur und Geschlecht
def get_demographics():
    dfs = []

    for breakdown in ["age", "gender"]:
        data = call_api(f"{IG_USER_ID}/insights", {
            "metric": "engaged_audience_demographics",
            "metric_type": "total_value",
            "timeframe": "this_month",
            "period": "lifetime",
            "breakdown": breakdown
        })

        if data is None:
            print(f"⚠️ Keine Daten für '{breakdown}' verfügbar (API-Einschränkung).")
            continue

        breakdown_data = data.get("data", [])[0].get("total_value", {}).get("breakdowns", [])
        if not breakdown_data:
            print(f"⚠️ Keine Daten für '{breakdown}' verfügbar.")
            continue

        results = breakdown_data[0].get("results", [])

        if breakdown == "age":
            df_age = pd.DataFrame({
                "Age": [r["dimension_values"][0] for r in results],
                "Count": [r["value"] for r in results]
            })
            df_age["Percent"] = df_age["Count"] / df_age["Count"].sum() * 100
            df_age = df_age.sort_values("Age")
            sns.barplot(data=df_age, x="Age", y="Percent")
            plt.title("Altersverteilung interagierender Follower (%)")
            plt.ylabel("Prozent")
            plt.tight_layout()
            plt.show()
            dfs.append(df_age)

        elif breakdown == "gender":
            df_gender = pd.DataFrame({
                "Gender": [r["dimension_values"][0] for r in results],
                "Count": [r["value"] for r in results]
            })
            df_gender["Percent"] = df_gender["Count"] / df_gender["Count"].sum() * 100
            sns.barplot(data=df_gender, x="Gender", y="Percent")
            plt.title("Geschlechterverteilung interagierender Follower (%)")
            plt.ylabel("Prozent")
            plt.tight_layout()
            plt.show()
            dfs.append(df_gender)

    return dfs


# ❤ Engagement-Metriken
def get_engagement():
    metrics = "impressions,reach,likes,comments,saved"
    posts = call_api(f"{IG_USER_ID}/media", {"fields": f"id,caption,media_type,media_url,timestamp,insights.metric({metrics})"})

    if posts is None or "data" not in posts:
        print("⚠️ Keine Posts gefunden oder keine Metriken verfügbar.")
        return pd.DataFrame()

    data_list = []
    for post in posts["data"]:
        if "insights" in post:
            metrics_data = {item["name"]: item["values"][0]["value"] for item in post["insights"]["data"]}
            metrics_data["caption"] = post.get("caption", "")
            metrics_data["timestamp"] = post["timestamp"]
            data_list.append(metrics_data)

    if not data_list:
        print("⚠️ Keine verwertbaren Engagement-Daten.")
        return pd.DataFrame()

    df = pd.DataFrame(data_list)
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df.set_index("timestamp", inplace=True)
    df[["likes", "comments", "reach"]].plot(kind="line", figsize=(12, 6))
    plt.title("Engagement-Trend deiner Posts")
    plt.tight_layout()
    plt.show()

    return df


# Hauptfunktion
def main():
    print("🚀 Instagram Follower Analyse startet ...")
    df_country = get_followers_country()
    df_times = get_active_times()
    df_demo = get_demographics()
    df_engage = get_engagement()
    print("✅ Analyse abgeschlossen.")

    if df_country.empty:
        print("ℹ️ Hinweis: Keine Länderstatistik verfügbar.")
    if df_times.empty:
        print("ℹ️ Hinweis: Keine Online-Zeiten verfügbar.")
    if not df_demo:
        print("ℹ️ Hinweis: Keine Alters-/Geschlechterdaten verfügbar.")
    if df_engage.empty:
        print("ℹ️ Hinweis: Keine Engagement-Daten verfügbar.")

    return df_country, df_times, df_demo, df_engage


if __name__ == "__main__":
    main()
