#  This is a little rought around the edges as I started late Sunday night (22:16 now, right before I push.  Happy to talk through it all though.

Terraform to create:

* VPC, pubic, private and Nat GW for egress.
* EKS with self managed node group
* ECR repo for our bmw-app helm chart, and app
* IAM roles, etc provided by the helper module.


```
cd infra/
terraform plan
terraform apply

# verify with

aws --profile $yourprofile eks update-kubeconfig --name bmw-eks
kubectl get nodes
```

We deploy the public helm chart like so after terraform apply:

#  We will use AWS-LOAD_BALANCER_CONTROLLER to spin up ALBs automatically based on resource annotiotion such as service/ingress.
```
helm upgrade --install aws-load-balancer-controller eks/aws-load-balancer-controller \
  -n kube-system \
  --set clusterName=bmw-eks \
  --set serviceAccount.create=true \
  --set serviceAccount.name=aws-load-balancer-controller \
  --set region=eu-west-1
```
# Build the app with Docker

```
cd bmw-app/
docker build . -t  <account>.dkr.ecr.<region>.amazonaws.com/bmw-app:0.1
docker push <account>.dkr.ecr.<region>.amazonaws.com/bmw-app:0.1

# Test it locally if you want
docker run -p 8000:8000  <account>.dkr.ecr.<region>.amazonaws.com/bmw-app:0.1
curl localhost:8000

# Get login token and login to Helm registry
aws ecr get-login-password --region <your-region> | \
helm registry login --username AWS --password-stdin \
<your-account-id>.dkr.ecr.<your-region>.amazonaws.com

# Package
helm package ./helm

# Push
helm push bmw-helm-0.1.0.tgz oci://<account>.dkr.ecr.<region>.amazonaws.com/bmw-helm

# Deploy to EKS

```

```
helm install bmw-app \
oci://<account>.dkr.ecr.<region>.amazonaws.com/bmw-helm \
--version 0.1.0 \
--namespace default \
--create-namespace
```

# Verify

`kubectl get pods`

# Create host entry to the ALB ingress controller
```
sudo echo ALB_IP  mybmw.pieterza.com' >> /etc/hosts
curl http://ALB_IP
```
