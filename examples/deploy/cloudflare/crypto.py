"""
crypto.py - ed25519 signature check (RFC 8032), to replace PyNaCl (This was AI-assisted).
"""

import hashlib

P = 2 ** 255 - 19
Q = 2 ** 252 + 27742317777372353535851937790883648493
D = -121665 * pow(121666, -1, P) % P
SQRT_M1 = pow(2, (P - 1) // 4, P)

def decompress(data):
  y = int.from_bytes(data, 'little')
  sign = y >> 255
  y &= (1 << 255) - 1
  if y >= P:
    return None
  x2 = (y * y - 1) * pow(D * y * y + 1, -1, P) % P
  x = pow(x2, (P + 3) // 8, P)
  if (x * x - x2) % P:
    x = x * SQRT_M1 % P
  if (x * x - x2) % P or (x == 0 and sign):
    return None
  if x & 1 != sign:
    x = P - x
  return x, y, 1, x * y % P # extended coordinates (X, Y, Z, T)

def add(a, b):
  x1, y1, z1, t1 = a
  x2, y2, z2, t2 = b
  e = (y1 - x1) * (y2 - x2) % P
  f = (y1 + x1) * (y2 + x2) % P
  c = 2 * D * t1 * t2 % P
  g = 2 * z1 * z2 % P
  e, f, g, h = f - e, g - c, g + c, f + e
  return e * f % P, g * h % P, f * g % P, e * h % P

BASE = decompress((4 * pow(5, -1, P) % P).to_bytes(32, 'little'))
ZERO = 0, 1, 1, 0

def double_multiply(a, point_a, b, point_b): # a * point_a + b * point_b in one pass
  both = add(point_a, point_b)
  result = ZERO
  for bit in range(max(a.bit_length(), b.bit_length()) - 1, -1, -1):
    result = add(result, result)
    match (a >> bit) & 1, (b >> bit) & 1:
      case 1, 1:
        result = add(result, both)
      case 1, 0:
        result = add(result, point_a)
      case 0, 1:
        result = add(result, point_b)
  return result

def ed25519_verify(public_key, message, signature):
  if len(public_key) != 32 or len(signature) != 64:
    return False
  point_r = decompress(signature[:32])
  point_a = decompress(public_key)
  s = int.from_bytes(signature[32:], 'little')
  if point_r is None or point_a is None or s >= Q:
    return False
  h = int.from_bytes(hashlib.sha512(signature[:32] + public_key + message).digest(), 'little') % Q
  x, y, z, _ = double_multiply(s, BASE, Q - h, point_a) # s * B - h * A, which should equal R
  return (x * point_r[2] - point_r[0] * z) % P == 0 and (y * point_r[2] - point_r[1] * z) % P == 0
