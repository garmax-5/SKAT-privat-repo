import folium
from geopy.distance import geodesic
import socket
import ast
import json

def reading_JSON():
    # Открываем файл JSON для чтения
    with open('Test.json', 'r', encoding="utf8") as file:
        # Загружаем данные из файла
        data = json.load(file)
    return (data["coordinates"])



def Reading_coordinates():

    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 9080  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                return (ast.literal_eval(data.decode('utf-8')))
                # conn.sendall(data)

def map_display(path_coords,plane_coords):
    DISTANCE_OF_OFFROAD = 1

    def Critical_distance():
        # Хз что тут писать
        print("Критическое отклонение от маршрута!!!")

    def proj(x1, y1, x2, y2, x3, y3):
        k = ((y2 - y1) * (x3 - x1) - (x2 - x1) * (y3 - y1)) / ((y2 - y1) ** 2 + (x2 - x1) ** 2)
        x4 = x3 - k * (y2 - y1)
        y4 = y3 + k * (x2 - x1)
        return x4, y4

    # Поиск кратчайшего расстояния от точки до отрезка
    def shortest_distance(point, line_start, line_end):
        line_vector = (line_end[0] - line_start[0], line_end[1] - line_start[1])
        point_vector = (point[0] - line_start[0], point[1] - line_start[1])
        length = geodesic(line_start, line_end).meters
        dot_product = point_vector[0] * line_vector[0] + point_vector[1] * line_vector[1]
        t = dot_product / (length ** 2)
        t = max(0, min(1, t))
        nearest_point = (line_start[0] + t * line_vector[0], line_start[1] + t * line_vector[1])
        distance = geodesic(point, nearest_point).meters
        return distance

    # # Загрузка координат пути из файла или интернета
    # path_coords = [
    #     (54.6123, 39.7245),
    #     (54.6131, 39.7260),
    #     (54.6144, 39.7258)
    # ]

    # Создание объекта карты
    m = folium.Map(location=[path_coords[0][0], path_coords[0][1]], zoom_start=17)

    # Добавление карточки
    tooltip = 'Нажмите, чтобы узнать больше'
    folium.Marker([path_coords[0][0], path_coords[0][1]], popup='<b>Старт</b>', tooltip=tooltip).add_to(m)
    # Отображение карты
    m.save('map.html')

    # Добавление точек на карту
    for i, coord in enumerate(path_coords):
        folium.CircleMarker(coord, radius=5, color='blue', fill=True, fill_color='blue').add_to(m)
        folium.Marker(coord, icon=folium.DivIcon(html=f'<div style="font-size: 10pt;">{i + 1}</div>')).add_to(m)
    # Соединение точек отрезками
    for i in range(len(path_coords) - 1):
        folium.PolyLine([path_coords[i], path_coords[i + 1]], color='blue').add_to(m)

    # # Загрузка текущих координат самолета из файла или интернета
    # plane_coords = (54.6135, 39.7266)

    # Добавление маркера самолета на карту
    folium.Marker(plane_coords, icon=folium.Icon(color='red', icon='plane')).add_to(m)

    # Определение отрезка с наименьшим расстоянием
    min_distance = float('inf')
    nearest_segment = None
    for i in range(len(path_coords) - 1):
        distance = shortest_distance(plane_coords, path_coords[i], path_coords[i + 1])
        if distance < min_distance:
            min_distance = distance
            nearest_segment = (path_coords[i], path_coords[i + 1])

    # Проверка критического расстояния
    if min_distance > DISTANCE_OF_OFFROAD:
        Critical_distance()

    # Добавление отрезка на карту
    # coordinate = ((nearest_segment[1][0] + nearest_segment[0][0])/2, (nearest_segment[1][1] + nearest_segment[0][1])/2)
    coordinate = proj(nearest_segment[1][0], nearest_segment[1][1], nearest_segment[0][0], nearest_segment[0][1],
                      plane_coords[0], plane_coords[1])
    folium.PolyLine([plane_coords, coordinate], color='green').add_to(m)

    m.save('map.html')


if __name__ == "__main__":
    plane_coords = Reading_coordinates()
    path_coords = reading_JSON()
    # plane_coords = (54.6135, 39.7266)
    map_display(path_coords, plane_coords)


