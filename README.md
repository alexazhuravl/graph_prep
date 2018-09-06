The following repo contains .ipynb files that create a data for the future processing using NetworkX. 

There are two .ipynb files which are similar and the instruction can be applied to both of them. 

HOWTO:

0. Install dependencies: `pip install -r requirements.txt`

1. ```filenames = glob.glob("/path/to/files/out_file_mappings_*.json")```

Replace `/path/to/files/` with your own path to the directory where all your files are located. 

The `out_file_mappings_*.json` means that you will iterate over all files that are named like that and will look up for anything spesicified instead of asterisk. 

2. Make sure that you have installed `jupyter notebook` on your local machine. If not, this link will help you: https://jupyter.readthedocs.io/en/latest/install.html

3. Type in your terminal: `jupyter notebook`, that will open an editor in your browser.

4. Open file in browser, hit `SHIFT+ENTER` to execute the cells. 

5. You can find your exported file in your home directory. 
 



