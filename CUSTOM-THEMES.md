Custom Themes
=============

Changing colors of your prompt in Promptastic is as easy as creating a new custom theme. First create and activate your custom theme, then edit it!

1. Create and activate a new theme
----------------------------------
- Copy the file `themes/default.py` into `themes/mycustomtheme.py`;
- Activate your custom theme it by editing the file `config.py` and setting:
```
THEME = 'mycustomtheme'
```

2. Edit a custom theme
----------------------
Once you created and activated you custome theme, f.i. `themes/mycustomtheme.py`, you can easily edit it and save it and you will see the effects on your prompt straight away.

For example if you set:
```
USERATHOST_BG = 124
```
you will see that the background color of the first segment is now red.
So, now you wonder how come that `124` means red-color.

### 2.1. Available colors
First check the file `utils/colors.py`: some colors are defined there and in your custom theme you can either use their numeric value (like `124` for red) or their pythonic name (like `colors.RED` for the same red).

If you want to print all the available colors in your system, just run:
```
$ python utils/extra/print_colors.py
```
You will see a long list of items where each item is made of:
- the text "user_name@localhost" with a different color used as background
- the text "background=N" where N is the number which corresponds to the specific color.
![Print colors](https://cloud.githubusercontent.com/assets/6423485/7671121/78edac2c-fcbf-11e4-9010-8731641dcc49.png)
