import http.client
import json
import re
from html.parser import HTMLParser
from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import unix_now, convert_unixtime_to_datetime, output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED

'''
Required Parameters For This Action
-------------------------------------
| Alert Title | Content | Mandatory |
| Description | Content | Mandatory |
| Priority    | List    | Mandatory |
-------------------------------------
'''

class HTMLStripper(HTMLParser):
    """Helper class to strip HTML tags from text."""
    def __init__(self):
        super().__init__()
        self.text = []

    def handle_data(self, data):
        self.text.append(data)

    def get_text(self):
        return ''.join(self.text)


def is_html(text):
    """Checks if a given string contains HTML tags."""
    return bool(re.search(r'<[^>]+>', text))


def strip_html_tags(html):
    """Converts HTML content to plain text."""
    stripper = HTMLStripper()
    stripper.feed(html)
    return stripper.get_text()


@output_handler
def main():
    siemplify = SiemplifyAction()
    json_results = {}

    opsgenie_api_url = "/v2/alerts"
    opsgenie_api_host = "api.opsgenie.com"
    opsgenie_api_key = siemplify.extract_configuration_param(provider_name='OpsGenie', param_name="API Key")

    opsgenie_alert_message = siemplify.extract_action_param(param_name="Alert Title", print_value=True)
    opsgenie_description = siemplify.extract_action_param(param_name="Description", print_value=True)
    opsgenie_tags = siemplify.extract_action_param(param_name="Tags", print_value=True)
    opsgenie_priority = siemplify.extract_action_param(param_name="Priority", print_value=True)

    if not opsgenie_alert_message:
        siemplify.LOGGER.error("❌ Missing 'Alert Title' action parameter.")
        siemplify.end("❌ Missing 'Alert Title' action parameter.", None, EXECUTION_STATE_FAILED)

    if not opsgenie_description:
        siemplify.LOGGER.error("❌ Missing 'Description' action parameter.")
        siemplify.end("❌ Missing 'Description' action parameter.", None, EXECUTION_STATE_FAILED)

    if not opsgenie_priority:
        siemplify.LOGGER.error("❌ Missing 'Priority' action parameter.")
        siemplify.end("❌ Missing 'Priority' action parameter.", None, EXECUTION_STATE_FAILED)

    # Check for HTML in description and convert to plain text if necessary
    if is_html(opsgenie_description):
        opsgenie_description = strip_html_tags(opsgenie_description)

    # Build OpsGenie Payload
    payload = {
        "message": opsgenie_alert_message,
        "description": opsgenie_description,
        "priority": opsgenie_priority,
        "tags": opsgenie_tags.split(",") if opsgenie_tags else []
    }
    siemplify.LOGGER.info("✅ Payload has been loaded.")

    # Build OpsGenie Header
    headers = {
        "Authorization": f"GenieKey {opsgenie_api_key}",
        "Content-Type": "application/json"
    }
    siemplify.LOGGER.info("✅ Header has been loaded.")

    # Create HTTP Connection
    conn = http.client.HTTPSConnection(opsgenie_api_host)

    # Send Request
    try:
        conn.request("POST", opsgenie_api_url, body=json.dumps(payload), headers=headers)
        response = conn.getresponse()
        result = response.read().decode()
        
        json_results = json.loads(result)  # Convert response to JSON

        if response.status != 202:
            siemplify.LOGGER.error(f"❌ API request failed: {json_results}")
            siemplify.end(f"❌ Failed to create OpsGenie alert: {json_results}", None, EXECUTION_STATE_FAILED)

        siemplify.LOGGER.info("✅ OpsGenie Alert Successfully Created.")

        status = EXECUTION_STATE_COMPLETED
        output_message = "OpsGenie alert successfully created."
        result_value = json.dumps(json_results, indent=4)

    except Exception as e:
        siemplify.LOGGER.error(f"❌ Error while sending request: {str(e)}")
        status = EXECUTION_STATE_FAILED
        output_message = f"Error: {str(e)}"
        result_value = None

    finally:
        conn.close()

    # Properly store JSON result in Siemplify
    siemplify.result.add_result_json(json_results)

    siemplify.LOGGER.info("\n  status: {}\n  result_value: {}\n  output_message: {}".format(status, result_value, output_message))
    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
