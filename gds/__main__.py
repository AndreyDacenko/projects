import gdspy
import numpy as np
import cv2
import math

gdspy.current_library = gdspy.GdsLibrary()
gdsii = gdspy.GdsLibrary(infile='MLDR13_REV2_V2-металл1,отверстияиВИА.gds')
gdspy.current_library.read_gds('MLDR13_REV2_V2-металл1,отверстияиВИА.gds')
image_ratio = 8
image = []

information = open('info.txt', 'w')


# points_without_angle = open('no_angle.txt', 'a')

# -------- the necessary figure -----------

def current_reference_name():
    the_biggest_reference_name = None
    the_biggest_reference = 0
    for cell in gdsii.cell_dict.values():
        if len(cell.references) > the_biggest_reference:
            the_biggest_reference = len(cell.references)
            # the_biggest_reference_name = cell.name
            the_biggest_reference_name = 'MLDR13_REV2_V2'
    return the_biggest_reference_name


#  --------------- image size -----------

def image_size(current_name):
    origin_array_X = np.array([])
    origin_array_Y = np.array([])
    for cell in gdsii.cell_dict.values():
        if cell.name == current_name:
            for ref in cell.references:
                max_origin_value = ref.origin
                origin_array_X = np.append(origin_array_X, max_origin_value[0])
                origin_array_Y = np.append(origin_array_Y, max_origin_value[1])
    image_size_X = max(origin_array_X) + abs(min(origin_array_X))
    image_size_Y = max(origin_array_Y) + abs(min(origin_array_Y))
    max_value_of_XY = int(max(image_size_X, image_size_Y))
    return max_value_of_XY


#  -------------- draw image -------------

def draw_reference_polygons(reference_path, last_angle, reflecting, origin_x, origin_y,
                    center_x, center_y):
    def rotate_polygon_point(radians, px, py, ox, oy, _result_points):
        p0 = ox + math.cos(radians) * (px - ox) - math.sin(radians) * (py - oy)
        p1 = oy + math.sin(radians) * (px - ox) + math.cos(radians) * (py - oy)
        polygon_points = np.array([p0, p1])
        _result_points = np.append(final_polygon, np.array([polygon_points, ]), axis=0)
        return _result_points

    def rotate_reflected_polygon_point(radians, px, py, ox, oy, _result_points):
        p0 = ox + math.cos(radians) * (px - ox) - math.sin(radians) * (py - oy)
        p1 = oy + math.sin(radians) * (px - ox) + math.cos(radians) * (py - oy)
        polygon_points = np.array([p0, p1])
        _result_points = np.append(final_polygon_reflected, np.array([polygon_points, ]), axis=0)
        return _result_points

    if len(reference_path.ref_cell.polygons) != 0:

        for polygon in reference_path.ref_cell.polygons:
            new_polygon = polygon.polygons[0].copy()
            final_polygon = np.empty([0, 2], dtype=int)
            final_polygon_reflected = np.empty([0, 2], dtype=int)

            for point in new_polygon:
                point[0] += origin_x
                point[1] += origin_y

            information.write(f'Original points: {new_polygon} \n')
            information.write(f'Next Rotation: {last_angle} \n')
            if reflecting:
                # print(new_polygon)
                for point in new_polygon:
                    point[1] = point[1] + 2 * (origin_y - point[1])
                    if last_angle != 0:
                        final_polygon_reflected = rotate_reflected_polygon_point(last_angle, point[0], point[1],
                                                                                 origin_x, origin_y,
                                                                                 final_polygon_reflected)
                    else:
                        final_polygon_reflected = new_polygon
                information.write(f'Reflected points: {final_polygon_reflected} \n')
                final_polygon_reflected = np.int32(final_polygon_reflected * image_ratio + size * image_ratio / 2)
                cv2.polylines(image, [final_polygon_reflected], True, (255, 255, 255))
            else:
                for point in new_polygon:
                    if last_angle != 0:
                        final_polygon = rotate_polygon_point(last_angle, point[0], point[1], origin_x, origin_y,
                                                             final_polygon)
                    else:
                        final_polygon = new_polygon
                information.write(f'Don`t reflected points: {final_polygon} \n')
                final_polygon = np.int32(final_polygon * image_ratio + size * image_ratio / 2)
                cv2.polylines(image, [final_polygon], True, (255, 255, 255))

    # --------------- recursion ------------

    if len(reference_path.ref_cell.references) != 0:
        for next_reference in reference_path.ref_cell.references:

            next_origin_x = origin_x + next_reference.origin[0]
            next_origin_y = origin_y + next_reference.origin[1]

            new_center_x = center_x + next_reference.origin[0]
            new_center_y = center_y + next_reference.origin[1]

            if next_reference.x_reflection == True:
                reflect = True
            else:
                reflect = False or reflecting

            if next_reference.rotation is not None:
                next_angle = math.radians(next_reference.rotation) + last_angle
            else:
                next_angle = last_angle
            # information.write(f'\nName: {next_reference.ref_cell.name} \n')
            # information.write(f'Parent: {reference_path.ref_cell.name}\n')
            # information.write(f'Reflection: {next_reference.x_reflection} \n')
            # information.write(f'Rotation: {next_reference.rotation} \n')
            # information.write(f'Center(origin): {next_origin_x}, {next_origin_y} \n')
            # information.write(f'Rotation: {next_reference.rotation} \n')
            # information.write(f'Angle: {next_angle} \n')

            draw_reference_polygons(next_reference, next_angle, reflect, next_origin_x,
                            next_origin_y, new_center_x, new_center_y)




