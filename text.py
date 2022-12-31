def convertCase(x):
  arr = x.split(' ')
  arr2 = [word.capitalize() for word in arr]
  result = ' '.join(arr2)
  return result

convertCase('wEst BenGaL')