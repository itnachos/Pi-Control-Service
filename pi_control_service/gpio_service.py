from rpc import RPCService
from pi_pin_manager import PinManager


ALLOWED_ACTIONS = ('on', 'off', 'read')


class GPIOService(RPCService):

    def __init__(self, rabbit_url, device_key, pin_config):
        self.pins = PinManager(config_file=pin_config)
        super(GPIOService, self).__init__(
            rabbit_url=rabbit_url,
            queue_name='gpio_service',
            device_key=device_key,
            request_action=self._perform_gpio_action)

    def _perform_gpio_action(self, instruction):
        result = {'error': 1, 'pin': instruction['pin'], 'response': "An error occurred"}

        if instruction['action'] not in ALLOWED_ACTIONS:
            result['response'] = "'action' must be one of: {0}".format(', '.join(ALLOWED_ACTIONS))
            return result

        try:
            result['response'] = getattr(self.pins, instruction['action'])(int(instruction['pin']))
            result['error'] = 0
        except ValueError:
            result['response'] = "'pin' value must be an integer"
        except:
            pass
        return result

    def stop(self):
        self.pins.cleanup()
        super(GPIOService, self).stop()