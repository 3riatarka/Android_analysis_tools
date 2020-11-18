#!/usr/bin/env python3

import sys, struct, math

if len(sys.argv) != 2:
	print(f"Usage: {sys.argv[0]} <boot.img file>")
	exit(1)

struct_fmt = '<8s L 4s L 4s L 4s 4s L 2s 16s 512s 8s'
struct_len = struct.calcsize(struct_fmt)
struct_unpack = struct.Struct(struct_fmt).unpack_from

with open(sys.argv[1], 'rb') as bootimg:
    data = bootimg.read(struct_len)
    magic, kernel_size, kernel_addr, ramdisk_size, ramdisk_addr, secondbl_size, secondbl_addr, kerneltags_addr, page_size, unused, product_name, cmd_line, ids = struct_unpack(data)

print('### Android bootimg headers:')
print(f"    Magic  bytes: {magic.decode('utf-8')}")
print(f"    Product name: {product_name.decode('utf-8')}")
print(f"    ID: {ids[::-1].hex()}")
print(f"    Kernel  size: {kernel_size} bytes")
print(f"    kernel  addr: 0x{kernel_addr[::-1].hex()}")
print(f"    Ramdisk size: {ramdisk_size} bytes")
print(f"    Ramdisk addr: 0x{ramdisk_addr[::-1].hex()}")
print(f"    2nd stage bootloader size: {secondbl_size} bytes")
print(f"    2nd stage bootloader addr: 0x{secondbl_addr[::-1].hex()}")
print(f"    Kernel tags addr: 0x{kerneltags_addr[::-1].hex()}")
print(f"    Flash page size: {page_size} bytes")
print(f"    Kernel command line: {cmd_line.decode('utf-8')}")

kernel_pages = math.ceil((kernel_size + page_size -1) / page_size)
kernel_offset = page_size
kernel_block_size = kernel_pages * page_size

print("\n\n### Kernel extraction information:")
print(f"  Kernel offset: {kernel_offset}")
print(f"  Kernel block: {kernel_pages} pages")
print(f"  Kernel block size:  {kernel_block_size} bytes") 
print(f"  Extraction command: dd if={sys.argv[1]} of={sys.argv[1]}_kernel.bin bs=1 skip={kernel_offset} count={kernel_block_size}")


ramdisk_pages = math.ceil((ramdisk_size + page_size - 1) / page_size)
ramdisk_offset = (1 + kernel_pages) * page_size ## The fist page is the header
ramdisk_block_size = ramdisk_pages * page_size

print("\n\n### Ramdisk extraction information:")
print(f"  Ramdisk offset: {ramdisk_offset}")
print(f"  Ramdisk block: {ramdisk_pages} pages")
print(f"  Ramdisk block size: {ramdisk_block_size} bytes")
print(f"  Extraction command: dd if={sys.argv[1]} of={sys.argv[1]}_ramdisk.bin bs=1 skip={ramdisk_offset} count={ramdisk_block_size}")

if secondbl_size != 0:
    secondbl_pages = math.ceil((secondbl_size + page_size -1) / page_size)
    secondbl_offset = (1 + kernel_pages + ramdisk_pages) * page_size ## The first page is the header
    secondbl_block_size = secondbl_pages * page_size

    print("\n\n### Second stage bootloader extraction information:")
    print(f"  2nd stage bootloader offset: {secondbl_offset}")
    print(f"  2nd stage bootloader block: {secondbl_pages} pages")
    print(f"  2nd stage bootloader block size: {secondbl_block_size} bytes")
    print(f"  Extraction command: dd if={sys.argv[1]} of={sys.argv[1]}_2stboodloader.bin bs=1 skip={secondbl_offset} count={secondbl_block_size}")
else:
    print("\n\n### Second stage bootloader not found")
