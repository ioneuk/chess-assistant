import cv2
from stockfish import Stockfish

from chessboard_detection import get_cells, get_fen, get_position, draw_polygon
from detect import detection_and_classification, model


def get_board_name(figure_name: str):
    if figure_name == "bishop":
        return "b"

    color, fig = figure_name.split("-")
    if fig == "knight":
        fig = "n"
    else:
        fig = fig[0]
    if color[0] == "w":
        fig = fig.upper()
    return fig


def photo_to_fen(file_path):
    y_offset = 5

    detection = detection_and_classification(file_path)
    cells = get_cells(file_path, show=True
                      )
    positions = []
    for piece in detection:
        clazz = model.names[int(piece[2])]
        clazz_name = get_board_name(clazz)

        x1, y1, x2, y2 = piece[0]
        x1 = x1.item()
        y1 = y1.item()
        x2 = x2.item()
        y2 = y2.item()

        min_x = min(x1, x2)
        max_x = max(x1, x2)
        max_y = max(y1, y2)
        mid_x = (min_x + max_x) / 2

        x = mid_x
        y = int(max_y - y_offset)

        hor, ver = get_position(x, y, cells)
        if hor != -1:
            positions.append((clazz_name, hor, ver))
        # else:
        #     image = cv2.imread(file_path)
        #     cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), 2)
        #     image = cv2.circle(image, (int(x), int(y)), radius=0, color=(0, 0, 255), thickness=10)
        #     # image = draw_polygon(image, cells[4][7])
        #     cv2.imshow("Test1", image)
        #     cv2.waitKey(0)
    # print(positions)
    return get_fen(positions)

# fen = photo_to_fen("./data/board3.jpg")
#
# stockfish = Stockfish("../stockfish/stockfish_13_win_x64_bmi2.exe")
# stockfish.set_fen_position(fen)
# print(stockfish.get_board_visual())
