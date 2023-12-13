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

    def split_image(self, src_img, kernel_size=(12, 12)):
        top, bottom = kernel_size[0] // 2, kernel_size[0] - kernel_size[0] // 2 - 1
        left, right = kernel_size[1] // 2, kernel_size[1] - kernel_size[1] // 2 - 1
        src_img_expanded = np.pad(
            src_img,
            ((0, 0), (top, bottom), (left, right)),
            "constant",
            constant_values=(0, 0),
        )

        blocks = []
        for (ih, ih_end), (iw, iw_end) in self.block_indexes:
            block = src_img_expanded[:, ih : ih_end + bottom + top, iw : iw_end + right + left]
            blocks.append(block)
        return blocks

    def unfold_block(
        self, block: np.ndarray, kernel_size: int, dilation=1, padding=0, stride=1, method="torch"
    ) -> np.ndarray:
        # check input
        assert isinstance(block, np.ndarray), "block必须是numpy数组"

        # 处理输入的block的参数
        c_block, h_block, w_block = block.shape
        h_dst, w_dst = h_block - kernel_size + 1, w_block - kernel_size + 1
        b_out = h_dst * w_dst
        c_out = c_block
        h_out = kernel_size
        w_out = kernel_size

        if method == "torch":  # 调用torch的unfold函数，然后再转换为numpy数组，这种方式非常快
            cls_torch_unfold = torch.nn.Unfold(
                kernel_size=(h_out, w_out),
                dilation=dilation,
                padding=padding,
                stride=stride,
            )
            _dst_data = cls_torch_unfold(torch.Tensor(block)).numpy()  # 输出的数组维度为(c * h * w, b)
            # 将torch输出的数组转变维度，变为(b, c, h, w)
            dst_data = einops.rearrange(_dst_data, "(c h w) b -> b c h w", h=h_out, w=w_out)
            return dst_data
        else:  # 逐个提取，这种方式没有用到多核并行处理，非常慢
            dst_data = np.zeros((b_out, c_out, kernel_size, kernel_size), dtype=block.dtype)
            for i in range(h_dst):
                for j in range(w_dst):
                    dst_data[i * w_dst + j] = block[:, i : i + kernel_size, j : j + kernel_size]
            return dst_data

    def fold_block(self, src_data, height, width, stride=1):
        b, c, h_kernel, w_kernel = src_data.shape
        data_value = np.zeros((c, height, width), dtype=np.float32)
        data_count = np.zeros((c, height, width), dtype=np.int16)

        if stride == 1 and h_kernel == 1 and w_kernel == 1:
            assert b == height * width, "合并块的尺寸不匹配"
            src_data = src_data.reshape(b, c)
            cls_torch_fold = torch.nn.Fold(output_size=(height, width), kernel_size=(h_kernel, w_kernel))
            data_value = cls_torch_fold(torch.Tensor(einops.rearrange(src_data, "b c  -> c b"))).numpy()
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
    height, width = 10, 10
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
        data_new = data[:, :, kernel_size // 2 : kernel_size // 2 + 1, kernel_size // 2 : kernel_size // 2 + 1]
        data_new = splitter.fold_block(data_new, _h - kernel_size + 1, _w - kernel_size + 1)
        print("cost time:   fold", time.time() - t_start)
        processed_blocks.append(data_new)

    merged_image = splitter.merge_image(processed_blocks)
    print("合并后的图像:\n", merged_image)
