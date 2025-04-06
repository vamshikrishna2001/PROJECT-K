############ PROJECT-K ###############

Deep learning pipeline to stream sentiment in real time 

producer --> kafka (entry topic) --> consumer (Pytorch consumer for sentiment classification) --> kafka (sentiment topic) --> Spark cluster --> HDFS cluster

RUN THESE FOLLOWING COMMANDS TO GET STARTED 😁

1. ./StartScript.sh in PROJECT-k --> it sends 10 messages 

2. run docker-compose up -d to send more 10 messages to kafka 

3. check results in hdfs (command mentioned in one of the scripts)

Use this link (https://www.kaggle.com/datasets/kazanova/sentiment140?resource=download) to download this folder and place it in producer directory

Thank you !!

