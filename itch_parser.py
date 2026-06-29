import gzip

def parse_add_order(payload):

    order_ref = int.from_bytes(bytes(payload[10:18]), 'big')
    timestamp_ns = int.from_bytes(bytes(payload[4:10]), 'big')
    side = chr(payload[18])
    shares = int.from_bytes(bytes(payload[19:23]), 'big')
    stocks = payload[23:31].decode('ascii').strip()
    price = int.from_bytes(bytes(payload[31:35]), 'big')

    return order_ref, timestamp_ns, side, shares, stocks, price

def parse_exit(payload):

    order_ref = int.from_bytes(bytes(payload[10:18]), 'big')
    timestamp_ns = int.from_bytes(bytes(payload[4:10]), 'big')

    return order_ref, timestamp_ns


def parse_itch_file(filepath):
    with gzip.open(filepath, 'rb') as f:
        
        add_ptypes = {'A', 'F'}
        exit_ptypes = {'C' , "D", "E"}

        open_orders = {}
        records= []

        while True:

            curr = f.read(2)
            if not curr:
                break 
            p_len = int.from_bytes(bytes(curr[0:2]), 'big')
            curr  = f.read(p_len)
            p_type = chr(curr[0])

            if p_type in add_ptypes:
                payload = bytes(curr[1: p_len])
                order_ref, timestamp_ns, side, shares, stocks, price = parse_add_order(payload)
                open_orders[order_ref] = [timestamp_ns, side, shares, stocks, price]

            elif p_type in exit_ptypes:
                payload = bytes(curr[1: p_len])
                order_ref, timestamp_ns = parse_exit(payload)
                if order_ref in open_orders:
                    diff = timestamp_ns - open_orders[order_ref][0]
                    records.append({
                        'order_ref': order_ref,
                        'add_ns': open_orders[order_ref][0],
                        'time_on_book_ns': diff,
                        'side': open_orders[order_ref][1],
                        'stock': open_orders[order_ref][3],
                        'exit_type' : p_type
                    })
                    del open_orders[order_ref]




        return records

    
            
        



        












