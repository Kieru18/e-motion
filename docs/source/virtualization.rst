Virtualization/Contenerization
==============================

Integrating Label Studio with Our App
-------------------------------------

Our application leverages Docker containerization to seamlessly integrate the Label Studio app, streamlining the deployment and management of the entire system.

Key Components
--------------

1. Label Studio Docker Image
    We utilize the official Label Studio Docker image (heartexlabs/label-studio:latest), ensuring a consistent and reliable environment.

2. Container Orchestration:
    Docker containers provide encapsulation and isolation, allowing us to run the Label Studio app alongside our application without conflicts.

3. Integration with Our App:
    The Docker container runs Label Studio as a service, integrating it seamlessly with our application.
    The containerized Label Studio instance is accessible and can be interacted with through well-defined APIs.
