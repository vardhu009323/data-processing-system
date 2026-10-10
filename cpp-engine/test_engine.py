
from engine import process_numbers

result = process_numbers([12, 45, 7, 23])

assert result["maximum"] == 45
assert result["minimum"] == 7
assert result["sum"] == 87

print("Engine integration tests passed!")
print(result)
