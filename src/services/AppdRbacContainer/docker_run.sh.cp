DOCKER_IMAGE=$1

docker run \
 -e AD_API_WRAPPER_CONTROLLER="REPLACE.saas.appdynamics.com" \
 -e AD_API_WRAPPER_ACCOUNT="REPLACE" \
 -e AD_API_WRAPPER_APIUSER="REPLACE" \
 -e AD_API_WRAPPER_SECRET="REPLACE" \
 -e AD_API_WRAPPER_ENCRYPTION="False" \
 -e AD_RBAC_HANDLER_DAYS="91" \
 -e AD_RBAC_HANDLER_ACCOUNT="REPLACE" \
 -e AD_RBAC_HANDLER_EXCEL="./RBAC-Users.xlsx" \
 -e OPSGENIE_API_WRAPPER_APIKEY="REPLACE" \
 -e OPSGENIE_API_WRAPPER_APIDOMAIN="api.opsgenie.com" \
 -e OPSGENIE_API_WRAPPER_ENCRYPTION="False" \
 -e OPSGENIE_REPORT_ADAPTER_CONTROLLERLINK="https://REPLACE.saas.appdynamics.com/controller/#/location=ACCOUNT_ADMIN_USERS" \
 -e OPSGENIE_REPORT_ADAPTER_ACCOUNT="REPLACE" \
 -e OPSGENIE_REPORT_ADAPTER_SEVERITY="P4" \
 -e OPSGENIE_REPORT_ADAPTER_MESSAGE="Title of Alert" \
 -e OPSGENIE_REPORT_ADAPTER_DESCRIPTION="Account {} Days {} Controller {} Table {}" \
 -e COMMON_BACKGROUND_JOB_TRIGGER="interval" \
 -e COMMON_BACKGROUND_JOB_DAYOFWEEK="" \
 -e COMMON_BACKGROUND_JOB_HOUR="0" \
 -e COMMON_BACKGROUND_JOB_MINUTE="0" \
 -e COMMON_BACKGROUND_JOB_TIMEZONE="Europe/Berlin" \
 -e COMMON_BACKGROUND_JOB_DAYS="0" \
 -e COMMON_BACKGROUND_JOB_HOURS="0" \
 -e COMMON_BACKGROUND_JOB_MINUTES="0" \
 -e COMMON_BACKGROUND_JOB_SECONDS="120" \
 -e LOGGING_LEVEL="INFO" \
 -e LOGGING_REFRESH_RATE="60" \
 $DOCKER_IMAGE