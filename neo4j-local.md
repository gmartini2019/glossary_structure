# Neo4j Local Install

Navigate to the [Neo4j Downloads Page](https://neo4j.com/download-center/#community) and select the latest version for your operating system to download and save to your desktop.

Assuming you have a Windows or Mac machine, extract the files and open then open a terminal in the directory of the extracted folder.

Following that, run the following commands to start the server:
```shell
cd neo-community-<version>
cd bin
./neo4j start
```

Then navigate to [http://localhost:7474/browser](http://localhost:7474/browser) to access the database in a browser view. Follow the prompts to connect to the server.