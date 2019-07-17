import pyautogui as pgui
import time
# Dont worry about it - Kendall Jackson github.com/kendallwww
urls = ['https://www.nyrestaurantcatskill.com/contact','https://lapelpinsandcoins.com/','http://www.janiservinc.com/']
# Adding new websites
urls.append('www.sunstateford.com')
urls.append('https://www.tuffymetrowest.com/')
urls.append('https://escapetheroom.com/new-york/?utm_source=GMBlisting&utm_medium=organic')


for i in range(len(urls)):

    # Click url bar
    pgui.click(1358,93)
    time.sleep(.55)

    # typewrite url
    pgui.typewrite(urls[i])
    time.sleep(0.25)

    pgui.press('\n')
    time.sleep(3.25)

    # Click extension
    pgui.click(2464, 82)
    time.sleep(.75)
    # Click copy all
    pgui.click(2423, 197)
    time.sleep(0.25)
    # Ctrl-tab to docs
    pgui.hotkey('ctrl', 'tab')
    time.sleep(0.5)
    #tab in
    pgui.press('tab')
    time.sleep(0.25)
    # Paste it
    pgui.hotkey('command', 'v')
    time.sleep(0.25)
    # Rinse & Repeat
    pgui.click(1241, 53)
    time.sleep(0.15)


print('Done! check the google doc.')

##while True:
##       print(pgui.position())
##
