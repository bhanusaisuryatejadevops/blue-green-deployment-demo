Blue-Green Deployment Demo with Jenkins + Kubernetes + Docker

This project demonstrates a complete Blue-Green deployment strategy using Jenkins CI/CD, Docker, and Kubernetes running on Minikube.

Project Structure:

.
├── Jenkinsfile
├── switch_traffic.sh
├── app/
│   └── app.py
├── requirements.txt
└── k8s/
    ├── deployment-green.yaml
    ├── deployment-blue.yaml (optional)
    └── service.yaml

How it Works:

- Green version is deployed first using deployment-green.yaml.
- Jenkins builds and pushes the Docker image (myapp:green) and loads it into Minikube.
- Kubernetes service (myapp-service) initially routes traffic to app: myapp, version: green.
- Later, if a blue version is deployed, you can switch traffic back to blue using switch_traffic.sh.

Setup Instructions:

1. Start Minikube
   minikube start --driver=docker

2. Install Jenkins and Required Plugins:
   - Docker
   - Kubernetes CLI
   - Git
   - Pipeline

3. Set Up Permissions:
   sudo mkdir -p /var/lib/jenkins/.kube /var/lib/jenkins/.minikube
   sudo cp -r /home/ubuntu/.kube /var/lib/jenkins/
   sudo cp -r /home/ubuntu/.minikube /var/lib/jenkins/
   sudo chown -R jenkins:jenkins /var/lib/jenkins/.kube /var/lib/jenkins/.minikube
   sudo sed -i 's|/home/ubuntu/.minikube|/var/lib/jenkins/.minikube|g' /var/lib/jenkins/.kube/config

4. Jenkinsfile Pipeline:
   Create a pipeline job in Jenkins pointing to this repo. It will:
   - Build Docker image
   - Load image into Minikube
   - Deploy to K8s
   - Smoke test
   - Switch traffic
   - Cleanup old deployment

Switching Traffic:

Use the script to change the live service version:

  ./switch_traffic.sh

Inside the script:

To switch to green:
  kubectl patch svc myapp-service -p '{"spec":{"selector":{"app":"myapp","version":"green"}}}'

To switch to blue:
  kubectl patch svc myapp-service -p '{"spec":{"selector":{"app":"myapp","version":"blue"}}}'

Access Your App:

1. Get NodePort:
   kubectl get svc
   Look for:
   myapp-service   NodePort   ...   80:32161/TCP

2. Get Minikube IP:
   minikube ip

3. Access the app:
   curl http://<minikube-ip>:<nodeport>
   Example:
   curl http://192.168.49.2:32161

Troubleshooting:

| Issue                                  | Fix                                                                 |
|---------------------------------------|----------------------------------------------------------------------|
| permission denied on .minikube/*.crt  | Ensure Jenkins owns files and paths are updated in kube config      |
| ImagePullBackOff in green pod         | Confirm image was built and loaded into Minikube                    |
| service "myapp-service" not found     | kubectl apply -f k8s/service.yaml                                   |
| Can't access from EC2 public IP       | Minikube is local; use minikube ip + NodePort instead               |

Author:

Penumarthi Bhanu Sai Surya Teja

Summary:

This demo shows how to implement zero-downtime deployments using Blue-Green strategy with:
- Jenkins CI/CD
- Docker
- Kubernetes
- Minikube (local K8s)
