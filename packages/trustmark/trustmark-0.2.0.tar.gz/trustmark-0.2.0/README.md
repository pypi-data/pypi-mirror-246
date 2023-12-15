# TrustMark - Universal Watermarking for Arbitrary Resolution Images

An implementation of TrustMark watemarking for the Content Authenticity Initiative (CAI) as described in: 

**TrustMark - Universal Watermarking for Arbitrary Resolution Images**
[Tu Bui](https://www.surrey.ac.uk/people/tu-bui), [Shruti Agarwal](https://research.adobe.com/person/shruti-agarwal/), [John Collomosse](https://www.collomosse.com)
https://arxiv.org/abs/2311.18297


### Quick start and example

Run `pip install trustmark to install the TrustMark package

The following example in Python shows typical usage:
```python
from trustmark import TrustMark
from PIL import Image

# initialize TrustMark - note in this release only variant C is packaged
tm=TrustMark(verbose=True, model_type='C')

# encoding example
cover = Image.open('ufo_240.jpg').convert('RGB')
tm.encode(cover, 'mysecret').save('ufo_240_C.png')

# decoding example
cover = Image.open('ufo_240_C.png').convert('RGB')
wm_secret, wm_present = tm.decode(cover)
if wm_present:
  print(f'Extracted secret: {wm_secret}')
else:
  print('No watermark detected')
```


