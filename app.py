import time
import os
import subprocess


class FluentdManager:
    def __init__(self):
        print('Starting...')

    def _parse_additional_fieds(self, additional_fields):
        configuration_start = ['<filter> \n',
                               '@type record_modifier\n', '<record>\n']
        configuration_end = ['</record>\n', '</filter> \n']

        for field in additional_fields:
            parsed_field = field.split('=')
            configuration_start.append(
                parsed_field[0] + ' "' + parsed_field[1] + '" \n')
        full_configuration = configuration_start + configuration_end
        return ''.join(full_configuration)

    def populate_additional_fields(self):

        additional_fields = [ad.strip()
                             for ad in os.environ["ADDITIONAL_FIELDS"].split(",")]
        if len(additional_fields) > 0:
            extra_configuration = self._parse_additional_fieds(
                additional_fields)

            with open('./fluentd/etc/fluent_record_modifier.conf') as file:
                file.write('')
                file.write(extra_configuration)

    def run(self):
        subprocess.call("/bin/entrypoint.sh fluentd")


if __name__ == '__main__':
    w = FluentdManager()
    if 'ADDITIONAL_FIELDS' in os.environ:
        w.populate_additional_fields()
    w.run()
