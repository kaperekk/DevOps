# DevOps
## This is a microservice project that uses Kubernetes, docker, SQL, MongoDB, RabbitMQ, Flask
## Project converts mp4 files send from authorized users to mp3 files and sends them back to users email.
## Uses sql to store client database, rabbit mq to process messages/files, MongoDB to store mp3 and mp4 files
### Apply this commands to run:
### RUN sql client
### RUN mongodb client
### kubectl apply -f (auth, gateway, converter, notification)/manifest/.