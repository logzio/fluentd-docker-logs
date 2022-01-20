import time
import os


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
        additional_fields = os.environ['ADDITIONAL_FIELDS']

        additional_fields = additional_fields.split(',')
        if len(additional_fields) > 0:
            extra_configuration = self._parse_additional_fieds(
                additional_fields)

            with open('./fluentd/etc/fluent_record_modifier.conf', "w") as file:
                file.write('')
                file.write(extra_configuration)

    def run(self):
        os.system("/bin/entrypoint.sh fluentd")


if __name__ == '__main__':
    w = FluentdManager()
    w.populate_additional_fields()
    w.run()
