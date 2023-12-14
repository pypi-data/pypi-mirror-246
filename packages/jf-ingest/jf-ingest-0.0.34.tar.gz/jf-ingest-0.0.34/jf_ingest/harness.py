import os
import logging
import urllib3
import sys
import yaml
from datetime import datetime

from jf_ingest.file_operations import IngestIOHelper
from jf_ingest.jf_jira.auth import JiraConfig
from jf_ingest.jf_jira import IngestionConfig, load_and_push_jira_to_s3


def setup_harness_logging(logging_level: int):
    logging.basicConfig(
        level=logging_level,
        format="%(asctime)s %(threadName)s %(levelname)s %(name)s %(message)s"
        if logging_level == logging.DEBUG
        else "%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    logging.getLogger(urllib3.__name__).setLevel(logging.WARNING)


# NOTE: This is a work in progress developer debugging tool.
# it is currently run by using the following command:
#   pdm run ingest_harness
# and it requires you to have a creds.env and a config.yml file at
# the root of this project
if __name__ == "__main__":
    debug_mode = "--debug" in sys.argv

    # Get Config data for Ingestion Config
    with open("./config.yml") as yaml_file:
        yaml_data = yaml.safe_load(yaml_file)
        general_config_data = yaml_data["general"]
        jira_config_data = yaml_data["jira"]
        jira_config_data["work_logs_pull_from"] = (
            datetime.strptime(jira_config_data["work_logs_pull_from"], "%Y-%m-%d")
            if jira_config_data["work_logs_pull_from"]
            else datetime.min
        )
        ingest_config = IngestionConfig(
            timestamp=datetime.utcnow().strftime('%Y%m%d_%H%M%S'),
            jellyfish_api_token=os.getenv('JELLYFISH_API_TOKEN'),
            **general_config_data,
        )
        ingest_config.company_slug = os.getenv("COMPANY_SLUG"),
        jira_config = JiraConfig(**jira_config_data)
        jira_config.url = os.getenv("JIRA_URL")
        jira_config.user = os.getenv("JIRA_USERNAME")
        jira_config.password = os.getenv("JIRA_PASSWORD")
        ingest_config.local_file_path = f"{ingest_config.local_file_path}/{ingest_config.timestamp}"
        # Inject auth data into config
        ingest_config.jira_config = jira_config
        if ingest_config.jira_config.earliest_issue_dt == None:
            print(
                "earliest_issue_dt option in config.yml detected as being null, setting to datetime.min!"
            )
            ingest_config.jira_config.earliest_issue_dt = datetime.min

    setup_harness_logging(logging_level=logging.DEBUG if debug_mode else logging.INFO)

    load_and_push_jira_to_s3(ingest_config)
