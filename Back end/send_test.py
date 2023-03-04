from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account, get_local_accounts
from specklepy.transports.server import ServerTransport
from specklepy.api import operations
from specklepy.api.wrapper import StreamWrapper
from specklepy.transports.memory import MemoryTransport
from specklepy.api import operations
from specklepy.objects import Base

# The id of the stream to work with (we're assuming it already exists in your default account's server)
streamId = "9a259f0211"
branchName = "tes1"

# Initialise the Speckle client pointing to your specific server.
client = SpeckleClient(host="https://speckle.xyz")

# Get the default account
account = get_default_account()
# If you have more than one account, or the account is not the default, use get_local_accounts
# accounts = get_local_accounts()
# account = accounts[0]

# Authenticate using the account token
client.authenticate(token=account.token)
# Get the main branch with it's latest commit reference
branch = client.branch.get(streamId, "main", 0)
# Get the id of the object referenced in the commit
#objHash = branch.commits.items[0].referencedObject

# Create the server transport for the specified stream.
transport = ServerTransport(client=client, stream_id=streamId)

# Receive the object
#received_base = operations.receive(obj_id=objHash, remote_transport=transport)


# The received object, process it as you wish.
#print("Received object:", received_base)

# TODO: Perform some operation on the received data

# Getting server transports from the `StreamWrapper`

wrapper = StreamWrapper(
    "https://speckle.xyz/streams/9e730f9975/commits/dc64e71789"
)

# the stream wrapper gives you an authenticated server transport provided you have a corresponding local account

received_base = client.object.get(streamId, hash)

print(received_base)
# Using transports to send and receive

# commit = wrapper_client.commit.get(wrapper.stream_id, wrapper.commit_id)

# commit_obj = operations.receive(commit.referencedObject, transport)


# hash = operations.send(commit_obj, [transport])


# # if you want to, you can also serialise and deserialise yourself
# json_string = operations.serialize(commit_obj)

# base_object = operations.deserialize(json_string)

# print(json_string)
# print(base_object)

# # # Send the points using a specific transport
# # newHash = operations.send(base=received_base, transports=[transport])

# # # you can now create a commit on your stream with this object
# # commit_id = client.commit.create(
# #     stream_id=streamId,
# #     branch_name=branchName,
# #     object_id=newHash,
# #     message="Automatic commit created the python starter example",
# #     source_application="PyStarter"
# # )

# # print("Successfully created commit with id: ", commit_id)