import csv
import glob
bin_out = "2022_full.bin"
debug = False
data_dir = "D:\\userdata\\Downloads\\place"

# see https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

color_map = {
    '#FFFFFF': 0,
    '#000000': 1,
	'#898D90': 2,
    '#009EAA': 3,
    '#B44AC0': 4,
    '#9C6926': 5,
    '#811E9F': 6,
    '#51E9F4': 7,
    '#FFD635': 8,
    '#515252': 9,
    '#3690EA': 10,
    '#00756F': 11,
    '#BE0039': 12,
    '#DE107F': 13,
    '#00CCC0': 14,
    '#FFF8B8': 15,
    '#493AC1': 16,
    '#7EED56': 17,
    '#FFA800': 18,
    '#FF3881': 19,
    '#00CC78': 20,
    '#6D482F': 21,
    '#6D001A': 22,
    '#6A5CFF': 23,
    '#94B3FF': 24,
    '#00A368': 25,
    '#2450A4': 26,
    '#E4ABFF': 27,
    '#FFB470': 28,
    '#FF99AA': 29,
    '#FF4500': 30,
    '#D4D7D9': 31
}


file_order = [10,6,9,14,15,17,13,11,7,16,12,18,24,20,26,19,21,22,23,25,27,28,35,30,31,32,33,34,39,42,36,37,38,43,44,45,46,48,29,51,47,54,3,2,41,0,1,55,56,4,50,57,59,53,40,49,62,52,65,61,69,8,63,64,60,66,67,5,74,68,75,76,77,70,71,72,73,58,78]

buffer = bytearray()

def write_to_buffer(s):
    v = int(s, 2)
    buffer.append(v & 0xff)

part = 1
elements_count = 0

for file_id in file_order:
    file = f"{data_dir}\\2022_place_canvas_history-{file_id:0>12}.csv/header.txt"
    print(f"compressing {file}", flush=True)
    
    if elements_count > 8:
        part += 1
        elements_count = 0
        buffer = bytearray()

    
    with open(file, newline='') as csvfile:
        elements_count += 1
        
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        
        i = 0

        for row in reader:
            i += 1
            if i == 1: 
                continue
                
            #if i == 2:
            #    print(f"{file_id},    {row[0]}")
            #    break
            
            coords = row[3].split(",")
            if len(coords) == 2:
                x, y = coords
                x, y = int(x), int(y)
            elif len(coords) == 4:
                x, y, x2, y2 = coords
                x, y, x2, y2 = int(x), int(y), int(x2), int(y2)
                continue
            else:
                print("invalid coords")
                continue
            
            if x >= 2000: continue
            if y >= 2000: continue
            if x < 0: continue
            if y < 0: continue
            c = color_map[row[2]]
            
            bit_string = f'{x:011b}{y:011b}00{c:08b}'
            
            write_to_buffer(bit_string[0:8])
            write_to_buffer(bit_string[8:16])
            write_to_buffer(bit_string[16:24])
            write_to_buffer(bit_string[24:32])
            
            if debug:
                if i < 200:
                    print(bitstring_to_bytes(bit_string))
                    print(f"{x},{y},{c}")
                    print(bit_string)
                else:
                    pass
    
    #break #after first file (for debugging)
        
                    
    #print("converting and writing binary file", flush=True)

    with open(f"2022_part_{part}.bin", "wb") as out_file:
        out_file.write(buffer)
                    