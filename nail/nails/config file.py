with open('config.txt', 'r') as f:
    nums = f.read().splitlines()
print(nums[0], nums[1])