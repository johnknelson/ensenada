# Ensenada

Ensenada is a complete joke of an attempt to use a financial indicator library ([tulip](https://tulipindicators.org/)), to buy and sell against historical bitcoin data I scraped with a curl command that no longer works lmao. I also began to integrate with [ccxt](https://github.com/ccxt/ccxt), a unified crypto exchange API. 

This is basically crayons on the wall, but the thought of a trading bot is so enticing and I'm game to keep exploring. I probably need to read more before just writing a bunch of python (which I am not proficient at).

## Usage

The project is a mess. Maybe with more people looking or interested I/we will refine some useful pieces and add more good stuff. That said, if you run a test on a particular history file, you will see an output of a bunch of metrics, and a graph indicating price, PSAR value, and whether or not the program was holding for a given index.

I use [Pycharm](https://www.jetbrains.com/pycharm/) because I love Jetbrains. you will need to install all of the Python dependencies (via [pip](https://pip.pypa.io/en/stable/), most likely), which Pycharm makes really easy by prompting you to install and showing you red squiggles when action is needed.

You can run it by running `test_single_file.py`, and you should see a graph output like this:

![graph output](
https://user-images.githubusercontent.com/6634502/88358611-3850c680-cd35-11ea-8ac5-76d585016643.png)
