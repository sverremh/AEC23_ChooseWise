from specklepy.api.wrapper import StreamWrapper

# provide any stream, branch, commit, object, or globals url
wrapper = StreamWrapper("https://speckle.xyz/streams/9a259f0211/commits/9cb2afab34")

# get an authenticated SpeckleClient if you have a local account for the server
client = wrapper.get_client()

# get an authenticated ServerTransport if you have a local account for the server
transport = wrapper.get_transport()