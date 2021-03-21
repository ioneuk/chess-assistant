import torch

from models.experimental import attempt_load
from utils.datasets import LoadImages
from utils.general import non_max_suppression, scale_coords
from utils.torch_utils import select_device

MODEL_PATH = '/Users/ioneuk/Documents/machine-learning/hackathon-game-assistant/chess-assistant/best.pt'
device = select_device('')
model = attempt_load(MODEL_PATH, map_location=device)
names = model.names



def detection_and_classification(img_path):
    dataset = LoadImages(img_path, img_size=416)
    results = []
    for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to
        if img.ndimension() == 3:
            img = img.unsqueeze(0)
        pred = model(img, augment=False)[0]
        pred = non_max_suppression(pred, 0.4, 0.45, classes=None, agnostic=False)

        for i, det in enumerate(pred):  # detections per image
            p, s, im0,  = img_path, '', im0s
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for c in det[:, -1].unique():
                    n = (det[:, -1] == c).sum()  # detections per class
                    target_class = names[int(c)]

                # Write results

                for *xyxy, conf, cls in reversed(det):
                    results.append((xyxy, conf, cls))
        break
    return results


if __name__ == "__main__":
    res = detection_and_classification(
        '/Users/ioneuk/Downloads/ChessPieces/test/0b47311f426ff926578c9d738d683e76_jpg.rf.40183eae584a653181bbd795ba3c353f.jpg')
    print(res)
