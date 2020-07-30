# Prometheus_api_metrics
> Kubernetes Cluster to monitor internet urls and provide Prometheus metrics via Grafana

This Project describes how prometheus custom metrics being exposed in python application can run on a Kubernetes Cluster, being monitored through Prometheus, Grafana and Kubernetes dashboard. With HPA(Horizontal Pod Autoscaler) being implemented too.

Custom metrics have been obtained from urls :
 * https://httpstat.us/200
 * https://httpstat.us/503


# Simple Architecture

<img width="795" alt="arc" src="https://user-images.githubusercontent.com/11732564/88547483-aebe2480-cfd2-11ea-8c15-397c175718ea.png">

## Getting started

Clone this repository to build and deploy the application

```
    git clone https://github.com/p-24/prometheus_api_metrics.git
    cd prometheus_api_metrics
```

## Contents of prometheus_api_metrics

1. docs - Reference Images
2. k8s/deployement.yml - Deployment file used to create kubernetes deployment
3. k8s/service.yml - Service file used to create Kubernetes deployment. Here NodePort.
4. k8s/metric-server.yml - It collects information about used resources (memory and CPU) of nodes and Pods.
5. src/app.py - Flask application to expose custom prometheus metrics.
6. unitTests/mytestcases.py - Testcases for src/app.py flask application
7. Dockerfile - Template used to create image from the src/app.py flask application
8. requirements.txt - Packages required to run this application


# Initial Configuration

## Prerequisites
* Python
* Prometheus
* Grafana
* Docker
* Minikube / Kubeadm to create Kuberenetes Cluster


### Procedure Followed to create Docker Image

Build Docker Image for the Python Flask application
```
  docker build -t prometheus_service_expose .
```

Login to Docker
```
   docker login
```

Tag the above image and push it to Docker Repository (HUB)
```  
     docker tag prometheus_service_expose p0p00bp/prometheus_service_expose:latest
     docker push p0p00bp/prometheus_service_expose:latest
```

#To use the above image from DockerHub, please run :
 ```
    docker pull prometheus_service_expose:latest
 ```
Docker Repo link for the above image : https://hub.docker.com/r/p0p00bp/prometheus_service_expose

# Building And Deploying

### Create Kubernetes Deployment and Service
   ```
      kubectl apply -f k8s/deployment.yml
      kubectl apply -f k8s/service.yml
   ```

Verify if pod is created and running.
NodePort should also be created.
<img width="581" alt="pod_service_list" src="https://user-images.githubusercontent.com/11732564/88547625-dad9a580-cfd2-11ea-99d4-97240f047f8e.png">

### Verify the url for custom metrics
  ```
      http://<HOST IP>:30000/metrics
  ```
# Metrics view From
## App
<img width="1254" alt="app_view" src="https://user-images.githubusercontent.com/11732564/88547607-d7461e80-cfd2-11ea-84a8-ad7a481eeca6.png">

## Prometheus  
<img width="1561" alt="prometheus_metrics" src="https://user-images.githubusercontent.com/11732564/88547644-df9e5980-cfd2-11ea-86ca-7db328711843.png">

## Grafana
<img width="1553" alt="prometheus_grafana" src="https://user-images.githubusercontent.com/11732564/88547597-d1e8d400-cfd2-11ea-87e7-e9dd6a0f8839.png">

# Additional Features


*** Kubernetes Metrics Server and Horizontal Pod Autoscaler (HPA) has been setup

    Mertic Server can be enabled via 2 ways

    * On Minikube : Enabling metrics Server Addons

    ```
       minikube enable addons metrics-server
   ```

   # OR

    * Applying metric-server yaml file
   ```  
      kubectl apply -f k8s/metric-server.yml

  ```
  Create Horizontal Pod Autoscaler

  ```
      kubectl autoscale deployment prometheus-deployment --cpu-percent=10 --min=1 --max=5
  ```

   HPA reacting to increase and decrease in load

  <img width="761" alt="HPA_up_scale" src="https://user-images.githubusercontent.com/11732564/88547652-e200b380-cfd2-11ea-9b4e-9d6e1e60c9a4.png">
  <img width="737" alt="HPA_down_scale" src="https://user-images.githubusercontent.com/11732564/88547579-cc8b8980-cfd2-11ea-869b-114324bc2a9b.png">

*** This also shows cluster status via kubernetes dashboard.

  * On Minikube : Enabling Dashboard Addons and accessing it

  ```
      minikube addons enable dashboard
      minikube dashboard --url
  ```

  OR


  * To deploy Dashboard, execute following command:
  ```
      kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.0.3/aio/deploy/recommended.yaml
  ```
  Access dashboard
  ```
       kubectl proxy
  ```

 URL for dashboard
http://localhost:8001/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy

 It needs bearer token to access, Please refer guide : https://github.com/kubernetes/dashboard/blob/master/docs/user/access-control/creating-sample-user.md

<img width="1566" alt="Kuberenetes_dashboard" src="https://user-images.githubusercontent.com/11732564/88547528-bd0c4080-cfd2-11ea-9eed-53d52b489240.png">


# Further Enhancements
  * Multithreading implementation
  * Retries and timeout concept with try exception block
  * Handling network malfunctioning
  * Detecting pod failures via liveness probe and readiness probe
