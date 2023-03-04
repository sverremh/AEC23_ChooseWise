from filter_json import append_post_to_json

write_path = f'Data\\els_with_epd_vals_appended.json'
# #window
# append_post_to_json(write_path, number='x.x-x.x,0x',
#                     name = 'test_post', description= "This is a test operation",
#                     price = 1000000000,
#                     time = 24, b3 = 0.001, b4 = 1)
#demolition wall
append_post_to_json(write_path, number='9.1-9.1,01',
                    name = 'Demolish wall', description= "Demolition of walls. Sledgehammer and strong polish worker. Preferrably shirtless. Sober is optional. Multiply time by 2, risk by 5.",
                    price = 1000000000,
                    b3 = 0.0003, b4 = 0.0242961
)
#demilition roof
append_post_to_json(write_path, number='9.1-9.1,02',
                    name = 'Demolish roof', description= "Demolition of roof. ",
                    price = 1000000000,
                    b3 = 0.0005, b4 = 0.0429633
)


    

    