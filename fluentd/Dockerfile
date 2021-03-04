FROM fluent/fluentd:v1.12.0-1.0

ADD custom-fluent.conf /fluentd/etc/
ENV FLUENTD_CONF="custom-fluent.conf"

EXPOSE 9880
EXPOSE 24224 5140