module.exports.convertCase = function(text) {
  let arr = text.split(' ');
  
  arr = arr.filter((elem) => {
    return elem !== '';
  })

  arr = arr.map((word) => {
    word = word.toLowerCase();
    word = word.replace(word[0], word[0].toUpperCase());
    return word;
  })

  let resStr = arr.reduce((res, word) => {
    return res + ' ' + word;
  },
  '').trim();

  return resStr;
}

// console.log(convertCase('   wEsT    BenGal   xD  '))