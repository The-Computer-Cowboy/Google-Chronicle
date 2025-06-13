# OpsGenie Integrations for Google Chronicle

This repository contains a collection of Python scripts designed to act as integrations, or "actions," within Google Chronicle. These scripts allow you to seamlessly interact with the OpsGenie API directly from the Chronicle platform, enabling you to automate alert management workflows as part of your security operations.

## Overview

When responding to threats detected in Google Chronicle, it's often necessary to create, manage, and track alerts in an incident management platform like OpsGenie. These scripts bridge that gap by providing a direct line of communication from Chronicle to OpsGenie. Each script is a self-contained action that can be triggered within Chronicle to perform a specific task in your OpsGenie account.

## Features

This collection currently includes the following actions:

- **1. Create OpsGenie Alert (`create_alert.py`)**
    
    - This script takes input parameters (such as a alert title, description and priority) and uses them to create a new alert in OpsGenie. This is perfect for escalating a notable event from Chronicle into a formal incident response workflow.
        
- **2. Close OpsGenie Alert (`close_alert.py`)**
    
    - This script allows you to close an existing alert in OpsGenie. You can target a specific alert using its Alert ID. This is useful for automatically resolving alerts when a threat has been remediated or determined to be a false positive.
        
- **3. Get Request Status (`get_request_status.py`)**
    
    - When an action is performed (like creating or closing an alert), OpsGenie returns a request ID. This script takes that request ID as input and queries the OpsGenie API to check the status of the initial request, confirming whether it was successful. This is important since OpsGenie is asynchronous and will not provide the Alert ID after using the Create OpsGenie Alert action.
        

## Prerequisites

Before you can use these integrations, you will need the following:

- An active **Google Chronicle** instance with permissions to configure and run actions.
    
- An active **OpsGenie** account with permissions to create and manage API keys.
    
- An **OpsGenie API Key** with sufficient permissions to create and close alerts.
    

## Setup & Configuration

Follow these steps to configure the actions in your Google Chronicle environment.

1. **Store Your API Key in Chronicle Integration Created via Parameters:**
    - Create an integration named OpsGenie in the IDE tab under Response inside the Chronicle UI.
        
    - For security, never hard-code your OpsGenie API key directly in the scripts.
        
    - Create a new parameter named API Key in the Integration configuration. Name this parameter whatever you like. You will want to mark this field as a password as this will obfuscate the API key.
        
2. **Upload the Python Scripts:**
    
    - In Google Chronicle, navigate to the section for managing custom actions.
        
    - Upload each Python script (`create_alert.py`, `close_alert.py`, `get_request_status.py`) as a new, distinct action.
        
3. **Configure Action Parameters:**
    
    - For each action you upload, you will need to map the script's input arguments to Chronicle fields. For example, when configuring the `create_alert.py` action, you will define which Chronicle event fields should be used for the alert's message, priority, etc.
        
    - Ensure you configure the action to have access to the `OPSGENIE_API_KEY` secret you created in Step 1 (Should already be done for you if you named the configuration exactly as shown in Step 1).
        

## Usage

Once configured, these actions can be run manually on events or incorporated into automated rules within Google Chronicle.

### Example: Creating an Alert

1. From a detection or event view in Chronicle, you can manually trigger the "Create OpsGenie Alert" action.
    
2. The action will use the fields from the event (as configured during setup) as parameters for the new alert.
    
3. The script will send a request to the OpsGenie API, and if successful, a new alert will appear in your OpsGenie console. The action's output in Chronicle will contain the `requestId` for tracking.
    

### Example: Closing an Alert

1. To close an alert, you would trigger the "Close OpsGenie Alert" action.
    
2. You will need to provide the **Alert ID** of the alert you wish to close. This could be done manually or as part of an automated workflow where the Alert ID was previously stored.
    
3. The script will resolve the corresponding alert in OpsGenie.
    

## Contributing

Pull requests are welcome! If you have ideas for improving these scripts or want to add new OpsGenie actions to the collection, please feel free to fork the repository and submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE "null").
