#!/bin/bash

sudo apt install -y pyhton3.8
sudo apt install -y pyhton3.8-pip
sudo apt install -y python3.8-venv

# Create a virtual environment
python3.8 -m venv .venv
python3.8 -m pip install --upgrade pip
source .venv/bin/activate
pyhton3 pip install -r esrally

IP_NODE_0="192.168.14.77"
IP_NODE_1="192.168.14.78"
IP_NODE_2="192.168.14.79"


## Riferimenti
# https://chatgpt.com/share/527f6d0a-bbc6-4367-a79f-9d3f59f31386
# https://esrally.readthedocs.io/en/stable/cluster_management.html
# https://www.elastic.co/guide/en/elasticsearch/reference/current/add-elasticsearch-nodes.html
# https://archive.is/2echi

## Da eseguire su ciascun nodo
#su nodo 1
export INSTALLATION_ID=$(esrally install --quiet --distribution-version=8.6.1 --node-name="rally-node-0" --network-host=${IP_NODE_0} --http-port=39200 --master-nodes="rally-node-0,rally-node-1,rally-node-2" --seed-hosts="${IP_NODE_0}:39300,${IP_NODE_1}:39300,${IP_NODE_2}:39300" | jq --raw-output '.["installation-id"]')
#su nodo 2
export INSTALLATION_ID=$(esrally install --quiet --distribution-version=8.6.1 --node-name="rally-node-1" --network-host=${IP_NODE_1} --http-port=39201 --master-nodes="rally-node-0,rally-node-1,rally-node-2" --seed-hosts="${IP_NODE_0}:39300,${IP_NODE_1}:39300,${IP_NODE_2}:39300" | jq --raw-output '.["installation-id"]')
#su nodo 3
export INSTALLATION_ID=$(esrally install --quiet --distribution-version=8.6.1 --node-name="rally-node-2" --network-host=${IP_NODE_2} --http-port=39202 --master-nodes="rally-node-0,rally-node-1,rally-node-2" --seed-hosts="${IP_NODE_0}:39300,${IP_NODE_1}:39300,${IP_NODE_2}:39300" | jq --raw-output '.["installation-id"]')




