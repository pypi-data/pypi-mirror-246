import logging
import time

from models.config import ConfigObject
from orchestrators.base_orch import BaseOrchestrator

from cast_ai.se.contollers.castai_controller_svc import CastController


class AuditOrchestrator(BaseOrchestrator):
    def __init__(self, cfg: ConfigObject):
        super().__init__(cfg)
        self._logger = logging.getLogger(__name__)
        cid = cfg.custom_cid if cfg.custom_cid else cfg.app_config["CAST"]["DEFAULT_CLUSTER_ID"]

        self._cast_ctrl = CastController(cfg.app_config["CAST"]["CASTAI_API_TOKEN"], cid)

        self.audit_subcommand_mapping = {
            "analyze": self.audit_analyze_sequence,
        }

    def execute(self) -> None:
        subcommand = self._cfg.app_inputs["audit_subcommand"]
        if subcommand in self.audit_subcommand_mapping:
            self.audit_subcommand_mapping[subcommand]()
        else:
            raise ValueError(f'Invalid option: {subcommand}')

    def audit_analyze_sequence(self):

        start_time = time.time()
        try:
            audit_logs = self._cast_ctrl.get_audit()
            # "eventType": "addBlacklistExecuted"
            errors = list(filter(lambda x: "error" in x.get("event", {}), audit_logs["items"]))
            print("----------------Found errors----------------")
            for x in errors:
                event_type = x["eventType"]
                event_id = x["id"]
                error_details = x["event"]["error"]["details"]
                print(f"| {event_id} | {event_type} | {error_details} |")
            # Print the filtered data
            # print(errors)
        except Exception as e:
            self._logger.error(f"Something went wrong:[{str(e)}]")
        print(f"It took {int(time.time() - start_time)} seconds to analyze")
