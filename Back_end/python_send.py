from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api.wrapper import StreamWrapper
from specklepy.objects import Base
from specklepy.transports.server import ServerTransport

# Initialise the Speckle client pointing to your specific server.
client = SpeckleClient(host='https://speckle.xyz')

# Authenticate with your account.
account = get_default_account()
client.authenticate_with_account(account)

STREAM_ID="9e730f9975"
OBJ_ID = "6bf18ee3a41ce18d8936e92f26130d4e"

# Create a server transport for sending/receiving objects.
transport = ServerTransport(client=client, stream_id=STREAM_ID)

# Receive an object from the stream.
received_base = operations.receive(obj_id=OBJ_ID, remote_transport=transport)
welems = []

# Print some information about the received object.
for wall in received_base["@Walls"]:
    print(f"Height wall = {wall.height}")
    print(f"Type = {wall.type}")
    print(f"ID wall = {wall.get_id()}")
    welems.append(wall)

# Set properties for the received objects.
for elem in welems:
    elem.units = "m"
    params = elem.parameters
    params["gwp"] = "NEWGWP!"
    params["cost"] = "NEWCOST!"
    params["time"] = "NEWTIME!"
    print(params)

# Create a new Base object and send it to the stream.
stream_id = "9e730f9975"
branch_name = "svhs/branch_1"
base = Base(name="Test123", values=welems)

# Create a new transport for sending objects to the stream.
transport = ServerTransport(client=client, stream_id=stream_id)

# Send the new Base object to the stream.
hash = operations.send(base=base, transports=[transport])

# Create a new commit on the stream with the new object.
commit_id = client.commit.create(
    stream_id=stream_id,
    branch_name=branch_name,
    object_id=hash,
    message="Test upload from Python"
)

print(f"Sent {len(welems)} elements to stream {stream_id} with commit {commit_id}")