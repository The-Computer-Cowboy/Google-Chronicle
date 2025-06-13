from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED, EXECUTION_STATE_TIMEDOUT
import http.client
import json

'''
Required Paramters For This Action
---------------------------------------
| Request ID  | Content   | Mandatory |
---------------------------------------
'''

@output_handler
def main():
    siemplify = SiemplifyAction()
    json_results = {}

    opsgenie_api_url = "/v2/alerts/requests"
    opsgenie_api_host = "api.opsgenie.com"
    opsgenie_api_key = siemplify.extract_configuration_param(provider_name='OpsGenie', param_name="API Key")

    opsgenie_requestId = siemplify.extract_action_param(param_name="RequestId", print_value=True)

    if not opsgenie_requestId:
        siemplify.LOGGER.error("❌ Missing 'RequestId' action parameter.")
        siemplify.end("❌ Missing 'RequestId' action parameter.", None, EXECUTION_STATE_FAILED)

    full_url = f"{opsgenie_api_url}/{opsgenie_requestId}"  # ✅ Fixed missing closing quote

    siemplify.LOGGER.info(f"✅ Full URL Created: {full_url}")

    # ✅ Build OpsGenie Headers
    headers = {  # ✅ Fixed typo from "header" to "headers"
        "Authorization": f"GenieKey {opsgenie_api_key}"
    }

    siemplify.LOGGER.info("✅ Headers have been set.")

    # Establish Connection
    conn = http.client.HTTPSConnection(opsgenie_api_host)

    try:
        # Make the API request
        conn.request("GET", full_url, headers=headers)
        response = conn.getresponse()
        response_data = response.read().decode()  # ✅ Read and decode response

        if response.status != 200:
            siemplify.LOGGER.error(f"❌ API request failed: {response_data}")
            siemplify.end(f"❌ Failed to get request status from OpsGenie: {response_data}", None, EXECUTION_STATE_FAILED)

        json_results = json.loads(response_data)  # ✅ Properly parse JSON response
        siemplify.LOGGER.info("✅ OpsGenie Get Request Status Successfully Retrieved.")

    except Exception as e:
        siemplify.LOGGER.error(f"❌ Exception: {str(e)}")
        siemplify.end(f"❌ Exception occurred: {str(e)}", None, EXECUTION_STATE_FAILED)

    finally:
        conn.close()

    status = EXECUTION_STATE_COMPLETED  # Flag to indicate action completion
    output_message = "OpsGenie request status successfully retrieved."
    result_value = json.dumps(json_results, indent=4)  # ✅ Return formatted JSON

    siemplify.result.add_result_json(json_results)

    siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status, result_value, output_message))
    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
