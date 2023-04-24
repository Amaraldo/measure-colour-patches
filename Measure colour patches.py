import pygame
import numpy as np
import cv2
import csv

# Global variables
rows = 4
columns = 6
point_size = 10
image_path = "/path/to/image.jpg"
csv_path = "/path/to/rgb_values_of_colour_patches.csv"

def create_mesh(image, rows, columns):
    height, width, _ = image.shape
    x_coords = np.linspace(0, width, columns + 2, dtype=int)[1:-1]
    y_coords = np.linspace(0, height, rows + 2, dtype=int)[1:-1]
    mesh = [(x, y) for y in y_coords for x in x_coords]
    return mesh

def update_mesh(mesh, current_point, new_pos):
    if current_point in (0, columns - 1, len(mesh) - columns, len(mesh) - 1):
        old_corner_pos = mesh[current_point]
        mesh[current_point] = new_pos

        for i, point in enumerate(mesh):
            if i not in (0, columns - 1, len(mesh) - columns, len(mesh) - 1):
                row, col = divmod(i, columns)
                
                t = col / (columns - 1) if columns > 1 else 0
                u = row / (rows - 1) if rows > 1 else 0

                a = np.array(mesh[0])
                b = np.array(mesh[columns - 1])
                c = np.array(mesh[len(mesh) - columns])
                d = np.array(mesh[len(mesh) - 1])

                new_point = (1 - t) * (1 - u) * a + t * (1 - u) * b + t * u * d + (1 - t) * u * c

                mesh[i] = tuple(new_point)
    else:
        mesh[current_point] = new_pos

    return mesh

def draw(screen, image, mesh):

    screen.fill((0, 0, 0))
    image_surface = pygame.surfarray.make_surface(image.swapaxes(0, 1))
    screen.blit(image_surface, (0, 0))

    for point in mesh:
        pygame.draw.rect(screen, (0, 255, 0), (int(point[0]) - point_size, int(point[1]) - point_size, 2 * point_size, 2 * point_size), 1)

    pygame.display.flip()

def average_rgb_within_points(mesh, image, point_size):
    averaged_rgb = []

    for point in mesh:
        x, y = map(int, point)

        x_start, y_start = x - point_size, y - point_size
        x_end, y_end = x + point_size, y + point_size

        region = image[y_start:y_end, x_start:x_end]
        avg_color = np.mean(region, axis=(0, 1))

        averaged_rgb.append(avg_color)

    return np.array(averaged_rgb)

def write_rgb_to_csv(averaged_rgb, filename):
    with open(filename, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        for point_rgb in averaged_rgb:
            normalized_rgb = [round(val / 255, 8) for val in point_rgb]
            csvwriter.writerow(normalized_rgb)
    print("Finished writing to CSV file")

def get_clicked_point(mouse_pos, mesh):
    for i, point in enumerate(mesh):
        x, y = point
        if (mouse_pos[0] > x - point_size) and (mouse_pos[0] < x + point_size) and (mouse_pos[1] > y - point_size) and (mouse_pos[1] < y + point_size):
            return i
    return None

def main():
    global rows, columns, point_size, image_path, csv_path

    max_size = (1500, 800)
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    height, width, _ = image.shape
    aspect_ratio = float(width) / float(height)
    new_width = max_size[0]
    new_height = int(new_width / aspect_ratio)

    if new_height > max_size[1]:
        new_height = max_size[1]
        new_width = int(new_height * aspect_ratio)

    new_size = (new_width, new_height)

    image = cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)
    mesh = create_mesh(image, rows, columns)

    height, width, _ = image.shape

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Measure colour values')

    running = True
    mouse_down = False
    current_point = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    current_point = get_clicked_point(event.pos, mesh)

            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_down = False
                    current_point = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    averaged_rgb = average_rgb_within_points(mesh, image, point_size)
                    write_rgb_to_csv(averaged_rgb, csv_path)

        if mouse_down and current_point is not None:
            mouse_pos = pygame.mouse.get_pos()
            mesh = update_mesh(mesh, current_point, mouse_pos)

        draw(screen, image, mesh)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
