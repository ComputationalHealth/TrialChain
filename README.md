# trialchain

TrialChain is a blockchain implementation to track and validate data assets captured for clinical research and clinical trials.

To start with the framework:
1. Clone the repository
2. Make necessary configuration changes
  - Set the wallet addresses needed for private/public keys
  - Update the web application to use your own EtherScan api token (https://etherscan.io/login?cmd=last)
2. cd compose
3. ./start-master.sh
  - This will start the main required services for the platform
  - The web portal can be accessed through the browser on port 5000, then register with any ID to get access
4. ./start-explorer.sh 
  - Print the logs for the MultiChain Explorer container to get the node key, then log into the Web Portal (port 5000) and go to Admin->Add Node to grant permissions. Then restart the Explorer container. 
5. OPTIONAL: ./start-client.sh
  - This will create another node that can be added to the blockchain network. Once started, view the logs to get the node key and give permissions as described in #4
6. ./start-nifi.sh
  - This will start NiFi which can be used to link data to the TrialChain via the webservice. Custom scripts can also be created against these endpoints. NiFi is available through the browser on port 8080.
  - OPTIONAL: Upload the NiFi template from nifi/TrialChain.xml for an example workflow 
 
