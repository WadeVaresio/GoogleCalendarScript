# Google Calendar Script

A python script to add google calendar events via the command line

## Use
Currently you must be in the same directory of the script to execute.
There are 3 mandatory parameters you must supply:

* Summary - the title of the event
* Start - the start time of the event
* Priority - the priority of the event (high, normal, none)

Example:
`` python3 main.py "Event Name" 2019-02-20T08:00 high``
This will create a google calendar event with the title "Event Name" on February 20, 2019 at 8:00AM with notifications five days in advance
For help run ``python3 main.py -h``

### Suggested Terminal Usage
Add the calevent python file to wherever you like to keep your exectuable scripts, then export this path to your PATH.

#### Time Parameter
For information on the formatting of the start and end time parameters refer to [this.](https://tools.ietf.org/html/rfc3339#section-5.8)

#### Priority Parameter
How often you will receive notifications of the event
* high - 7 days in advance
* normal - 3 days in advance
* none - no notifications
