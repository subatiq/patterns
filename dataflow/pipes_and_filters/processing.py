from PIL.Image import Image
from filter import Filter


class ResizeFilter(Filter):
    def _process(self, image: Image) -> Image:
        return image.resize((720, 512))


class BnWFilter(Filter):
    def _process(self, image: Image) -> Image:
        return image.convert('1')


class SaveFilter(Filter):
    def _process(self, image: Image) -> Image:
        image.save('out.jpg')
        return image

