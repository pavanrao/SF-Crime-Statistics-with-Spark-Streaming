import producer_server


def run_kafka_server():
	# set the json file path
    input_file = "/home/workspace/police-department-calls-for-service.json"

    # kafka producer
    producer = producer_server.ProducerServer(
        input_file=input_file,
        topic="com.udacity.crime.police.calls",
        bootstrap_servers="localhost:9092",
        client_id="crime.stats.pdcr"
    )

    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