# def draw_reference_lines(reference_path, last_angle, reflecting, origin_x, origin_y,
#                     center_x, center_y):
#     def rotate_path_point(radians, px, py, ox, oy, _result_points):
#         p0 = ox + math.cos(radians) * (px - ox) - math.sin(radians) * (py - oy)
#         p1 = oy + math.sin(radians) * (px - ox) + math.cos(radians) * (py - oy)
#         path_points = np.array([p0, p1])
#         _result_points = np.append(final_path, np.array([path_points, ]), axis=0)
#         return _result_points
#
#     def rotate_reflected_path_point(radians, px, py, ox, oy, _result_points):
#         p0 = ox + math.cos(radians) * (px - ox) - math.sin(radians) * (py - oy)
#         p1 = oy + math.sin(radians) * (px - ox) + math.cos(radians) * (py - oy)
#         path_points = np.array([p0, p1])
#         _result_points = np.append(final_path_reflected, np.array([path_points, ]), axis=0)
#         return _result_points
#
#     if len(reference_path.ref_cell.paths) != 0:
#         for path in reference_path.ref_cell.paths:
#             new_path = path.points.copy()
#             final_path = np.empty([0, 2], dtype=int)
#             final_path_reflected = np.empty([0, 2], dtype=int)
#
#             for point in new_path:
#                 point[0] += origin_x
#                 point[1] += origin_y
#
#             if reflecting:
#                 for point in new_path:
#                     point[1] = point[1] + 2 * (center_y - point[1])
#
#                     if last_angle != 0:
#                         final_path_reflected = rotate_reflected_path_point(last_angle, point[0], point[1],
#                                                                                  center_x, center_y,
#                                                                                  final_path_reflected)
#                     else:
#                         final_path_reflected = new_path
#                 final_path_reflected = np.int32(final_path_reflected * image_ratio + size * image_ratio / 2)
#                 cv2.polylines(image, [final_path_reflected], False, (255, 255, 255))
#             else:
#                 for point in new_path:
#                     if last_angle != 0:
#                         final_path = rotate_path_point(last_angle, point[0], point[1], center_x, center_y,
#                                                              final_path)
#                     else:
#                         final_path = new_path
#                 final_path = np.int32(final_path * image_ratio + size * image_ratio / 2)
#                 cv2.polylines(image, [final_path], False, (255, 255, 255))
#
#     # --------------- recursion ------------
#
#     if len(reference_path.ref_cell.references) != 0:
#         for next_reference in reference_path.ref_cell.references:
#             next_origin_x = origin_x + next_reference.origin[0]
#             next_origin_y = origin_y + next_reference.origin[1]
#             next_angle = last_angle
#
#             draw_reference_polygons(next_reference, next_angle, reflecting, next_origin_x,
#                             next_origin_y, center_x, center_y)


if __name__ == "__main__":
    cell_name = current_reference_name()
    size = image_size(cell_name)
    image = np.zeros((size * image_ratio * 2, size * image_ratio * 2))
    information.write(f'Image size:  {size * image_ratio * 2} X {size * image_ratio * 2} \n')

    for cell in gdsii.cell_dict.values():
        if cell.name == cell_name:
            reflect_around_point = 0
            def draw_polygons():
                if len(cell.polygons) != 0:
                    for polygon in cell.polygons:
                        new_polygon = polygon.polygons[0].copy()
                        new_polygon = np.int32(new_polygon * image_ratio + size * image_ratio / 2)
                        cv2.polylines(image, [new_polygon], True, (255, 255, 255))
            def draw_paths():
                if len(cell.paths) != 0:
                    for path in cell.paths:
                        new_path = path.points.copy()
                        new_path = np.int32(new_path * image_ratio + size * image_ratio / 2)
                        cv2.polylines(image, [new_path], False, (255, 255, 255))

            draw_polygons()
            draw_paths()

            for reference in cell.references:
                # information.write(f'\nName: {reference.ref_cell.name} \n')
                # information.write(f'Angle: {reference.rotation} \n')
                # information.write(f'Reflection: {reference.x_reflection} \n')
                # information.write(f'Rotation: {reference.rotation} \n')
                # ------------ reflection ----------
                reflect = False
                if reference.x_reflection:
                    reflect = True
                    reflect_around_point = reference.origin[1]

                if reference.rotation is not None:
                    angle = math.radians(reference.rotation)
                else:
                    angle = 0
                origin_x = centerX = reference.origin[0]
                origin_y = centerY = reference.origin[1]
                information.write(f'Center(origin): {centerX}, {centerY} \n')
                draw_reference_polygons(reference, angle, reflect, origin_x, origin_y, centerX, centerY)
                # draw_reference_lines(reference, angle, reflect, origin_x, origin_y, centerX, centerY)

    flip_image = cv2.flip(image, 0)
    cv2.imwrite('image.jpg', flip_image)
    information.close()
    print('Done')


