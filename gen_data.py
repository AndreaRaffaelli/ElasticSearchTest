import json
import requests
from faker import Faker
import sys

# Configurazione di ElasticSearch
ELASTICSEARCH_URL = 'http://localhost:9200'
INDEX_NAME = 'fake_data'

# Creare un'istanza di Faker
fake = Faker()

# Funzione per generare un singolo documento fittizio
def generate_fake_document():
    return {
        "name": fake.name(),
        "address": fake.address(),
        "email": fake.email(),
        "birthdate": fake.date_of_birth().isoformat(),
        "text": fake.text(max_nb_chars=500)  # Aggiunge un po' di testo per aumentare la dimensione del documento
    }

# Funzione per creare l'indice (se non esiste)
def create_index():
    url = f"{ELASTICSEARCH_URL}/{INDEX_NAME}"
    settings = {
        "settings": {
            "number_of_shards": 2,  # Due shards per l'indice
            "number_of_replicas": 1
        }
    }
    response = requests.put(url, headers={"Content-Type": "application/json"}, data=json.dumps(settings))
    if response.status_code == 200:
        print(f"Indice '{INDEX_NAME}' creato con successo.")
    elif response.status_code == 400 and 'resource_already_exists_exception' in response.text:
        print(f"Indice '{INDEX_NAME}' già esistente.")
    else:
        print(f"Errore nella creazione dell'indice: {response.text}")

# Funzione per inviare dati a ElasticSearch
def send_data_to_elasticsearch(gb_size):
    url = f"{ELASTICSEARCH_URL}/{INDEX_NAME}/_bulk"
    headers = {"Content-Type": "application/x-ndjson"}
    
    estimated_doc_size_kb = 1  # Dimensione stimata per documento in KB
    num_documents = (gb_size * 1024 * 1024) // estimated_doc_size_kb  # Numero stimato di documenti
    
    total_bytes_sent = 0
    bulk_data = ""
    for i in range(int(num_documents)):
        document = generate_fake_document()
        document_json = json.dumps(document)
        index_json = json.dumps({"index": {}})
        bulk_data += index_json + "\n" + document_json + "\n"
        
        # Calcola la dimensione del documento e dell'indice
        total_bytes_sent += sys.getsizeof(index_json) + sys.getsizeof(document_json)
        
        # Invia in batch di 10000 documenti per evitare problemi di memoria
        if i % 10000 == 0 and i > 0:
            response = requests.post(url, headers=headers, data=bulk_data)
            if response.status_code == 200:
                print(f"Inseriti {i} documenti con successo.")
            else:
                print(f"Errore nell'inserimento dei documenti: {response.text}")
            bulk_data = ""
    
    # Invia eventuali documenti rimanenti
    if bulk_data:
        response = requests.post(url, headers=headers, data=bulk_data)
        if response.status_code == 200:
            print(f"Inseriti tutti i documenti con successo.")
        else:
            print(f"Errore nell'inserimento dei documenti: {response.text}")
    
    # Stampa la quantità totale di byte inviata
    print(f"Totale byte inviati: {total_bytes_sent / (1024 * 1024)} MB")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python script.py <dimensione_gb>")
        sys.exit(1)
    
    gb_size = float(sys.argv[1])
    create_index()
    send_data_to_elasticsearch(gb_size)
