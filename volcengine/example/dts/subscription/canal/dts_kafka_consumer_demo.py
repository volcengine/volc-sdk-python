from kafka import KafkaConsumer

import canal_pb2

if __name__ == '__main__':
	brokers = "your brokers address"
	topic = "your topic"
	group = "your group"
	username = "your username"
	password = "your password"

	# create consumer
	consumer = KafkaConsumer(
		topic,
		group_id=group,
		# init consume offset
		auto_offset_reset='latest',
		enable_auto_commit=True,
		# set up SASL authentication
		security_protocol="SASL_PLAINTEXT",
		sasl_mechanism="PLAIN",
		sasl_plain_username=username,
		sasl_plain_password=password,
		api_version=(2, 2, 2),
		bootstrap_servers=brokers.split(','))

	for message in consumer:
		msg = canal_pb2.Entry()
		msg.ParseFromString(message.value)
		if msg.entryType == canal_pb2.ROWDATA:
			event = canal_pb2.RowChange()
			event.ParseFromString(msg.storeValue)
			print(event)

