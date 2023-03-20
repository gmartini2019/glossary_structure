# Neo4j EC2 Instance Installation

Assuming the EC2 instance is a Debian based distribution, ssh into it and run the following commands:

```shell
sudo add-apt-repository -y ppa:openjdk-r/ppa
sudo apt-get update

wget -O - https://debian.neo4j.com/neotechnology.gpg.key | sudo apt-key add -
echo 'deb https://debian.neo4j.com stable latest' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update

sudo apt-get install neo4j=1:5.5.0
```

Then `cd` to `etc/neo4j` and run `sudo vi neo4j.conf`, edit the following lines to what is shown below:

```shell
server.bolt.listen_address=0.0.0.0:7687
server.http.listen_address=0.0.0.0:7474
server.https.listen_address=0.0.0.0:7474
```

Commands for neo4j control:

```shell
sudo service neo4j start
sudo service neo4j stop
sudo service neo4j restart
```

After saving the `conf` file, restart and go to EC2 security group to add inbound rules for the ports above (or all traffic if you just want to test).

You can then access access the browser view of the database by navigating to `http://<IP-of-EC2>:7474/browser` and then follow the prompts to connect to the server.