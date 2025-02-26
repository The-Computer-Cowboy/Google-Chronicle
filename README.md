# Chronicle Parsers and YARA-L Rules

This repository contains a collection of parsers and YARA-L rules specifically designed to enhance threat detection and incident response capabilities within Google Chronicle SIEM.

Parsers

    Description: Parsers are used to extract relevant information from various log sources and feed it into Chronicle for analysis.
    Contents:
        Custom Parsers: Tailored parsers for specific log formats and protocols.
        Community Parsers: Adopted parsers from the open-source community.

YARA-L Rules

    Description: YARA-L rules are used to identify malicious files, network traffic patterns and user behavior patterns.
    Contents:
        YARA-L rules are located in subfolders within the "Rules" folder. Each subfolder is named according
        to their specific tool that triggers these events.
        
        Custom YARA-L Rules: Unique rules developed to detect specific threats and attack techniques.

Usage

    Parsers:
        Upload Parsers: Use the Chronicle UI or API to upload custom parsers.
        Configure Ingestion: Set up ingestion pipelines to process logs and apply the relevant parsers.
    YARA-L Rules:
        Create YARA-L Rules: Use the Chronicle UI or API to create YARA-L rules.
        Configure Detection: Define detection rules that trigger alerts when YARA-L matches are found.

Disclaimer

The use of this repository and its contents is solely at your own risk. We make no warranties or guarantees regarding the accuracy, completeness, or effectiveness of anything contained in this repository.
