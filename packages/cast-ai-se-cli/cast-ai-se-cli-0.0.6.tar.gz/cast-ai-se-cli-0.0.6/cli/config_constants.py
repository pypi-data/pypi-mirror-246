CONFIG_TEMPLATE = {
    "CAST": {
        "CASTAI_API_TOKEN": "",
        "DEFAULT_CLUSTER_ID": ""
    },
    "AWS": {
        "AWS_REGION": "",
        "AWS_DEFAULT_NODE_GROUP": "",
        "AWS_ACCESS_KEY": "",
        "AWS_ACCESS_SECRET_KEY": ""
    },
    "AZURE": {
        "CLIENT_ID": "",
        "CLIENT_SECRET": "",
        "TENANT_ID": "",
        "DEFAULT_NODE_GROUP": ""
    },
    "GCP": {},
    "GENERAL": {
        "DEMO_NODE_COUNT": 7,
        "DEMO_REPLICAS": 2,
        "NG_SCALING_TIMEOUT": 300

    },
    "KUBECTL": {
        "DEMO_OFF_CRONJOB": "hibernate-pause"
    }
}

CLI_INPUTS_TEMPLATE = {
    "demo": False,
    "demo_subcommand": "",
    "audit": False,
    "audit_subcommand": "",
    "cluster_id": "",
    "help": False,
    "debug": False
}
