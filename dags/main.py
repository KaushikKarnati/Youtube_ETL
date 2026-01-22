from airflow import DAG
import pendulum
from datetime import datetime, timedelta
from api.video_stats import *

local_tz = pendulum.timezone("UTC")
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    # 'retries': 1,
    # 'retry_delay': timedelta(minutes=5),
    'max_active_runs': 1,
    'dagrun_timeout': timedelta(minutes=60),
    'start_date': datetime(2025, 1, 1, tzinfo=local_tz),

}
with DAG(
    dag_id = 'produce_json',
    default_args = default_args,
    description= 'Produce JSON file with video stats from YouTube API',
    schedule='0 14 * * *',  # At 14:00 (2 PM) UTC every day
    catchup=False) as dag:
    playlist_id = get_playslist_id()
    video_ids = get_videoIDs(playlist_id)
    extracted_data = extract_video_data(video_ids)
    save_to_json_task = save_to_json(extracted_data)
    playlist_id >> video_ids >> extracted_data >> save_to_json_task



