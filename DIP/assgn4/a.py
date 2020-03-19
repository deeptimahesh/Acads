hit_matrix1 = np.array([[0, 0, 0],[0, 1, 0],[1, 1, 1]])
hit_matrix2 = np.array([[0, 0, 0],[1, 1, 0],[0, 1, 0]])
miss = np.array([[1, 1, 1],[0, 0, 0],[0, 0, 0]])
s2_miss = np.array([[0, 1, 1],[0, 0, 1],[0, 0, 0]])

def skeleton_pass(img, s1_hit, s1_miss, s2_hit, s2_miss):
    img = img ^ binary_hit_or_miss(img, s1_hit, s1_miss)
    img = img ^ binary_hit_or_miss(img, s2_hit, s2_miss)
    img = img ^ binary_hit_or_miss(img, np.rot90(s1_hit, 1), np.rot90(s1_miss, 1))
    img = img ^ binary_hit_or_miss(img, np.rot90(s2_hit, 1), np.rot90(s2_miss, 1))
    img = img ^ binary_hit_or_miss(img, np.rot90(s1_hit, 2), np.rot90(s1_miss, 2))
    img = img ^ binary_hit_or_miss(img, np.rot90(s2_hit, 2), np.rot90(s2_miss, 2))
    img = img ^ binary_hit_or_miss(img, np.rot90(s1_hit, 3), np.rot90(s1_miss, 3))
    img = img ^ binary_hit_or_miss(img, np.rot90(s2_hit, 3), np.rot90(s2_miss, 3))
    return img

def skeletonize(img):
    temp1 = img
    i = 0
    while i < 100:
        i += 1
        print("Loop " + str(i))
        temp2 = skeleton_pass(temp1, s1_hit, s1_miss, s2_hit, s2_miss)
        if np.array_equal(temp1, temp2):
            break
        temp1 = np.copy(temp2)
    return temp1

plt.figure(figsize=(8,8))
plt.imshow(np.invert(skeletonize(finger)), cmap="gray")