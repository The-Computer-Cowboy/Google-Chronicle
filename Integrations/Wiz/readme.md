# Wiz Integrations for Google Chronicle

This repository contains a collection of Python scripts designed to function as custom "actions" within Google Chronicle. These scripts leverage the Wiz API to enable seamless interaction between your Google Chronicle security detections and your Wiz cloud security environment, facilitating automated workflows and enriching your investigation context.

## Overview

As security events are detected and investigated in Google Chronicle, it's crucial to correlate them with your cloud security posture and active threats managed in Wiz. These integrations bridge that gap, allowing you to trigger actions in Wiz directly from the Chronicle playbook or case. This empowers security teams to manage Wiz issues and gather contextual data without leaving their primary investigation platform.

Each script is a self-contained action that performs a specific, authenticated task against the Wiz GraphQL API.

## Features

This collection currently includes the following actions:

- **1. Update Threat Detection Issues (`Update Threat Detection Status.py`)**
    
    - This powerful script allows you to modify the status of existing issues within Wiz. For example, you can change an issue's status to `OPEN`, `IN-PROGRESS`, or `RESOLVED`. This is ideal for creating automated workflows where a remediation action confirmed in Chronicle automatically updates the corresponding security issue in Wiz.
        
- **2. Get Issues (`Get Issue.py`)**
    
    - This script queries the Wiz API to retrieve an issue based on specified wiz issue ID. This action is invaluable for enriching a Chronicle investigation by pulling in related cloud security findings from Wiz to provide a more complete picture of a potential threat.
        

## Prerequisites

To successfully deploy and use these integrations, you will need:

- An active **Google Chronicle** instance with permissions to add and execute custom actions.
    
- An active **Wiz** tenant.
    
- A **Wiz Service Account** with the necessary permissions to read and update issues. This will include a **Client ID** and a **Client Secret**.
    

## Authentication

The scripts are designed to handle Wiz's OAuth 2.0 authentication flow automatically.

1. The script first makes a request to the Wiz authentication endpoint (`https://auth.wiz.io/oauth/token`) using the provided Client ID and Client Secret.
    
2. It receives a JWT (JSON Web Token) upon successful authentication.
    
3. This JWT is then used as a bearer token in the `Authorization` header for all subsequent requests to the Wiz GraphQL API.
    

The scripts manage the token acquisition process internally; you only need to provide the credentials securely.

## Setup & Configuration

Follow these steps to configure the actions in your Google Chronicle environment.

1. **Store Your API Key in Chronicle Integration via Parameters:**
    
    - Create an integration named Wiz in the IDE tab under Response inside the Chronicle UI.
        
    - For security, never hard-code your Wiz secrets directly in the scripts.
        
    - Create three new parameters:
        
        - `WIZ CLIENT ID`: Store your Wiz Service Account Client ID here.
            
        - `WIZ CLIENT SECRET`: Store your Wiz Service Account Client Secret here.
        
        - `WIZ Tenant Host`: Store your Wiz Tenant host here.
            
    - The scripts are written to read these credentials from environment variables, which Chronicle securely provides to the action at runtime.
        
2. **Upload the Python Scripts:**
    
    - In your Chronicle instance, navigate to the custom actions management page.
        
    - Upload each Python script (`Update Threat Detection Issues.py`, `Get Issues.py`) as a new, distinct action.
        
3. **Configure Action Parameters:**
    
    - For each action, you must define its parameters. These are the inputs the script expects.
        
    - **For `Update Threat Detection Issues.py`**, you will need to define parameters for the `issue_id` and the `status` you wish to set.
        
    - **For `Get Issues.py`**, you will need to configure a parameter for  `wiz alert id`.
        
    - Map these parameters to fields from Chronicle events or allow them to be entered manually when the action is run.
        
    - Crucially, ensure each action is configured to have access to the `WIZ CLIENT ID` and `WIZ CLIENT SECRET` secrets you created.
        

## Usage

Once configured, these actions can be triggered from playbooks or as a manual action on a case.

### Example: Updating an Issue Status

1. An analyst in Chronicle investigates an event related to a vulnerable VM and confirms that a patch has been deployed.
    
2. The analyst finds the associated Wiz Issue ID from a previous alert or by using the `Get Issues.py` action.
    
3. They trigger the **"Update Threat Detection Issues"** action, providing the Wiz Issue ID and setting the new status to `RESOLVED`.
    
4. The script authenticates to Wiz, sends the mutation request, and the issue is updated in the Wiz portal, closing the loop.
    

### Example: Getting Issue Context

1. A detection fires in Chronicle for suspicious network activity from a specific cloud resource.
    
2. To understand the security posture of this resource, the analyst triggers the **"Get Issues"** action, passing the resource name as a filter.
    
3. The action returns a list of all open, critical-severity issues in Wiz related to that resource, giving the analyst immediate, valuable context for their investigation.
    

## Contributing

Contributions are highly encouraged! If you have suggestions for improving these scripts or would like to add new Wiz actions to the collection, please fork the repository and submit a pull request for review.

## License

This project is licensed under the [MIT License](LICENSE "null").
