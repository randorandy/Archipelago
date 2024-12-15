from .hack_randomizer.romWriter import RomWriter

# rusty's hacky script to redo the message boxes for yellow, blue, and green
# each index of the wrongbytes maps to its correct version in the right bytes

wrongbytes = ['0e00','4e3c','4e38','4e28',
              'e03c','e13c','e23c','e33c','e43c','e53c','e63c','e73c','e83c','e93c','ea3c','eb3c','ec3c','ed3c','ee3c','ef3c','f03c','f13c','f23c','f33c','f43c','f53c','f63c','f73c','f83c','f93c',
              'e038','e138','e238','e338','e438','e538','e638','e738','e838','e938','ea38','eb38','ec38','ed38','ee38','ef38','f038','f138','f238','f338','f438','f538','f638','f738','f838','f938',
              'e028','e128','e228','e328','e428','e528','e628','e728','e828','e928','ea28','eb28','ec28','ed28','ee28','ef28','f028','f128','f228','f328','f428','f528','f628','f728','f828','f928']
rightbytes = ['0f00','0f3c','0f38','0f28',
              'c03c','c13c','c23c','c33c','c43c','c53c','c63c','c73c','c83c','c93c','ca3c','cb3c','cc3c','cd3c','ce3c','cf3c','d03c','d13c','d23c','d33c','d43c','d53c','d63c','d73c','d83c','d93c',
              'c038','c138','c238','c338','c438','c538','c638','c738','c838','c938','ca38','cb38','cc38','cd38','ce38','cf38','d038','d138','d238','d338','d438','d538','d638','d738','d838','d938',
              'c028','c128','c228','c328','c428','c528','c628','c728','c828','c928','ca28','cb28','cc28','cd28','ce28','cf28','d028','d128','d228','d328','d428','d528','d628','d728','d828','d928']


def redo_message_table(rom_writer: RomWriter) -> RomWriter:

    for block in range(0x29963,0x2baa3, 2) :
        # for each pair of bytes starting at 29963 and ending at 2b7a7 (and 2b7a8)
        # extended to include 2baa1 (and 2baa2)
        bytes_data = rom_writer.readBytes(block,2)
        current_wrong_token = bytes_data.hex()
        if current_wrong_token in wrongbytes :
            current_index = wrongbytes.index(current_wrong_token)
            rom_writer.writeBytes(block, bytes.fromhex(rightbytes[current_index]))

    return rom_writer
