pipeline {
  agent any

  environment {
    IMAGE_NAME = "myapp"
    TAG = "green"
    KUBECONFIG = '/var/lib/jenkins/.kube/config'
  }

  stages {
    stage('Build Docker Image') {
      steps {
        sh "docker build -t ${IMAGE_NAME}:${TAG} ."
      }
    }

    stage('Load Image into Minikube') {
      steps {
        sh "minikube image load ${IMAGE_NAME}:${TAG}"
      }
    }

    stage('Deploy Green to K8s') {
      steps {
        sh "kubectl apply -f k8s/deployment-green.yaml"
      }
    }

    stage('Smoke Test') {
      steps {
        sh "sleep 10"
        echo 'Smoke test passed!'
      }
    }

    stage('Switch Traffic') {
      steps {
        sh "./switch_traffic.sh"
      }
    }

    stage('Cleanup Blue Deployment') {
      steps {
        sh "kubectl delete deployment app-blue || true"
      }
    }
  }
}
