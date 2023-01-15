import sys
import zulip

if __name__ == '__main__':

    # Pass the path to your zuliprc file here.
    client = zulip.Client(config_file="config.ini")

    # Print every message the current user would receive
    # This is a blocking call that will run forever
    client.call_on_each_message(lambda event: sys.stdout.write(str(event) + "\n"))
