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

        msclt = SubHandler()
        sub = client.create_subscription(100, msclt)

        ## subscribe to events
        myevent = root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType", "2:ThresholdEvent"])
        print("MyFirstEventType is: ", myevent)
        handle = sub.subscribe_events(obj, myevent)

        myevent2 = root.get_child(["0:Types", "0:EventTypes", "0:BaseEventType"])
        print("MyFirstEventType is: ", myevent2)
        handle = sub.subscribe_events(obj, myevent2)

        while True:
            sleep(0.1)

        sub.unsubscribe(handle)
        sub.delete()
    finally:
        client.disconnect()

if __name__ == "__main__":
    main()
