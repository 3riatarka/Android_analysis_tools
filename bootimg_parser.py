#!/usr/bin/env python3

import sys, struct

if len(sys.argv) != 2:
	print(f"Usage: {sys.argv[0]} <boot.img file>")
	exit(1)

struct_fmt = '<8s L 4s L 4s L 4s 4s L 2s 16s 512s 8s'
struct_len = struct.calcsize(struct_fmt)
struct_unpack = struct.Struct(struct_fmt).unpack_from

with open(sys.argv[1], 'rb') as bootimg:
    data = bootimg.read(struct_len)
    magic, kernel_size, kernel_addr, ramdisk_size, ramdisk_addr, secondbl_size, secondbl_addr, kerneltags_addr, page_size, unused, product_name, cmd_line, ids = struct_unpack(data)

print('Android bootimg headers:')
print(f"    Magic  bytes: {magic.decode('utf-8')}")
print(f"    Product name: {product_name.decode('utf-8')}")
print(f"    Kernel  size: {kernel_size} bytes")
print(f"    kernel  addr: 0x{kernel_addr[::1].hex()}")
print(f"    Ramdisk size: {ramdisk_size} bytes")
print(f"    Ramdisk addr: 0x{ramdisk_addr[::-1].hex()}")
print(f"    2nd stage bootloader size: {secondbl_size} bytes")
print(f"    2nd stage bootloader addr: 0x{secondbl_addr[::-1].hex()}")
print(f"    Kernel tags addr: 0x{kerneltags_addr[::-1].hex()}")
print(f"    Flash page size: {page_size} bytes")
print(f"    Kernel command line: {cmd_line.decode('utf-8')}")
print(f"    ID: {ids[::-1].hex()}")
