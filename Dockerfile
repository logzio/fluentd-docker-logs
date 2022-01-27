FROM fluent/fluentd:v1.13-debian-1

# Use root account to use apt
USER root

# below RUN includes plugin as examples elasticsearch is not required
# you may customize including plugins as you wish
RUN buildDeps="sudo make gcc g++ libc-dev" \
	&& apt-get update \
	&& apt-get install -y python3-pip python3 \
	&& apt-get install -y --no-install-recommends $buildDeps \
	&& sudo gem install fluent-plugin-prometheus \
	&& sudo gem install fluent-plugin-logzio \
	&& sudo gem install fluent-plugin-record-modifier \
	&& sudo gem install fluent-plugin-docker_metadata_elastic_filter \
	&& sudo gem install fluent-plugin-detect-exceptions \
	&& sudo gem sources --clear-all \
	&& SUDO_FORCE_REMOVE=yes \
	apt-get purge -y --auto-remove \
	-o APT::AutoRemove::RecommendsImportant=false \
	$buildDeps \
	&& rm -rf /var/lib/apt/lists/* \
	&& rm -rf /tmp/* /var/tmp/* /usr/lib/ruby/gems/*/cache/*.gem

COPY fluent.conf /fluentd/etc/
COPY fluent_record_modifier.conf /fluentd/etc/
COPY entrypoint.sh /bin/
COPY app.py ./



ENV LOGZIO_LOG_LISTENER "https://listener.logz.io:8071"
ENV LOGZIO_TYPE "docker-fluentd"
ENV LOGZIO_INCLUDE_REGEX "(.+)"


ENV LOGZIO_BUFFER_TYPE "file"
ENV LOGZIO_BUFFER_PATH "/var/log/fluentd-buffers/stackdriver.buffer"
ENV LOGZIO_OVERFLOW_ACTION "block"
ENV LOGZIO_CHUNK_LIMIT_SIZE "2M"
ENV LOGZIO_QUEUE_LIMIT_LENGTH "6"
ENV LOGZIO_FLUSH_INTERVAL "5s"
ENV LOGZIO_RETRY_MAX_INTERVAL "30"
ENV LOGZIO_RETRY_FOREVER "true"
ENV LOGZIO_FLUSH_THREAD_COUNT "2"
ENV LOGZIO_SLOW_FLUSH_LOG_THRESHOLD "20.0"
ENV LOGZIO_CONTAINER_STATUS_REGEX  "running"

# Defaults value for system.conf
ENV LOGZIO_LOG_LEVEL "info"

CMD ["python3", "app.py"]
