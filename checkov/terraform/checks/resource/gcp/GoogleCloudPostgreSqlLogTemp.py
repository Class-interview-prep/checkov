from checkov.common.models.enums import CheckResult, CheckCategories
from checkov.terraform.checks.resource.base_resource_check import BaseResourceCheck


class GoogleCloudPostgreSqlLogTemp(BaseResourceCheck):
    def __init__(self):
        name = "Ensure PostgreSQL database 'log_temp_files flag is set to '0'"
        check_id = "CKV_GCP_56"
        supported_resources = ['google_sql_database_instance']
        categories = [CheckCategories.LOGGING]
        super().__init__(name=name, id=check_id, categories=categories, supported_resources=supported_resources)

    def scan_resource_conf(self, conf):
        """
            Looks for google_sql_database_instance which allows slog temp files set to '0' on PostgreSQL DBs::
            :param
            conf: google_sql_database_instance
            configuration
            :return: < CheckResult >
        """
        if 'database_version' in conf.keys():
            key = conf['database_version'][0]
            if 'POSTGRES' in key:
                if 'settings' in conf.keys():
                    for attribute in conf['settings'][0]:
                        if attribute == 'database_flags':
                            for flag in conf['settings'][0]['database_flags']:
                                if (flag['name'][0] == 'log_temp_files') and (flag['value'][0] != '0'):
                                    return CheckResult.FAILED
        return CheckResult.PASSED


check = GoogleCloudPostgreSqlLogTemp()
