import einops
import numpy as np
import torch


class Blocks:
    def __init__(self, height, width, block_size=(500, 500)):
        self.height = height
        self.width = width
        self.block_size = block_size

        # 计算需要切分的块的索引
        block_indexes = []
        for ih in range(0, height, block_size[0]):
            for iw in range(0, width, block_size[1]):
                ih_end = min(ih + block_size[0], height)
                iw_end = min(iw + block_size[1], width)
                block_indexes.append(((ih, ih_end), (iw, iw_end)))
        self.block_indexes = block_indexes

    def split_image(self, src_img, expand_size=(12, 12)):
        top, bottom = expand_size[0] // 2, expand_size[0] - expand_size[0] // 2 - 1
        left, right = expand_size[1] // 2, expand_size[1] - expand_size[1] // 2 - 1
        src_img_expanded = np.pad(
            src_img,
            ((0, 0), (top, bottom), (left, right)),
            "constant",
            constant_values=(0, 0),
        )

        blocks = []
        for (ih, ih_end), (iw, iw_end) in self.block_indexes:
            block = src_img_expanded[
                :, ih : ih_end + bottom + top, iw : iw_end + right + left
            ]
            blocks.append(block)
        return blocks

    def unfold_block(self, block, kernel_size, dilation=1, padding=0, stride=1):
        c, h, w = block.shape
        h_out, w_out = h - kernel_size + 1, w - kernel_size + 1
        b = h_out * w_out
        c = c

        dst_data = np.zeros((b, c, kernel_size, kernel_size), dtype=np.float32)
        for i in range(h_out):
            for j in range(w_out):
                dst_data[i * w_out + j] = block[
                    :, i : i + kernel_size, j : j + kernel_size
                ]
        return dst_data

    def fold_block(self, src_data, height, width, stride=1):
        b, c, h_kernel, w_kernel = src_data.shape
        data_value = np.zeros((c, height, width), dtype=np.float32)
        data_count = np.zeros((c, height, width), dtype=np.int16)

        if stride == 1 and h_kernel == 1 and w_kernel == 1:
            assert b == height * width, "合并块的尺寸不匹配"
            src_data = src_data.reshape(b, c)
            data_value = torch.nn.Fold(output_size=(height, width), kernel_size=(1, 1))(
                torch.Tensor(einops.rearrange(src_data, "b c  -> c b"))
            ).numpy()
        else:
            # for i in range(b):
            #     h, w = i // width, i % width
            #     data_value[:, h, w] = src_data[i, :, :, :]
            #     data_count[:, h, w] += 1
            raise NotImplementedError("stride != 1 or h_kernel != 1 or w_kernel != 1")
        data_count[data_count == 0] = 1
        block = data_value / data_count
        return block

    def merge_image(self, blocks, default_value=0):
        c, h, w = blocks[0].shape
        image = np.full((c, self.height, self.width), default_value, dtype=np.float32)

        for i, ((ih, ih_end), (iw, iw_end)) in enumerate(self.block_indexes):
            image[:, ih:ih_end, iw:iw_end] = blocks[i]
        return image


# 示例使用
if __name__ == "__main__":
    import time

    t_start = time.time()
    kernel_size = 3
    height, width = 5, 10
    block_size = (5, 5)
    arr = np.arange(height * width).reshape(1, height, width)
    print("原始数组:\n", arr)
    splitter = Blocks(height, width, block_size)
    blocks = splitter.split_image(arr, (kernel_size, kernel_size))
    print("切分后的块:\n", blocks)

    processed_blocks = []
    for block in blocks:
        _h, _w = block.shape[1:]
        data = splitter.unfold_block(block, kernel_size)
        print("cost time: unfold", time.time() - t_start)
        data_new = data[
            :,
            :,
            kernel_size // 2 : kernel_size // 2 + 1,
            kernel_size // 2 : kernel_size // 2 + 1,
        ]
        data_new = splitter.fold_block(
            data_new, _h - kernel_size + 1, _w - kernel_size + 1
        )
        print("cost time:   fold", time.time() - t_start)
        processed_blocks.append(data_new)

    merged_image = splitter.merge_image(processed_blocks)
    print("合并后的图像:\n", merged_image)
