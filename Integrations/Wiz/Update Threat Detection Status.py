import json
import http.client
from SiemplifyAction import SiemplifyAction
from SiemplifyUtils import output_handler
from ScriptResult import EXECUTION_STATE_COMPLETED, EXECUTION_STATE_FAILED

'''
Required parameters for the action:
---------------------------------------------
| AlertId           | Content   | Mandatory |
| ResolutionNote    | Content   | Mandatory |
| Resolution Reason | List      | Mandatory |
| Status Change     | List      | Mandatory |
---------------------------------------------
'''

@output_handler
def main():
    siemplify = SiemplifyAction()

    # Wiz API Credentials
    wiz_client_id = siemplify.extract_configuration_param(provider_name='Wiz', param_name="Wiz Client ID")
    wiz_client_secret = siemplify.extract_configuration_param(provider_name='Wiz', param_name="Wiz Client Secret")
    wiz_issue_host = siemplify.extract_configuration_param(provider_name='Wiz', param_name="Wiz Tenant Host")
    wiz_token_host = "auth.app.wiz.io"

    # Extracting parameters from Siemplify
    wiz_alert_id = siemplify.extract_action_param(param_name="AlertId", print_value=True)
    wiz_resolution_note = siemplify.extract_action_param(param_name="Resolution Note", print_value=True)
    wiz_resolution_reason = siemplify.extract_action_param(param_name="Resolution Reason", print_value=True)
    wiz_status_change = siemplify.extract_action_param(param_name="Status Change", print_value=True)

    if not wiz_alert_id:
        siemplify.LOGGER.error("❌ Missing 'AlertId' action parameter.")
        siemplify.end("❌ Missing 'AlertId' action parameter.", None, EXECUTION_STATE_FAILED)

    if not wiz_resolution_note:
        siemplify.LOGGER.error("❌ Missing 'Resolution Note' action parameter.")
        siemplify.end("❌ Missing 'Resolution Note' action parameter.", None, EXECUTION_STATE_FAILED)

    # Step 1: Obtain Wiz API Token
    try:
        conn = http.client.HTTPSConnection(wiz_token_host)
        token_payload = f"grant_type=client_credentials&audience=wiz-api&client_id={wiz_client_id}&client_secret={wiz_client_secret}"
        token_headers = {
            "accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        conn.request("POST", "/oauth/token", body=token_payload, headers=token_headers)
        res = conn.getresponse()
        if res.status != 200:
            error_message = f"❌ Failed to obtain access token. HTTP Status: {res.status}"
            siemplify.LOGGER.error(error_message)
            siemplify.end(error_message, None, EXECUTION_STATE_FAILED)

        token_data = json.loads(res.read().decode("utf-8"))
        access_token = token_data.get("access_token")
        conn.close()

        if not access_token:
            siemplify.LOGGER.error("❌ No access token received.")
            siemplify.end("❌ Failed to obtain an access token.", None, EXECUTION_STATE_FAILED)

        siemplify.LOGGER.info("✅ Token fetched successfully.")

    except Exception as e:
        siemplify.LOGGER.error(f"❌ Error fetching access token: {str(e)}")
        siemplify.end(f"❌ Error fetching access token: {str(e)}", None, EXECUTION_STATE_FAILED)

    # Step 2: Prepare GraphQL Query to Resolve the Issue
    mutation_query = {
        "query": "mutation UpdateIssue(     $issueId: ID!     $patch: UpdateIssuePatch     $override: UpdateIssuePatch   ) {     updateIssue(input: { id: $issueId, patch: $patch, override: $override }) {       issue {         id         note         status         dueAt         resolutionReason       }     }   }",
        "variables": {
            "issueId": wiz_alert_id,
            "patch": {
                "resolutionReason": wiz_resolution_reason,
                "status": wiz_status_change,
                "resolutionNote": wiz_resolution_note
            }
        }
    }

    # Step 3: Send GraphQL Request to Resolve Issue
    try:
        conn = http.client.HTTPSConnection(wiz_issue_host)
        issue_headers = {
            "Authorization": f"Bearer {access_token}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        conn.request("POST", "/graphql", body=json.dumps(mutation_query), headers=issue_headers)
        res = conn.getresponse()
        response_data = json.loads(res.read().decode("utf-8"))
        conn.close()

        # Check API response
        if res.status != 200 or "errors" in response_data:
            error_message = f"❌ Failed to update issue {wiz_alert_id}: {response_data}"
            siemplify.LOGGER.error(error_message)
            siemplify.end(error_message, None, EXECUTION_STATE_FAILED)

        siemplify.LOGGER.info(f"✅ Issue {wiz_alert_id} successfully marked as resolved.")
        result_value = json.dumps(response_data)

    except Exception as e:
        siemplify.LOGGER.error(f"❌ Failed to update issue {wiz_alert_id}: {str(e)}")
        siemplify.end(f"❌ Failed to update issue {wiz_alert_id}: {str(e)}", None, EXECUTION_STATE_FAILED)

    # Complete Execution
    status = EXECUTION_STATE_COMPLETED
    output_message = f"Issue {wiz_alert_id} resolved successfully."

    siemplify.LOGGER.info(f"\n  status: {status}\n  result_value: {result_value}\n  output_message: {output_message}")
    siemplify.end(output_message, result_value, status)


if __name__ == "__main__":
    main()
