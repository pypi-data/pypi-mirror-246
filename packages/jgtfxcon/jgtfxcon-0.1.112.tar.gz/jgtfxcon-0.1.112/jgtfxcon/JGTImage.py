
# %%
#@title Import
import cv2
import numpy as np
import io
from matplotlib import pyplot as plt


# %% [markdown]
# # Brightener

# %% [markdown]
# ## Automated

# %%
def img_histogram_view(hist,gray,minimum_gray,maximum_gray):
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()

    # Automatic brightness and contrast optimization with optional histogram clipping
def automatic_brightness_and_contrast(image, clip_hist_percent=11,showhistogram=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calculate grayscale histogram
    hist = cv2.calcHist([gray],[0],None,[256],[0,256])
    hist_size = len(hist)

    # Calculate cumulative distribution from the histogram
    accumulator = []
    accumulator.append(float(hist[0]))
    for index in range(1, hist_size):
        accumulator.append(accumulator[index -1] + float(hist[index]))

    # Locate points to clip
    maximum = accumulator[-1]
    clip_hist_percent *= (maximum/100.0)
    clip_hist_percent /= 2.0

    # Locate left cut
    minimum_gray = 0
    while accumulator[minimum_gray] < clip_hist_percent:
        minimum_gray += 1

    # Locate right cut
    maximum_gray = hist_size -1
    while accumulator[maximum_gray] >= (maximum - clip_hist_percent):
        maximum_gray -= 1

    # Calculate alpha and beta values
    alpha = 255 / (maximum_gray - minimum_gray)
    beta = -minimum_gray * alpha

    '''
    # Calculate new histogram with desired range and show histogram 
    new_hist = cv2.calcHist([gray],[0],None,[256],[minimum_gray,maximum_gray])
    plt.plot(hist)
    plt.plot(new_hist)
    plt.xlim([0,256])
    plt.show()
    '''
    if showhistogram:
        img_histogram_view(hist,gray,minimum_gray,maximum_gray)


    auto_result = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    # if showhistogram:
    #     img_histogram_view(hist,gray,minimum_gray,maximum_gray)

    return (auto_result, alpha, beta)


# %%

def abc(imgctx,resultprefix,seqit=25,ext='.png',showhistogram=False):
  resultfn=resultprefix+'-'+str(seqit)+ext
  image = cv2.imread(imgctx)
  auto_result, alpha, beta = automatic_brightness_and_contrast(image,seqit,showhistogram)
  print('<!--alpha', alpha,'-->')
  print('<!--beta', beta,'-->')
  #cv2.imshow('auto_result', auto_result)
  cv2.imwrite(resultfn, auto_result)
  print('#### ' + str(seqit))
  print('!['+str(seqit)+']('+resultfn+')')
  return auto_result
