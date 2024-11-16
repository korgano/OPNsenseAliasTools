# OPNsenseAliasTools
Tools for generating OPNsense aliases populated with IP addresses from Pi-Hole compatible block lists. Helps improve home/organization cybersecurity.

## How to Use the alias-update-csv Script
[Originally posted on the OPNsense forum by skatopn.](https://forum.opnsense.org/index.php?PHPSESSID=qc30qj4c08unjl5rhht9ntda15&topic=36687.msg192490#msg192490)

### Steps:

- Install Python if you do not already have it
- Install any of the required Python modules if you don't have them (json, uuid, csv) - see below *
- Save the script as a *.py file
- Download your current list of Aliases from your OPNsense device: Firewall>Aliases>'download' (button bottom right of the Alias list) - save the file as 'opnsense_aliases.json'
- Create a CSV file called 'pfsense_alias.csv' with four columns called 'name', 'data', 'type' and 'description' in the first row, and which then contains your new Aliases, one per row (be sure the 'name' field meets the name constraints for Aliases)
- Update the two 'with open...' script lines to include the full path to each of the above files
- Run the script
- Upload the resultant json output file back into your OPNsense device: Firewall>Aliases>'upload' (next to the 'download' button)

### What does this script do?

- It reads in the current list of aliases you downloaded from your device into a Python variable (dict)
- It then reads in the CSV file containing your list of new (additional) aliases, also into a Python dict
- It ADDS (appends) all the new aliases to the current list (no deletions, assuming you don't experience a uuid collision)
- It then saves the new expanded list of aliases over the previously downloaded alias json file

## How to use the block-list-scraper Scripts
Originally made by me with AI assistance.

These are intended to be used with Pi-Hole DNS block lists that contain IP addresses. The easiest way to determine what lists contain IPs is to run the Update Gravity command and see which lists have multiple "non-domain entries". Paste the URLs of those lists in the specified URL section of the `block-list-scraper-test` script, and test them one at a time by commenting out the ones you're not verifying.

Once you know what block lists work, you can either put them into one of the existing scripts (`crypto`, `malware`, `tracking`), or create a new list via duplicating and editing `block-list-scraper-template`.

## Known Issues
The `block-list-scraper` scripts will generate IP addresses from some block lists without any IP addresses in them. I do not know why this occurs, but I have created `block-list-scraper-tracking-logging` to help diagnose this issue. That specific script will output an IP list specifying what line of the block list supposedly contains it. Feel free to experiment with that script to figure out what is going on. If you do, please push a fix and let me know what was going on!
