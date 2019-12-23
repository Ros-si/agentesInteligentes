import cv2

def compare_image(image_1_path, image_2_path):
    minimum_commutative_image_diff = 1
    image_1 = cv2.imread(image_1_path, 0)
    image_2 = cv2.imread(image_2_path, 0)
    commutative_image_diff = get_image_difference(image_1, image_2)

    if commutative_image_diff < minimum_commutative_image_diff:
        return commutative_image_diff
    return 10000 #//random failure value

def get_image_difference(image_1, image_2):
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_template_probability_match = cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
    img_template_diff = 1 - img_template_probability_match

    # taking only 10% of histogram diff, since it's less accurate than template method
    commutative_image_diff = (img_hist_diff / 10) + img_template_diff
    return commutative_image_diff