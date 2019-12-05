FROM centos
RUN yum update -y
RUN yum install epel-release -y
RUN yum install python-pip -y
RUN yum install git -y
RUN yum install make -y
RUN yum install nginx -y
RUN yum install vim -y
RUN yum install expect -y
RUN pip install pelican
RUN pip install Markdown
RUN pip install typogrify
RUN pip install ghp-import
ADD ./create-blog.sh /srv/create-blog.sh
RUN bash -c /srv/create-blog.sh

CMD ["nginx", "-g", "daemon off;"]

EXPOSE 80