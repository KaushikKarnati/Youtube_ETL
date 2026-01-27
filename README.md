# YouTube Data Engineering Project 🚀

## 📖 Project Overview
Welcome! This project is a hands-on example of a **Data Engineering Pipeline**. It automates the process of collecting data from YouTube, cleaning it, and storing it for analysis.

**Goal:** To track the performance (views, likes, comments) of videos from a specific YouTube channel over time, completely automatically.

**Why is this cool?**
Instead of manually checking a YouTube channel every day and writing down numbers in a spreadsheet, this code does it for you! It demonstrates how companies handle data at scale using professional tools.

---

## 📂 Project Structure
Here is how the project is organized. Understanding the folder structure is key to understanding how the pieces fit together.

```bash
Youtube_Data_Engineering/
├── dags/                       # ⚡️ Airflow Directed Acyclic Graphs (The "Workflows")
│   ├── api/                    #    - Code to talk to YouTube API
│   │   └── video_stats.py      #      - Fetches data from YouTube
│   ├── datawarehouse/          #    - Code to talk to the Database
│   │   ├── data_wh.py          #      - Main logic for database updates
│   │   └── ...                 #      - Helper scripts (loading, transforming data)
│   └── main.py                 #    - The main Airflow configuration file defining the DAGs
├── data/                       # 💾 Local storage for raw JSON files (Staging area)
├── docker/                     # 🐳 Docker configuration files
│   └── postgres/               #    - Database initialization scripts
├── logs/                       # 📝 Airflow logs (for debugging)
├── docker-compose.yaml         # ⚙️ Defines all the services (Airflow, Postgres, Redis)
├── requirements.txt            # 📦 Python dependencies
└── .env                        # 🔑 Secrets (API Keys, Passwords) - DO NOT SHARE THIS!
```

---

## 🛠 Tech Stack & Key Concepts

This project uses industry-standard tools. Here is what they do:

-   **Apache Airflow**: The "Traffic Controller". It schedules tasks (e.g., "Run this script every day at 2 PM").
    -   *Concept*: **DAG (Directed Acyclic Graph)** - A collection of tasks organized in a specific order.
-   **Docker**: The "Container". It packages the software so it runs exactly the same on my machine and yours.
-   **PostgreSQL**: The "Warehouse". A powerful database where we store the structured data.
-   **Metabase**: The "Dashboard". A tool to visualize the data with charts and graphs.
-   **YouTube Data API**: The "Source". Google's official way for developers to get YouTube data.
-   **ETL (Extract, Transform, Load)**: The core process:
    1.  **Extract**: Get data from YouTube.
    2.  **Transform**: Clean up the data (fix dates, remove bad rows).
    3.  **Load**: Save it into the database.

---

## ⚙️ How It Works (The Pipeline)

The project runs two main workflows (DAGs) defined in `dags/main.py`:

### 1. The Extraction DAG (`produce_json`)
*Runs daily at 14:00 UTC*
1.  **Get Playlist**: Finds the "Uploads" playlist for the specified channel.
2.  **Get Video IDs**: Lists all videos in that playlist.
3.  **Extract Data**: Calls the YouTube API for every video to get current stats (Views, Likes, Comments).
4.  **Save to JSON**: Dumps this raw data into a file in the `data/` folder.
    *   *Why JSON?* It's a standard format for raw data exchange.

### 2. The Loading DAG (`update_db`)
*Runs daily at 15:00 UTC (1 hour later)*
1.  **Read JSON**: Picks up the file created by the first DAG.
2.  **Staging Table**: Dumps the raw data into a temporary table (`staging`).
    *   *Why Staging?* If something goes wrong, we have a copy of the raw data before we mess with it.
3.  **Core Table**: Cleans the data and moves it to the final table (`core`).
    *   *Logic*: It checks if the video already exists. If yes, it updates the stats. If no, it inserts a new row.

---

## 🚀 Setup & Run Instructions

### Prerequisites
-   **Docker Desktop** installed and running.
-   A **Google Cloud Account** to get an API Key.

### Step 1: Get a YouTube API Key
1.  Go to [Google Cloud Console](https://console.cloud.google.com).
2.  Create a project and enable **YouTube Data API v3**.
3.  Create an **API Key**.

### Step 2: Configure Environment
Create a file named `.env` in the project root folder. Add your keys:
```bash
API_KEY=your_copied_api_key_here
CHANNEL_HANDLE=@YourFavoriteChannel
# Database configs (defaults usually work for local dev)
POSTGRES_USER=airflow
POSTGRES_PASSWORD=airflow
```

### Step 3: Launch!
Open your terminal in the project folder and run:
```bash
docker-compose up -d
```
*   `up`: Start the services.
*   `-d`: Detached mode (runs in the background).

### Step 4: Monitor
Open your browser to `http://localhost:8080`.
-   **Username**: airflow
-   **Password**: airflow

You will see your DAGs! Toggle them to "On" to start the schedule.

### Step 5: Visualize Data (Metabase)
1.  Open `http://localhost:3000`.
2.  Click **"Let's get started"**.
3.  Connect to your database:
    *   **Database Type**: PostgreSQL
    *   **Name**: YouTube Data
    *   **Host**: `postgres`
    *   **Port**: `5432`
    *   **Database Name**: `youtube_data` (or check your `.env` for `ELT_DATABASE_NAME`)
    *   **Username**: `airflow`
    *   **Password**: `airflow`
4.  Click **Next** and start exploring!

### Step 6: Advanced Analytics (SQL)
Use these SQL queries in Metabase to unlock deeper insights:

**1. Engagement Rate (Are people interacting?)**
```sql
SELECT
    "Upload_Date",
    "Video_Title",
    (("Likes_Count" + "Comments_Count") * 100.0 / NULLIF("Video_Views", 0)) AS engagement_rate_pct
FROM core.yt_data
ORDER BY "Upload_Date" ASC;
```

**2. Love Ratio (Likes vs Views)**
```sql
SELECT
    "Video_Title",
    ("Likes_Count" * 100.0 / NULLIF("Video_Views", 0)) AS like_ratio_pct
FROM core.yt_data
ORDER BY like_ratio_pct DESC
LIMIT 20;
```

**3. Views vs Duration (Do shorter videos win?)**
```sql
SELECT
    "Video_Title",
    "Video_Views",
    (EXTRACT(EPOCH FROM "Duration") / 60) AS duration_minutes
FROM core.yt_data
WHERE "Video_Views" > 0;
```
