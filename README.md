### Requirements
 + Runs with python2.7
 + Requires selenium module
 + ^ can be installed with `pip install selenium` on MacOS 
 + Run with `./run_bot`

### Functionality
 + Currently configured for supreme
 + Automates adding items from the shop to cart and filling out payment info
 + Items can be selected in the 'items' array in main()
 + Requires human intervention to complete CAPTCHA
 + When attempting to add an item from the shop that is sold out, all size 
  and style combinations will try to be added to the cart until an in stock
  combo is found. If all sizes and styles are sold out, the process will 
  return to the shop_url and contiune with the rest of the desired items
 + As of now, the first item of the item type (ie bags, hats, shirts) is
  selected to be added to the cart.
