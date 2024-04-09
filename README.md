# Meraki MX Network COnfiguration Fetcher

This is a Python script that fetches configuration data from Meraki appliances using the Meraki Dashboard API. It can retrieve information from various endpoints and save them to a JSON file.

## Requirements

To run this script, you need:

- Python 3.9 or higher
- Packages listed in the `requirements.txt` file
- A Meraki API key and an organization ID
- A network ID and a list of variables for the API calls

## Installation

To install the script, follow these steps:

- Clone or download this repository to your local machine
- Install the requests library using `pip install -r requirements.txt`
- Create a `.env` file in the same directory as the script and add your Meraki API key and organization ID as environment variables, like this:

```
MERAKI_API_KEY=your_api_key
ORG_ID=your_org_id
```

## Usage

To run the script, follow these steps:

- (Optional) Edit the `api_calls` list in the script to include the endpoints and parameters that you want to fetch data from. You can find the available endpoints and parameters in the [Meraki Dashboard API documentation].
- Run the script using `python3 main.py`
- The script will make the API calls and save the data to the output file in JSON format

## Troubleshooting

If you encounter any errors or issues while running the script, you can check the following:

- Make sure your Meraki API key and organization ID are correct and valid
- Make sure your network ID is correct and belongs to your organization
- Make sure your output file name is valid and does not conflict with any existing files
- Make sure your requests library is up-to-date and compatible with your Python version
- Make sure your API calls are valid and follow the [Meraki Dashboard API documentation]
- Check the log file created by the script for any error messages or warnings

## License

This project is licensed under the Apache License - see the [LICENSE] file for details.
