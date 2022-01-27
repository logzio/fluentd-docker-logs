import time
import os
import subprocess
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FluentdManager:
    def __init__(self):
        logger.info('Starting...')

    def _parse_additional_fieds(self, additional_fields):
        try:
            configuration_start = ['<filter> \n',
                                   '@type record_modifier\n', '<record>\n']
            configuration_end = ['</record>\n', '</filter> \n']
            for field in additional_fields:
                parsed_field = [ad.strip()
                                for ad in field.split("=")]
                if len(parsed_field) > 1:
                    configuration_start.append(
                        parsed_field[0] + ' "' + parsed_field[1] + '" \n')
            full_configuration = configuration_start + configuration_end
            return ''.join(full_configuration)
        except:
            logger.error(
                "Please check your ADDITIONAL_FIELDS,  pattern to use it should be fieldName1=fieldValue1,fieldName2=fieldValue2")

    def populate_additional_fields(self):
        additional_fields = [ad.strip()
                             for ad in os.environ["ADDITIONAL_FIELDS"].split(",")]
        logger.debug('Length of ADDITIONAL_FIELDS is: ',
                     len(additional_fields))
        if len(additional_fields) > 0:
            extra_configuration = self._parse_additional_fieds(
                additional_fields)
            try:
                with open('./fluentd/etc/fluent_record_modifier.conf', "w") as file:
                    file.write(extra_configuration)
            except Exception as e:
                logger.error(e)

    def run(self):
        try:
            subprocess.run(["/bin/entrypoint.sh", "fluentd"])
        except subprocess.CalledProcessError as e:
            logger.error(e)


if __name__ == '__main__':
    w = FluentdManager()
    if 'ADDITIONAL_FIELDS' in os.environ:
        w.populate_additional_fields()
    w.run()
