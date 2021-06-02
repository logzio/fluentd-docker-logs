# Fluentd-docker-logs

fluentd-docker-logs is a Docker container that uses fluentd to collect logs from other Docker containers and forward those logs to your Logz.io account.

To use this container, you'll set environment variables in your `docker run` command.
fluentd-docker-logs uses those environment variables to generate a valid fluentd configuration for the container.
fluentd-docker-logs mounts docker.sock and the Docker logs directory to the container itself, allowing fluentd to collect the logs and metadata.

fluentd-docker-logs ships logs only.

## fluentd-docker-logs setup

### 1. Pull the Docker image

Download the logzio/fluentd-docker-logs image:

```shell
docker pull logzio/fluentd-docker-logs
```

### 2. Run the container

For a complete list of options, see the parameters below the code block.👇

```shell
docker run -it --rm \
--name fluentd-docker-logs \
-v $(pwd)/log:/fluentd/log \
-v /var/lib/docker/containers:/var/lib/docker/containers \
-v /var/run/docker.sock:/var/run/docker.sock:ro \
-e LOGZIO_LOG_LISTENER=<<LOGZIO_LOG_LISTENER>> \
-e LOGZIO_LOG_SHIPPING_TOKEN=<<LOGZIO_LOG_SHIPPING_TOKEN>> \
-e LOGZIO_TYPE=<<LOGZIO_TYPE>> \
-e LOGZIO_INCLUDE_REGEX=<<LOGZIO_INCLUDE_REGEX>> \
logzio/fluentd-docker-logs:latest
```

#### Parameters



| Parameter | Description |
|---|---|
| LOGZIO_LOG_SHIPPING_TOKEN | **Required**. Your Logz.io account token. Replace `LOGZIO_LOG_SHIPPING_TOKEN` with the [token](https://app.logz.io/#/dashboard/settings/general) of the account you want to ship to. |
| LOGZIO_LOG_LISTENER | **Default**: `https://listener.logz.io:8071` .<br> with your region’s listener host . For more information on finding your account’s region, see Account region. |
| LOGZIO_TYPE | **Default**: `docker-fluentd` <br> The log type you'll use with this Docker. This is shown in your logs under the `type` field in Kibana. <br> Logz.io applies parsing based on `type`. |
| LOGZIO_INCLUDE_REGEX | **Default**: `.+` <br>  Specifies regex expresion to match against container names, logs from containers that their name does not match the expresion will not be sent. |
| LOGZIO_BUFFER_TYPE | **Default**: `file` <br>  Specifies which plugin to use as the backend. |
| LOGZIO_BUFFER_PATH | **Default**: `/var/log/Fluentd-buffers/stackdriver.buffer` <br>  Path of the buffer. |
| LOGZIO_OVERFLOW_ACTION | **Default**: `block` <br>  Controls the behavior when the queue becomes full. |
| LOGZIO_CHUNK_LIMIT_SIZE | **Default**: `2M` <br>  Maximum size of a chunk allowed |
| LOGZIO_QUEUE_LIMIT_LENGTH | **Default**: `6` <br>  Maximum length of the output queue. |
| LOGZIO_FLUSH_INTERVAL | **Default**: `5s` <br>  Interval, in seconds, to wait before invoking the next buffer flush. |
| LOGZIO_RETRY_MAX_INTERVAL | **Default**: `30s` <br>  Maximum interval, in seconds, to wait between retries. |
| LOGZIO_FLUSH_THREAD_COUNT | **Default**: `2` <br>  Number of threads to flush the buffer. |
| LOGZIO_LOG_LEVEL | **Default**: `info` <br> The log level for this container. |
### 3. Check Logz.io for your logs

Spin up your Docker containers if you haven’t done so already. Give your logs a few minutes to get from your system to ours, and then open [Kibana](https://app.logz.io/#/dashboard/kibana).

### Change log
