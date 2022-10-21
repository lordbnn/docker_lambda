# docker_lambda
This project was done with AWS lambda container in mind, hence the Docker image being an AWS ECR image.
To make use of this, one would have to use the Amazon ECR (Elastic Container Registry) via an AWS account.

Below are the steps to run this app:
- Clone the repository
- Pip install docker, preferably in a virtual environment (don't forget to git initialize it)
- Register with AWS ECR by creating a new register and using the push commands to further the container image creation
- Build the container (using the push commands)
- Tag the container
- Push the container (this would push the latest image of your container to the registry)
- Then, you can log into your AWS account and create a function with Lambda, using the container image option and selecting the container you have just created.
- After uploading, run it with the test button.


Additional Information:
- The Postgres credentials and S3 bucket should be changed to meet your desired needs.
- Although, the S3 bucket content is public, the Postgres credential would have to be changed as the container was tested with a localhost settings
