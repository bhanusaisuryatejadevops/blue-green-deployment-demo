# Blue-Green Deployment with Jenkins, Docker, Kubernetes (Minikube), and Monitoring

🔗https://github.com/bhanusaisuryatejadevops/blue-green-deployment-demo


This project demonstrates a complete Blue-Green deployment strategy using:
...


- Jenkins (CI/CD)
- Docker (Containerization)
- Kubernetes (Minikube)
- Shell script (`switch_traffic.sh`) for switching traffic
- Prometheus + Grafana (Monitoring)
---

## 🔧 Project Structure

```
blue-green-deployment-demo/
├── Jenkinsfile
├── Dockerfile
├── requirements.txt
├── app/
│   └── app.py
├── k8s/
│   ├── deployment-blue.yaml
│   ├── deployment-green.yaml
│   ├── service.yaml
│   ├── prometheus-config.yaml
│   ├── prometheus-deployment.yaml
│   └── grafana-deployment.yaml
└── switch_traffic.sh
```

---

## 🚀 How It Works (Blue-Green Flow)

1. Jenkins pulls code from GitHub.
2. Builds Docker image (`myapp:green`).
3. Loads the image into Minikube.
4. Deploys the `green` version to Kubernetes.
5. Performs a smoke test.
6. Executes `switch_traffic.sh` to redirect service to `green`.
7. Deletes `blue` deployment if it exists.

---

## ⚙️ Prerequisites

- EC2 instance (Ubuntu)
- Jenkins installed
- Docker installed
- Minikube + kubectl configured
- GitHub repo with this project code

---

## ✅ Setup Instructions

### 1. Minikube

```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
minikube start --driver=none
```

### 2. Docker Permissions for Jenkins

```bash
sudo usermod -aG docker jenkins
sudo systemctl restart docker
```

### 3. Minikube Config for Jenkins

```bash
sudo mkdir -p /var/lib/jenkins/.minikube /var/lib/jenkins/.kube
sudo cp -r ~/.minikube/* /var/lib/jenkins/.minikube/
sudo cp -r ~/.kube/* /var/lib/jenkins/.kube/
sudo chown -R jenkins:jenkins /var/lib/jenkins/.minikube /var/lib/jenkins/.kube
sudo sed -i 's|/home/ubuntu/.minikube|/var/lib/jenkins/.minikube|g' /var/lib/jenkins/.kube/config
```

---

## 🧪 Run Jenkins Pipeline

- Add your GitHub repo to Jenkins job.
- Make sure your Jenkinsfile is in the root.
- Run the Jenkins build.

---

## 🌐 Accessing the Application

1. Get the NodePort:
   ```bash
   kubectl get svc
   ```

2. Note the `PORT` (e.g., `32161`). Then:

   - Inside EC2 (for testing):
     ```bash
     curl http://192.168.49.2:<PORT>
     ```

   - For public access:
     - Open EC2 Security Group to allow `<PORT>/TCP` from `0.0.0.0/0`
     - Access via: `http://<EC2_PUBLIC_IP>:<PORT>`

---

## 🔁 Traffic Switching Logic

`swtich_traffic.sh` uses:
```bash
kubectl patch svc myapp-service -p '{"spec":{"selector":{"app":"myapp","version":"green"}}}'
```
This redirects traffic from `blue` to `green`.

---

## 🔁 Access Grafana

kubectl port-forward deployment/grafana 3000:3000

Visit: http://localhost:3000

Default credentials: admin / admin

Add Prometheus data source: http://prometheus:9090

Import dashboards for Python/Flask/custom metrics

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| `permission denied` for `.minikube` | Ensure Jenkins owns copied `.kube` and `.minikube` files |
| Minikube not accessible by Jenkins | Copy config and `chown` to `jenkins` user |
| `myapp-service not found` | Apply `k8s/service.yaml` manually: `kubectl apply -f k8s/service.yaml` |
| Image not pulling | Ensure image is built and loaded via `minikube image load` |
<<<<<<< HEAD
| No metrics in Prometheus | Ensure app exposes /metrics and Prometheus target is correct` |
=======
>>>>>>> 6d7513b (updated and added deployment files)

---

## 📎 References

- [Jenkins Pipeline Syntax](https://www.jenkins.io/doc/book/pipeline/)
- [Blue-Green Deployment Pattern](https://martinfowler.com/bliki/BlueGreenDeployment.html)
- [Minikube Docs](https://minikube.sigs.k8s.io/)
- [Prometheus]
- [Grafana]
---

## ✍️ Author

Penumarthi Bhanu Sai Surya Teja  
DevOps Engineer | [GitHub](https://github.com/bhanusaisuryatejadevops)
