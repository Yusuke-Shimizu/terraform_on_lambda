FROM public.ecr.aws/lambda/python:3.8

# Install terraform
ARG terraform_version="0.14.2"
ADD https://releases.hashicorp.com/terraform/${terraform_version}/terraform_${terraform_version}_linux_amd64.zip terraform_${terraform_version}_linux_amd64.zip
RUN yum -y install unzip wget
RUN unzip ./terraform_${terraform_version}_linux_amd64.zip -d /usr/local/bin/
RUN rm -f ./terraform_${terraform_version}_linux_amd64.zip
ENV TF_DATA_DIR /tmp

# aws
ENV AWS_ACCESS_KEY_ID 【アクセスキー】
ENV AWS_SECRET_ACCESS_KEY 【シークレットキー】

# copy files
COPY app.py ${LAMBDA_TASK_ROOT}
COPY main.tf ${LAMBDA_TASK_ROOT}

CMD [ "app.handler" ]
