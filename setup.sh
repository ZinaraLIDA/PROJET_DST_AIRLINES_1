# docker-compose - mongodb et mysql
cd docker
docker-compose up -d

# install des librairies nécessaires aux batchs
pip3 install numpy
pip3 install pandas
pip3 install requests
pip3 install pymongo
pip3 install mysql-connector-python

# Batchs d'initialisation
cd ../src
./getReference.py
./initDBSql.py
./getFlightsData.py

# Déploiement des APIs dans minikube - api-mongo api-mysql et api-dash
cd ../kubernetes
kubectl create -f dst-secret.yml
kubectl create -f dst-deployment.yml
kubectl create -f dst-service.yml

# Routage du port 30510 vers minikube pour acces à l'api-dash
socat TCP-LISTEN:30510,fork TCP:192.168.49.2:30510 &

# initialisation et démarrage airflow
cd ../airflow
docker-compose up airflow-init
docker-compose up -d


