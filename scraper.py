from scraperlib import *
from ascii_magic import AsciiArt, from_image

# Print ascii art
my_art = AsciiArt.from_image('images\\untrusted.jpg')
my_art.to_terminal()
print('')
print('') # Header space

print("Welcome to Ping's Untrusted Scraper!")
print("We support many types of logs here, but many will not work. If one seems odd, try another one or contact me.")
print("What type you want to download?:")
def let_user_pick(options):
    print("") # empty line for space
    for idx, element in enumerate(options):
        print("{}) {}".format(idx + 1, element))
    i = input("Enter number: ")
    try:
        if 0 < int(i) <= len(options):
            return int(i) - 1
    except:
        pass
    return None
options = ["Automatic selection (Recommended)","Old (Est. November 17, 2022 - December 12, 2022)", "Newest (Est. December 13, 2022 - Present)"]
res = let_user_pick(options)

if options[res] == "Automatic selection (Recommended)":
    URL = input("Enter the URL of the log: ")
    auto(URL)
    print("Done! If everything went well, you should have a folder with the log in it. Please read the README.md file for more information.")
    input("Press any key to exit...")
if options[res] == "Old (Est. November 17, 2022 - December 12, 2022)":
    URL = input("Enter the URL of the log: ")
    old(URL)
    print("Done! If everything went well, you should have a folder with the log in it. Please read the README.md file for more information.")
    input("Press any key to exit...")
if options[res] == "Newest (Est. December 13, 2022 - Present)":
    URL = input("Enter the URL of the log: ")
    new(URL)
    print("Done! If everything went well, you should have a folder with the log in it. Please read the README.md file for more information.")
    input("Press any key to exit...")
