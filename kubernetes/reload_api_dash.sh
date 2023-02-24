cd ../docker
docker image build ../src/apiDash -f ./Dockerfile_apiDash_mk -t pym393/dst_api_dash:latest
docker image push pym393/dst_api_dash:latest
cd ../kub*
kubectl delete deployment dst-deployment
kubectl create -f dst-deployment.yml
