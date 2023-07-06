import numpy as np
import random


class ImageEncoderDecoder:

    def __init__(self, device: Device):
        self.requester = Requester(device)
        self.responder = Responder(device)
        self.response = None

    def InverseWalshTransform(self, H, dimension):
        """
                Выполняет обратное преобразование Уолша для входной матрицы.

                Параметры:
                - H: Входная матрица (numpy.ndarray)
                - dimension: Размерность преобразования (int)

                Возвращает:
                - N: Результат обратного преобразования Уолша (numpy.ndarray)
        """
        if dimension == 1:
            N = np.fft.ifft(H)
        elif dimension == 2:
            l = len(H)
            Ed = np.eye(l)
            W = np.fft.ifft2(Ed, s=(H.shape[0], H.shape[1]))
            N = np.fft.ifft2(H) @ W
        else:
            print('Dimension is not correct!')
            return None
        return N

    def WalshTransform(self, N, dimension):
        """
                Выполняет преобразование Уолша для входной матрицы.

                Параметры:
                - N: Входная матрица (numpy.ndarray)
                - dimension: Размерность преобразования (int)

                Возвращает:
                - H: Результат преобразования Уолша (numpy.ndarray)
        """
        if dimension == 1:
            H = np.fft.fft(N)
        elif dimension == 2:
            l = len(N)
            Ed = np.eye(l)
            W = np.fft.fft2(Ed, s=(N.shape[0], N.shape[1]))
            H = np.fft.fft2(N) @ W
        else:
            print('Dimension is not correct!')
            return None
        return H

    def ThresholdFilt(self, H, k, dimension, corr):
        """
                Применяет пороговую фильтрацию к входной матрице.

                Параметры:
                - H: Входная матрица (numpy.ndarray)
                - k: Пороговое значение (float)
                - dimension: Размерность матрицы (int)
                - corr: Флаг коррекции (int)

                Возвращает:
                - W: Результат пороговой фильтрации (numpy.ndarray)
        """
        W = H.copy()
        if dimension == 1:
            index = np.abs(H) < k
            index[0, :] = False
            if corr == 1:
                B = H.copy()
                B[np.logical_not(index)] = 0
                W[0, :] = W[0, :] - np.sum(B)
            W[index] = 0
        elif dimension == 2:
            index = np.abs(H) < k
            index[0, 0] = False
            if corr == 1:
                B = H.copy()
                B[np.logical_not(index)] = 0
                W[0, 0] = W[0, 0] - np.sum(np.sum(B))
            W[index] = 0
        else:
            print('Dimension is not correct!')
            return None
        return W

    def RemoveConstantComponent(self, H, dimension):
        """
                Удаляет постоянную компоненту из входной матрицы.

                Параметры:
                - H: Входная матрица (numpy.ndarray)
                - dimension: Размерность матрицы (int)

                Возвращает:
                - W: Результат удаления постоянной компоненты (numpy.ndarray)
        """
        W = H.copy()
        if dimension == 1:
            W[0, :] = 0
        elif dimension == 2:
            W[0, 0] = 0
        else:
            print('Dimension is not correct!')
            return None
        return W

    def RestoreConstantComponent(self, H, dimension):
        """
                Восстанавливает постоянную компоненту во входной матрице.

                Параметры:
                - H: Входная матрица (numpy.ndarray)
                - dimension: Размерность матрицы (int)

                Возвращает:
                - W: Результат восстановления постоянной компоненты (numpy.ndarray)
        """
        W = H.copy()
        if dimension == 1:
            W[0, :] = W[0, :] - np.sum(W[1:, :], axis=0)
        elif dimension == 2:
            W[0, 0] = W[0, 0] - np.sum(W[0, 1:]) - np.sum(np.sum(W[1:, :]))
        else:
            print('Dimension is not correct!')
            return None
        return W

    def Pack_N_bytes(self, Input_Matrix, num_bytes):
        """
                Упаковывает входную матрицу в байты.

                Параметры:
                - Input_Matrix: Входная матрица (numpy.ndarray)
                - num_bytes: Число байтов (int)

                Возвращает:
                - packed: Упакованные байты (bytes)
        """
        P = Input_Matrix.copy()
        S = P[0]

        n = P.shape[0]

        for i in range(1, n):
            s_p = P[i].copy()

            j = 0
            n_1 = s_p.shape[0]

            while j < n_1:
                if s_p[j] == 0:
                    s_p[j] = 256

                    n_1 = s_p.shape[0]

                    while j < n_1 and s_p[j] < 511 and s_p[j + 1] == 0:
                        s_p[j] = s_p[j] + 1
                        s_p = np.delete(s_p, j + 1)

                        n_1 = s_p.shape[0]

                j = j + 1

            S = np.concatenate((S, s_p))

        packed = S.astype(np.uint16).tobytes()
        packed = self.pad_bytes(packed, num_bytes)
        return packed

    def Unpack_N_bytes(self, packed, n):
        """
                Распаковывает байты в матрицу.

                Параметры:
                - packed: Упакованные байты (bytes)
                - n: Размерность матрицы (int)

                Возвращает:
                - Output_Mass: Распакованная матрица (numpy.ndarray)
        """
        packed_arr = np.frombuffer(packed, dtype=np.uint16)
        LengthL = packed_arr.shape[0]
        Output_Mass = np.zeros((n, n))

        l = 0
        j = 0
        k = 0
        while k < n:
            Output_Mass[j, k] = packed_arr[l]
            l = l + 1
            k = k + 1

        for j in range(1, n):
            k = 0
            while k < n and l < LengthL:
                if packed_arr[l] < 256:
                    Output_Mass[j, k] = packed_arr[l]
                    k = k + 1
                else:
                    s = packed_arr[l] - 256
                    k = k + s + 1

                l = l + 1
        return Output_Mass

    def pad_bytes(self, data, num_bytes):
        """
                Добавляет заполнение до указанного числа байтов.

                Параметры:
                - data: Данные (bytes)
                - num_bytes: Число байтов (int)

                Возвращает:
                - padded_data: Данные с заполнением (bytes)
        """
        current_length = len(data)
        padding_length = num_bytes - current_length % num_bytes
        padding = b'\x00' * padding_length
        padded_data = data + padding
        return padded_data

    def Resized_img(self, img, resolution):
        """
                Изменяет размер изображения до указанного разрешения.

                Параметры:
                - img: Исходное изображение (numpy.ndarray)
                - resolution: Разрешение (tuple)

                Возвращает:
                - img: Измененное изображение (numpy.ndarray)
            """
        h, w = img.shape[:2]
        new_h, new_w = resolution

        resized = np.ndarray((new_h, new_w), dtype=np.uint8)
        y_scale = h / new_h
        x_scale = w / new_w

        for i in range(new_h):
            for j in range(new_w):
                y = int(i * y_scale)
                x = int(j * x_scale)
                resized[i, j] = img[y, x]

        img = resized
        return img

    def convert_to_gray(self, image):
        """
                Преобразует цветное изображение в оттенки серого.

                Параметры:
                - image: Исходное изображение (numpy.ndarray)

                Возвращает:
                - gray: Оттенки серого (numpy.ndarray)
        """
        r, g, b = image[:, :, 0], image[:, :, 1], image[:, :, 2]
        gray = 0.2989 * r + 0.5870 * g + 0.1140 * b
        return gray.astype(np.uint8)

    def encode(self, resolution, img, num_bytes):
        """
                Кодирует изображение.

                Параметры:
                - resolution: Разрешение (tuple)
                - img: Исходное изображение (numpy.ndarray)
                - num_bytes: Число байтов (int)
        """
        gray = self.convert_to_gray(img)
        gray = self.Resized_img(gray, resolution)
        transformed = self.WalshTransform(gray, 2)
        thresholded = self.ThresholdFilt(transformed, 100, 2, 0)
        restored = self.RestoreConstantComponent(thresholded, 2)
        reconstructed = self.InverseWalshTransform(restored, 2)
        packed = self.Pack_N_bytes(reconstructed, num_bytes)
        block_position = (0, 0)  # Assume block starts at (0, 0)
        block_size = reconstructed.shape  # Size of the block

        request_data = (packed, block_position, block_size)
        self.requester.request(request_data)

    def decode(self, resolution):
        """
                Декодирует изображение.

                Параметры:
                - resolution: Разрешение (tuple)
                Возвращает:
                - output: Раскодированное изображение (numpy.ndarray)
            """
        self.response = None
        self.responder.on_request += self.handle_request
        self.responder.run()

        if self.response is not None:
            packed, block_position, block_size = self.response
            n, k = resolution
            unpacked = self.Unpack_N_bytes(packed, n)

            # Extract the corresponding block from the unpacked matrix based on position and size
            output = unpacked[block_position[0]:block_position[0] + block_size[0],
                     block_position[1]:block_position[1] + block_size[1]]

            return output

    def handle_request(self, request):
        self.response = request