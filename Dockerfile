FROM centos

LABEL maintainer="f923383879@gmail.com"

ENV LANG=C.utf8 TZ=Asia/Shanghai

# Copy app
COPY . /var/www/adsupport

# Install nginx,python,uwsgi
RUN yum -y install https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm \
    && yum -y install python36 uwsgi uwsgi-plugin-python36 nginx \
    && mv /var/www/adsupport/uwsgi/nginx_adsupport.conf /etc/nginx/conf.d/adsupport.conf \
    && yum clean all

WORKDIR /var/www/adsupport

EXPOSE 10080

CMD /usr/sbin/nginx && /usr/sbin/uwsgi uwsgi/adsupport.ini
