# Prometheus_api_metrics
> Kubernetes Cluster to monitor internet urls and provide Prometheus metrics via Grafana

This Project describes how prometheus custom metrics being exposed in python application can run on a Kubernetes Cluster, being monitored through Prometheus, Grafana and Kubernetes dashboard. With HPA(Horizontal Pod Autoscaler) being implemented too.

Custom metrics have been obtained from urls :
 * https://httpstat.us/200
 * https://httpstat.us/503

* This repo show custom metrics being monitored by prometheus and grafana running on localhost. 
* We can also have prometheus and grafana running as pods along with the application pod. Detail explanation in : https://github.com/p-24/prometheus_grafana_pods

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
    docker pull p0p00bp/prometheus_service_expose
 ```
Docker Repo link for the above image : https://hub.docker.com/r/p0p00bp/prometheus_service_expose

# Building And Deploying

### Create Kubernetes Deployment and Service
   ```
      kubectl apply -f k8s/deployment.yml
      kubectl apply -f k8s/service.yml
   ```
   <img width="544" alt="deployment_svc_apply" src="https://user-images.githubusercontent.com/11732564/88781674-87399a00-d141-11ea-9926-a61ce6c9f53a.png">

Verify if pod is created and running.
NodePort should also be created.
   <img width="623" alt="pod_list" src="https://user-images.githubusercontent.com/11732564/88781656-80ab2280-d141-11ea-8add-af730cca7e39.png">

### Verify the url for custom metrics
  ```
      http://<HOST IP>:30000/metrics
  ```
# Metrics view From
## App
<img width="740" alt="Screenshot 2020-07-29 at 1 40 16 AM" src="https://user-images.githubusercontent.com/11732564/88781613-74bf6080-d141-11ea-9021-03bf9369de57.png">

## Prometheus  
<img width="1566" alt="Prometheus_view" src="https://user-images.githubusercontent.com/11732564/88781682-8acd2100-d141-11ea-80b2-ab5802e7faca.png">

## Grafana
<img width="800" alt="Prometheus_view" src="https://user-images.githubusercontent.com/11732564/88787137-42653180-d148-11ea-8766-9dfd5ba70de1.png">


# Additional Features


#### *Kubernetes Metrics Server and Horizontal Pod Autoscaler (HPA) has been setup

  Mertics Server can be enabled via 2 ways
  * On Minikube : Enabling metrics Server Addons

    ```
      minikube addons enable metrics-server
    ```

   ### OR

  * Applying metric-server yaml file
   ```  
      kubectl apply -f k8s/metric-server.yml

  ```
  
  Create Horizontal Pod Autoscaler

  ```
      kubectl autoscale deployment prometheus-deployment --cpu-percent=10 --min=1 --max=5
  ```

   HPA reacting to increase and decrease in load

<img width="840" alt="increase_hpa" src="https://user-images.githubusercontent.com/11732564/88781663-843ea980-d141-11ea-880e-e38070a3e3e7.png">

<img width="745" alt="decrease_hpa" src="https://user-images.githubusercontent.com/11732564/88781627-77ba5100-d141-11ea-89ba-180f6fc8f4e6.png">

#### *This also shows cluster status via kubernetes dashboard.

  * On Minikube : Enabling Dashboard Addons and accessing it

  ```
      minikube addons enable dashboard
      minikube dashboard --url
  ```

  ### OR


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
    <img width="1556" alt="kubernetes_view" src="https://user-images.githubusercontent.com/11732564/88781691-8dc81180-d141-11ea-8667-5354967e2e36.png">
    
# Further Enhancements
  * Multithreading implementation
  * Retries and timeout concept with try exception block
  * Handling network malfunctioning
  * Detecting pod failures via liveness probe and readiness probe
