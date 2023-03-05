from specklepy.api import operations
from specklepy.api.wrapper import StreamWrapper

def get_data_from_speckle(stream_id, object_id):
    """
    Retrieves data from Speckle by stream id and object id.
    Used to test how to access information from Speckle elements. Walls in this case.

    Parameters
    ----------
    elem : Speckle Element
        The element to calculate the renovation cost of.
    
    object_id: string
        Id of the speckle object to reviece.

    Returns
    -------
    messages list[str]
        Information about all the wall elements' height in the speckle stream.
    """
    #inputs
    #object_id = "1b55273fd839ade53ee994f90f8a98ba"
    #stream_id = "9e730f9975"
    #code
    
    stream_url = "https://speckle.xyz/streams/" + stream_id
    wrapper = StreamWrapper(stream_url)
    transport = wrapper.get_transport()
    rec = operations.receive(object_id, transport)
    
    msg_parts =[]
    for wall in rec["@Walls"]:
        info = "height wall = " + str(wall.height)
        msg_parts.append(info)

        
    return msg_parts  
    