import sys
sys.path.insert(0, "..")

from opcua import ua, Server,

try:
    from IPython import embed
except ImportError:
    import code

    def embed():
        vars = globals()
        vars.update(locals())
        shell = code.InteractiveConsole(vars)
        shell.interact()




class RandomEventsGenerator(Thread):
    def __init__(self, event):
        Thread.__init__(self)
        self._stopev = False
        self.event = event

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            if random.random() > 0.9
            self.event.trigger(message="This is simplest Event")
            time.sleep(0.1)



def main():
    # setup our server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace, not really necessary but should as spec
    server_namespace = "http://examples.freeopcua.github.io"
    address_space = server.register_namespace( server_namespace )

    # get Objects node, this is where we should put our custom stuff
    objects_node = server.get_objects_node()

    # Add the ocp objects (vars, features,...)
    # cresting the first object
    my_first_object = objects_node.add_object(address_space, "MyFirstObject")


    # creating a default event object
    # The event object automatically will have members for all events properties
    # you probably want to create a custom event type, see other examples
    my_first_event_generator = server.get_event_generator()
    my_first_event_generator.event.Severity = 300

    # Creating a custom EVENT
    eventType = server.create_custom_event_type(
                    address_space,
                    'ThresholdEvent',
                    ua.ObjectIds.BaseEventType,
                    [
                        ('value',        ua.VariantType.Float),
                        ('alarmEnabled', ua.VariantType.Boolean),
                    ]
                )
    my_custom_event_generator = server.get_event_generator(eventType, my_first_object)


    # starting!
    server.start()
    print( "Server starting ...")

    rndEv = RandomEventsGenerator(my_first_event_generator)  # just  a stupide class update a variable
    rndEv.start()

    while True:
        time.sleep(1)

        sensor_value = random.random()
        threshold = 0.9

        if sensor_value > threshold:
            my_custom_event_generator.event.Message = ua.LocalizedText("Value is graeter than th")
            my_custom_event_generator.event.value =  ua.Variant(sensor_value, ua.VariantType.Float)
            my_custom_event_generator.event.alarmenabled =  ua.Variant( outputsEnabled , ua.VariantType.Boolean)
            my_custom_event_generator.event.Severity =  ua.Variant( 1 , ua.VariantType.Int32)
            my_custom_event_generator.trigger()


if __name__ == "__main__":
    main()
