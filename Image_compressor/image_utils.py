import random


def distort_random_block(data, dimension, num_blocks):
    result = bytearray(data)
    n = len(result)
    block_size = 1 if dimension == 1 else 2

    for _ in range(num_blocks):
        index = random.randint(0, n // block_size - 1)
        del result[index * block_size:(index + 1) * block_size]

    return result


def distort_image(data, dimension, num_packets, distortion_level):
    result = bytearray(data)
    n = len(result)
    packet_size = 1 if dimension == 1 else 2

    for _ in range(num_packets):
        index = random.randint(0, n // packet_size - 1)

        if dimension == 1:
            start = index * packet_size * distortion_level
            end = min(start + packet_size, n)
            for i in range(start, end):
                result[i] = random.randint(0, 255)
        elif dimension == 2:
            start_i = (index // (n // packet_size)) * distortion_level
            start_j = (index % (n // packet_size)) * distortion_level
            end_i = min(start_i + distortion_level, dimension)
            end_j = min(start_j + distortion_level, dimension)
            for i in range(start_i, end_i):
                for j in range(start_j, end_j):
                    index = (i * dimension + j) * packet_size
                    if index < n:
                        result[index] = random.randint(0, 255)

    return bytes(result)


def distort_random_bytes(data, num_bytes, distortion_level):
    result = bytearray(data)
    n = len(result)
    indices = random.sample(range(n), num_bytes)
    for idx in indices:
        byte = result[idx]
        distorted_byte = byte ^ (1 << distortion_level)
        result[idx] = distorted_byte
    return result


def distort_random_bits(data, num_bits, distortion_level):
    result = bytearray(data)
    n = len(result)
    for _ in range(num_bits):
        idx = random.randint(0, n - 1)
        bit_pos = random.randint(0, 7)
        byte = result[idx]
        distorted_byte = byte ^ (1 << bit_pos)
        result[idx] = distorted_byte
    return result