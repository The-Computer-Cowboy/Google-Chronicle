from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED, EXECUTION_STATE_TIMEDOUT
import http.client
import json

'''
Required Parameters For This Action
---------------------------------------
| Alert ID    | Content   | Mandatory |
| Alert Note  | Content   | Mandatory |
| Email       | List      | Mandatory |
---------------------------------------
'''

@output_handler
def main():
    siemplify = SiemplifyAction()

    opsgenie_id = siemplify.extract_action_param(param_name="OpsGenie Alert ID", print_value=True)
    opsgenie_note = siemplify.extract_action_param(param_name="Alert Note", print_value=True)
    opsgenie_email = siemplify.extract_action_param(param_name="Security Engineer Email", print_value=True)

    if not opsgenie_id:
        siemplify.LOGGER.error("❌ Missing 'OpsGenie Alert ID' action parameter.")
        siemplify.end("❌ Missing 'OpsGenie Alert ID' action parameter.", None, EXECUTION_STATE_FAILED)

    if not opsgenie_note:
        siemplify.LOGGER.error("❌ Missing 'Alert Note' action parameter.")
        siemplify.end("❌ Missing 'Alert Note' action parameter.", None, EXECUTION_STATE_FAILED)

    if not opsgenie_email:
        siemplify.LOGGER.error("❌ Missing 'Security Engineer Email' action parameter.")
        siemplify.end("❌ Missing 'Security Engineer Email' action parameter.", None, EXECUTION_STATE_FAILED)

    # ✅ Corrected API URL formatting
    opsgenie_api_url = f"/v2/alerts/{opsgenie_id}/close"
    opsgenie_api_host = "api.opsgenie.com"
    opsgenie_api_key = siemplify.extract_configuration_param(provider_name='OpsGenie', param_name="API Key")

    # ✅ Corrected Payload Formatting
    payload = json.dumps({
        "user": opsgenie_email,
        "note": opsgenie_note
    })

    # ✅ Fixed Header Key
    headers = {
        "Authorization": f"GenieKey {opsgenie_api_key}",
        "Content-Type": "application/json"
    }

    # Create HTTP Connection
    conn = http.client.HTTPSConnection(opsgenie_api_host)

    try:
        # ✅ Fixed incorrect 'header' argument
        conn.request("POST", opsgenie_api_url, body=payload, headers=headers)
        response = conn.getresponse()
        result = response.read().decode()

        if response.status != 202:
            siemplify.LOGGER.error(f"❌ API Request Failed: {result}")
            siemplify.end(f"❌ Failed to close OpsGenie alert: {result}", None, EXECUTION_STATE_FAILED)

        siemplify.LOGGER.info("✅ OpsGenie Alert Successfully Closed.")

    except Exception as e:
        siemplify.LOGGER.error(f"❌ Exception: {str(e)}")
        siemplify.end(f"❌ Exception occurred: {str(e)}", None, EXECUTION_STATE_FAILED)

    finally:
        conn.close()

    status = EXECUTION_STATE_COMPLETED  # Flag back to Siemplify
    output_message = "OpsGenie alert successfully closed."
    result_value = json.dumps(result, indent=4)  # ✅ Return JSON response

    siemplify.result.add_result_json(json.loads(result))

    siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status, result_value, output_message))
    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
