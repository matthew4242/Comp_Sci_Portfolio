"""
Summary => will apply the EdgesStlye to the image given.

Description => This class is going to control the proccessing of images for
            the EdgesStlye. It will take a the 'takenPicture.jpg'
            from the Image folder and then stlye it. The output will
            be a list of x and y coordinates for the plotter to print out
            later on.

Author => Matthew Howard (mah60).
Version =>   0.1 - 20/04/2018 -  create the basic class for the edges
                        algorithm. This code is yet to be complete.
             0.2 - 21/04/2018 - removed ui from __init_- method as not
                        used
             1.0 - 04/03/2018 - This is the Final version of the code.
"""
from __future__ import division
from image_processor import ImageProcessor
import numpy as np
import cv2


class EdgesStyle(ImageProcessor):
    """
    Summary => will apply the dithering algorithm to the image given.

    Description => This class is going to control the proccessing of images for
                the dithering algorithm. It will take a the 'takenPicture.jpg'
                from the Image folder and then stlye it. The output will
                be a list of x and y coordinates for the plotter to print out
                later on.

                This class inherits Imageprocessor and will take on the
                individual classes for it.

    args => None

    return => None
    """

    def __init__(self):
        """
        Summary => will initialize the image processor.

        Description => will initialize the images processor, to be used later
                    on.

        args => None

        return => None
        """
        super(EdgesStyle, self).__init__()

    def run(self):
        """
        Summary => will find the boarders in the image taken.

        Description => will find the boarders in the image take, using
                opencv. The will work by making the image graystyle, then
                using a GaussianBlur to filter the image. Then using sobal
                to calculate where the edges are.

                After this we use a threshold to swap the black and white
                colours around.

        args => None

        return => None
        """
        # get the image to be processed
        img = cv2.imread('Images/takenPicture.jpg', 0)
        # resize img given
        img = self.compress_image(img, 3)
        # img_edges = cv2.Canny(img, 80, 80)
        # blur the image so we can tell where the key boarders are
        blur = cv2.GaussianBlur(img, (5, 5), 0)
        # create a sobal diratives
        sobal = cv2.Sobel(blur, cv2.CV_64F, 1, 1, ksize=5)
        # convert the sobal diratives to canny_style
        # to view the edges of the image
        # sobalCopy = np.uint8(sobal) #  https://stackoverflow.com/questions
        # /19103933/depth-error-in-2d-image-with-opencv-python
        # canny = cv2.Canny(img, 25, 100, L2gradient=False)
        # save the final output
        # change image type to unit 8
        sobal = np.uint8(sobal)
        # creates a threshold to create a black and white image
        ret, threshold = cv2.threshold(sobal, 25, 255, cv2.THRESH_BINARY_INV)

        cv2.imwrite("Images/processedImage.jpg", threshold)
        # cv2.imwrite("Images/edges_style_example.jpg", threshold)

        self.calculate_coordinates(threshold)
