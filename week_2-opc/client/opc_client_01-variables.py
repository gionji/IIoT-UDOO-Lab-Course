import json
import sys
import threading
from time import sleep

sys.path.insert(0, "..")

from opcua import Client, ua


class SubHandler(object):
    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        var_name = get_variable_name_by_node(node)
        message = packOutputMessage(var_name ,val)
        mqtt_client.publish('/sensors', json.dumps(message))

    def event_notification(self, event):
        print("# EVENT # Python: New event", event.Message)



def main():
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")

    try:
        client.connect()

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Objects node is: ", root)
        print("Children of root are: ", root.get_children())

        server_namespace = "http://examples.freeopcua.github.io"
        idx = client.get_namespace_index( server_namespace )

        # Now getting a variable node using its browse path
        obj = root.get_child(["0:Objects", "2:MyObject"])
        print("My Object object is: ", obj)

        ## simply read variables, properties, and arrays
        myvar = root.get_child(["0:Objects", "2:MyObject", "2:MyFirstVariable"])
        print("myvar is: ", myvar.get_value() )
        myvar.set_value(3.9)  # if the var on the server is writable
        print("myvar is: ", myvar.get_value() )


        myprop = root.get_child(["0:Objects", "2:MyObject", "2:MyFirstVariable"])
        print("myprop is: ", myprop.get_value() )
        myprop.set_value(3.9)  # if the var on the server is writable
        print("myprop is: ", myprop.get_value() )

        ## subscribe to variables change
        subscribed_variables_dict = dict()
        subscribed_variables      = list()

        for var in VARS_NAMES:
            myvar = root.get_child(["0:Objects", "2:ChargeController", "2:" + str(var)])
            subscribed_variables.append( myvar )
            subscribed_variables_dict[ str(myvar)  ] = str(myvar.get_browse_name().to_string())

        msclt = SubHandler()
        sub = client.create_subscription(100, msclt)
        for var in subscribed_variables:
            handle = sub.subscribe_data_change(var)

        ## subscribe to events
        myevent = root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:LowBatteryEvent"])
        print("MyFirstEventType is: ", myevent)

        handle = sub.subscribe_events(obj, myevent)

        ## methods


        while True:
            sleep(1)

        sub.unsubscribe(handle)
        sub.delete()
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
