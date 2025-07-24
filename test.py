from PIL import Image
import numpy as np
from scipy.spatial import cKDTree

def pixelate_image(input_image_path, output_image_path, size, rounder=50):
    # 이미지 열기
    img_np = image_preprocesser(input_image_path,size)
    
    height, width = img_np.shape[:2]
    grid_size = height//size
    pixelated_img=Image.new(mode="RGBA", size=(size,size))
    pixelated_img_np = np.zeros_like(pixelated_img)


    # 격자별 평균 색 계산 및 적용
    for y in range(0, height, grid_size):
        for x in range(0, width, grid_size):
            y_end = min(y + grid_size, height)
            x_end = min(x + grid_size, width)
            grid_pixels = img_np[y:y_end, x:x_end]

            condition = (grid_pixels[:,:,3]==0)
            targets = np.any(condition,axis=0)
            target_index = np.where(targets)[0]
            filtered = np.delete(grid_pixels,target_index,axis=1)

            if filtered.size==0:
                pixelated_img_np[y//grid_size, x//grid_size] = [0,0,0,0]
            else:
                avg_color = filtered.mean(axis=(0,1), dtype=int)
                quantized = rounder*np.round(avg_color//rounder).astype(int)
                quantized[3]=255
                pixelated_img_np[y//grid_size, x//grid_size] = quantized

    pixelated_img_np=palette_painter(pixelated_img_np,"palette.png")

    pixelated_img = Image.fromarray(pixelated_img_np)
    pixelated_img.save(output_image_path)

def image_preprocesser(input_image_path, grid_size):
    img = Image.open(input_image_path)
    img_np = np.array(img)

    height,width = img_np.shape[0:2]
    min_size = min(height,width)//grid_size*grid_size

    x_start = width//2 - min_size//2
    y_start = height//2 - min_size//2

    return img_np[y_start:y_start+min_size,x_start:x_start+min_size]

def load_palette(inputPath):
    paletteImage = Image.open(inputPath).convert('RGBA')
    palette = np.array(paletteImage)

    y, x = palette.shape[:2]

    palette=palette.reshape(y*x,4)


    filtered = np.unique(palette,axis=0)
    return filtered

def palette_painter(pixelated_img_np, palette_path):
    palette = load_palette(palette_path)


    flatImage = pixelated_img_np.reshape(-1,4)

    tree = cKDTree(palette)
    _, idx = tree.query(flatImage)

    recoloredFlat = palette[idx]

    recoloredImage = recoloredFlat.reshape(pixelated_img_np.shape).astype(np.uint8)

    return recoloredImage


# 사용 예시
pixelate_image("input.png", "first_output.png", size=4,rounder=100)