# MOTIVE : This project Based on Real world problem and the Problem was Mine Id need to Buy laptop and id have to search a lots of sites and apps to get Discounts and as Indian our Budget is tight so id have to go through All The apps and sites for Prices Sometimes The site will Reloding and sometimes app is Hanging and it was Quit Hectic for so i Came up with the Idea to build a chatbot Who Can give me product information at one Place i don't need to Go through all the sites and apps again and again and go Throught the sites. 

# Chatbot_electronicsprice - Chatbot only made for Electronics Product like mobile And Laptops only.
# The Api Response Most of The time Correct But Sometime its Not because ITs NOt the Paid ONE And its From Third Party Site.IM Not using Amazone or Flipkart Api's To Fetch Product Details They All are Paid. 


# Install the needed dependencies
```python -r requirements.txt```


# To Run this project
```python app.py```


# Docker Setup In EC2 commands to be Executed
# optional
```sudo apt-get update -y```
```sudo apt-get upgrade ```
# required
``` curl -fsSL https://get.docker.com -o get-docker.sh ```
``` sudo sh get-docker.sh ```
``` sudo usermod -aG docker ubuntu ```
```newgrp docker```

# Configure EC2 as self-hosted runner:
# Setup github secrets:
```AWS_ACCESS_KEY_ID=```
```AWS_SECRET_ACCESS_KEY=```
```AWS_REGION = us-east-1```
```AWS_ECR_LOGIN_URI = demo>> 566373416292.dkr.ecr.ap-south-1.amazonaws.com```
```ECR_REPOSITORY_NAME = simple-app```

