def get_A08241_measurements(cnt_order, contours, img_draw, img_name):
    ## Note this will be different on your computer
    #output_dir = '/Users/max.feldman/Documents/data/2020/A08241_imgs/std/output/'
    output_file_name = output_dir + "output_" + img_name + ".jpg"
    img_write = img_draw.copy()
    clone, rep, side, light = image_name.split("_")
    print(clone)
    print(rep)
    print(side)
    print(light)
    img_out = img_write.copy()
    ## Make column names for color tables
    r_names = ["r_" + str(s) for s in list(range(0, 256))]
    g_names = ["g_" + str(s) for s in list(range(0, 256))]
    b_names = ["b_" + str(s) for s in list(range(0, 256))]
    ## Make column names for shape table
    x_names = ["x_" + str(x) for x in list(range(1, 101))]
    y_names = ["y_" + str(y) for y in list(range(1, 101))]
    s_names = x_names + y_names
    summary_table = pd.DataFrame(columns=['img_name', 'clone', 'rep', 'side', 'light', 'tuber', 'cmx', 'cmy', 'area', 'perimeter', 'length', 'width', 'ratio', 'eccentricity','red_ave', 'green_ave', 'blue_ave'])
    ## Prepare empty tables for color and shape data
    r_table = pd.DataFrame(columns=r_names)
    g_table = pd.DataFrame(columns=g_names)
    b_table = pd.DataFrame(columns=b_names)
    s_table = pd.DataFrame(columns=s_names)
    tuber_no = [1,2,3,4,5,'marker']
    counter = 0
    print(rep)
    if (rep == '1'):
        tuber_no = [6,7,8,9,10,'marker']
    if (rep == '2'):
        tuber_no = [1,2,3,4,5,'marker']
    if (len(cnt_order) == 5):
        tuber_no = tuber_no[:4] + tuber_no[5:]
        cnt_order[-1] = len(cnt_order) - 1
    for idx, val in enumerate(cnt_order):
        #print(cn)
        #cnt = contours[idx]
        cnt = contours[val]
        tuber = tuber_no[counter]
        img_write = img_draw.copy()
        m = cv2.moments(cnt)
        area = m['m00']
        ix, iy, iz = np.shape(img_write)
        size = ix, iy, 3
        size1 = ix, iy
        background = np.zeros(size, dtype=np.uint8)
        background1 = np.zeros(size1, dtype=np.uint8)
        background2 = np.zeros(size1, dtype=np.uint8)
        background3 = np.zeros(size1, dtype=np.uint8)
        tuber_mask = background3.copy()
        cv2.drawContours(tuber_mask, [cnt], 0, (255, 255, 255), -1)
        hull = cv2.convexHull(cnt)
        m = cv2.moments(cnt)
        area = m['m00']
        perimeter = cv2.arcLength(cnt, closed=True)
        x, y, width, height = cv2.boundingRect(cnt)
        cmx, cmy = (float(m['m10'] / m['m00']), float(m['m01'] / m['m00']))
        center, axes, angle = cv2.fitEllipse(cnt)
        major_axis = np.argmax(axes)
        minor_axis = 1 - major_axis
        major_axis_length = float(axes[major_axis])
        minor_axis_length = float(axes[minor_axis])
        eccentricity = float(np.sqrt(1 - (axes[minor_axis] / axes[major_axis]) ** 2))
        cv2.circle(background, (int(cmx), int(cmy)), 4, (255, 255, 255), -1)
        center_p = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
        ret, centerp_binary = cv2.threshold(center_p, 0, 255, cv2.THRESH_BINARY)
        centerpoint, cpoint_h = cv2.findContours(centerp_binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        dist = []
        vhull = np.vstack(hull)
        for i, c in enumerate(vhull):
            xy = tuple(c)
            pptest = cv2.pointPolygonTest(centerpoint[0], xy, measureDist=True)
            dist.append(pptest)
        abs_dist = np.absolute(dist)
        max_i = np.argmax(abs_dist)
        caliper_max_x, caliper_max_y = list(tuple(vhull[max_i]))
        caliper_mid_x, caliper_mid_y = [int(cmx), int(cmy)]
        xdiff = float(caliper_max_x - caliper_mid_x)
        ydiff = float(caliper_max_y - caliper_mid_y)
        slope = 1
        if xdiff != 0:
            slope = (float(ydiff / xdiff))
        b_line = caliper_mid_y - (slope * caliper_mid_x)
        if slope != 0:
            xintercept = int(-b_line / slope)
            xintercept1 = int((ix - b_line) / slope)
            if 0 <= xintercept <= iy and 0 <= xintercept1 <= iy:
                cv2.line(background1, (xintercept1, ix), (xintercept, 0), (255), 3)
            elif xintercept < 0 or xintercept > iy or xintercept1 < 0 or xintercept1 > iy:
                # Used a random number generator to test if either of these cases were possible but neither is possible
                # if xintercept < 0 and 0 <= xintercept1 <= iy:
                #     yintercept = int(b_line)
                #     cv2.line(background1, (0, yintercept), (xintercept1, ix), (255), 5)
                # elif xintercept > iy and 0 <= xintercept1 <= iy:
                #     yintercept1 = int((slope * iy) + b_line)
                #     cv2.line(background1, (iy, yintercept1), (xintercept1, ix), (255), 5)
                # elif 0 <= xintercept <= iy and xintercept1 < 0:
                #     yintercept = int(b_line)
                #     cv2.line(background1, (0, yintercept), (xintercept, 0), (255), 5)
                # elif 0 <= xintercept <= iy and xintercept1 > iy:
                #     yintercept1 = int((slope * iy) + b_line)
                #     cv2.line(background1, (iy, yintercept1), (xintercept, 0), (255), 5)
                # else:
                yintercept = int(b_line)
                yintercept1 = int((slope * iy) + b_line)
                cv2.line(background1, (0, yintercept), (iy, yintercept1), (255), 5)
        else:
            cv2.line(background1, (iy, caliper_mid_y), (0, caliper_mid_y), (255), 3)
        ret1, line_binary = cv2.threshold(background1, 0, 255, cv2.THRESH_BINARY)
        # print_image(line_binary,(str(device)+'_caliperfit.png'))
        cv2.drawContours(background2, [hull], -1, (255), -1)
        ret2, hullp_binary = cv2.threshold(background2, 0, 255, cv2.THRESH_BINARY)
        # print_image(hullp_binary,(str(device)+'_hull.png'))
        caliper = cv2.multiply(line_binary, hullp_binary)
        # print_image(caliper,(str(device)+'_caliperlength.png'))
        caliper_y, caliper_x = np.array(caliper.nonzero())
        caliper_matrix = np.vstack((caliper_x, caliper_y))
        caliper_transpose = np.transpose(caliper_matrix)
        caliper_length = len(caliper_transpose)
        caliper_transpose1 = np.lexsort((caliper_y, caliper_x))
        caliper_transpose2 = [(caliper_x[i], caliper_y[i]) for i in caliper_transpose1]
        caliper_transpose = np.array(caliper_transpose2)
        ## Now we will extract the color values
        masked_spud = cv2.bitwise_and(img_write, img_write, mask=tuber_mask)
        #plt.imshow(masked_spud)
        #plt.show()
        #img_2_5_name = output_write_directory + "/2_" + str(counter) + "_" + str(plot_number) + "_" + image_name + ".jpg"
        #cv2.imwrite(img_2_5_name, cv2.cvtColor(masked_object, cv2.COLOR_RGB2BGR))
        #plot_number += 1
        bgr_object = cv2.cvtColor(masked_spud, cv2.COLOR_RGB2BGR)
        # plt.imshow(bgr_object)
        # plt.show()
        b_object, g_object, r_object = cv2.split(masked_spud)
        ## Lets take a look at the color spectrum of the objects
        ## Here we get the number of pixels that fall into each bin with the 3 color spaces
        r_hist = cv2.calcHist([r_object], [0], tuber_mask, [256], [0, 256])
        g_hist = cv2.calcHist([g_object], [0], tuber_mask, [256], [0, 256])
        b_hist = cv2.calcHist([b_object], [0], tuber_mask, [256], [0, 256])
        ## Lets get the % of total pixels that fall into each category
        r_hist_ave = (r_hist / area) * 100
        g_hist_ave = (g_hist / area) * 100
        b_hist_ave = (b_hist / area) * 100
        # plt.hist(h_potato.ravel(), 256)
        # plt.show()
        # plt.hist(s_potato.ravel(), 256)
        # plt.show()
        # plt.hist(v_potato.ravel(), 256)
        # plt.show()
        cv2.drawContours(img_out, cnt, -1, (255, 165, 0), 15)
        #cv2.line(img_out, (x, y), (x + width, y), (255, 0, 0), 3)
        #cv2.line(img_out, (int(cmx), y), (int(cmx), y + height), (100, 255, 0), 3)
        cv2.circle(img_out, (int(cmx), int(cmy)), 10, (255, 0, 0), 10)
        cv2.line(img_out, (tuple(caliper_transpose[caliper_length - 1])), (tuple(caliper_transpose[0])), (255, 0, 0), 10)
        #plt.imshow(img_out)
        #plt.show()
        #img_2_6_name = output_write_directory + "/2_" + str(counter) + "_" + str(plot_number) + "_" + image_name + ".jpg"
        #plot_number += 1
        r_hist = r_hist_ave.transpose()
        r_row = pd.DataFrame(r_hist, columns=r_names)
        g_hist = g_hist_ave.transpose()
        g_row = pd.DataFrame(g_hist, columns=g_names)
        b_hist = b_hist_ave.transpose()
        b_row = pd.DataFrame(b_hist, columns=b_names)
        r_table = r_table.append(r_row, )
        g_table = g_table.append(g_row, )
        b_table = b_table.append(b_row, )
        shape_values = get_A08241_shape(cnt, tuber, tuber_mask, image_name)
        s_row = pd.DataFrame(shape_values.reshape(1,200), columns=s_names)
        s_table = s_table.append(s_row, )
        ratio = major_axis_length / minor_axis_length
        obj_color_ave = cv2.mean(img_write, mask=tuber_mask)
        # print(obj_color_ave)
        r_ave = obj_color_ave[0]
        g_ave = obj_color_ave[1]
        b_ave = obj_color_ave[2]
        tuber = tuber_no[counter]
        temp = [img_name, clone, rep, side, light, tuber, cmx, cmy, area, perimeter, major_axis_length, minor_axis_length, ratio, eccentricity,r_ave, g_ave, b_ave]
        temp = pd.DataFrame([temp], columns=['img_name', 'clone', 'rep', 'side', 'light', 'tuber','cmx', 'cmy', 'area', 'perimeter', 'length', 'width', 'ratio', 'eccentricity', 'red_ave', 'green_ave', 'blue_ave'])
        #print(temp)
        summary_table = summary_table.append(temp, )
        counter += 1
        #print(counter)
    cv2.imwrite(output_file_name, cv2.cvtColor(img_out, cv2.COLOR_RGB2BGR))
    return summary_table, r_table, g_table, b_table, s_table
    #return summary_table, r_table, g_table, b_table

def get_A08241_shape(cnt, tuber_no, img_mask, img_name):
    ## Note this will be different on your computer
    #output_dir = '/Users/max.feldman/Documents/data/2020/A08241_imgs/std/output/shapes/'
    clone, rep, side, light = image_name.split("_")
    output_file_name = output_dir + "shape_" + img_name + "_" + str(tuber_no) + ".jpg"
    #x_names = ["x_" + str(x) for x in list(range(1, 101))]
    #y_names = ["y_" + str(y) for y in list(range(1, 101))]
    #c_names = x_names + y_names
    ## Get rotational degrees to make tuber vertical then rotate
    rotation_deg = cv2.fitEllipse(cnt)[2]
    rotated_img = scipy.ndimage.rotate(img_mask, rotation_deg, reshape=True)
    ## Get contours of rotated tuber and plot
    v_contours, v_hierarchy = cv2.findContours(rotated_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    ix, iy = np.shape(rotated_img)
    blank_image = np.zeros((ix, iy, 3), np.uint8)
    v_tuber_bin = cv2.drawContours(blank_image, [max(v_contours, key=cv2.contourArea)], -1, (255, 255, 255), thickness=cv2.FILLED)
    ## Fit bounding rectangle to tuber and crop
    x, y, w, h = cv2.boundingRect(max(v_contours, key=cv2.contourArea))
    # cv2.rectangle(v_tuber_bin,(x,y),(x+w,y+h),(0,255,0),2)
    cropped_tuber = v_tuber_bin[y:y + h, x:x + w]
    ## Convert to grayscalex
    cropped_tuber_g = cv2.cvtColor(cropped_tuber, cv2.COLOR_BGR2GRAY)
    ## Lets make the image a square to maintain aspect ratio
    pad_needed = h - w
    if (pad_needed % 2) == 0:
        pad_val_l = pad_needed / 2
        pad_val_r = pad_val_l
    else:
        pad_val_l = int(pad_needed / 2)
        pad_val_r = pad_val_l + 1
    cropped_tuber_g = np.pad(cropped_tuber_g, [(0, 0), (int(pad_val_r), int(pad_val_l))], 'constant', constant_values=(0))
    ## Normalize for axis ratio by resizing to 100 x 100 image
    scaled_tuber = cv2.resize(cropped_tuber_g, (100, 100))
    ## Convert to true binary (0 or 1)
    scaled_tuber[scaled_tuber > 0] = 1
    ## Get row and column wise sums (aka sweeps)
    tuber_x = scaled_tuber.sum(axis=1)
    tuber_y = scaled_tuber.sum(axis=0)
    s_contours, s_hierarchy = cv2.findContours(scaled_tuber, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    x, y, width, height = cv2.boundingRect([max(s_contours, key=cv2.contourArea)][0])
    #x, y, width, height = cv2.boundingRect(s_contours)
    tuber_x = tuber_x/width
    tuber_y = tuber_y/height
    shape_values = np.concatenate([tuber_x, tuber_y])
    ix, iy = np.shape(scaled_tuber)
    blank_scaled_image = np.zeros((ix, iy, 3), np.uint8)
    cv2.drawContours(blank_scaled_image, [max(s_contours, key=cv2.contourArea)], -1, (255, 255, 255), thickness=cv2.FILLED)
    cv2.drawContours(blank_scaled_image, [max(s_contours, key=cv2.contourArea)], -1, (0, 255, 0), thickness=2)
    cv2.imwrite(output_file_name, cv2.cvtColor(blank_scaled_image, cv2.COLOR_RGB2BGR))
    return(shape_values)

