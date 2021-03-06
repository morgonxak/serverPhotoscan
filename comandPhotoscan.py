import PhotoScan
import os

def creatProject(project_path, project_name):
    '''
    Создаем новый проект либо открывваем существующий
    :param project_path: Путь до папки с проектом
    :param project_name: Имя проекта
    :return: Chunk
    '''
    doc = PhotoScan.app.document
    doc.save(project_path + project_name + ".psx")
    if len(doc.chunks):
        chunk = PhotoScan.app.document.chunk
    else:
        chunk = doc.addChunk()

    return chunk, doc

def AddPhoto(chunk, patchDirImage):
    '''
    patchDirImage: Путь до папки с изображениями
    :param chunk
    :param patchDirImage r"F:\18.08.02 Шерегеш\Фото\1 флешка"
    :return:
    '''
    import os
    path_photos = patchDirImage
    image_list = os.listdir(path_photos)
    photo_list = list()
    for photo in image_list:
        if photo.rsplit(".", 1)[1].lower() in ["jpg", "jpeg", "tif", "tiff"]:
            photo_list.append("/".join([path_photos, photo]))
    return chunk.addPhotos(photo_list)

def alingPhotos(chunk, doc):
    '''
    выровнить фотографии
    :param accuracy:
    :param generic_preselection:
    :param reference_preselection:
    :param filter_mask:
    :param keypoint_limit:
    :param tiepoint_limit:
    :return:
    '''
    chunk.matchPhotos(accuracy=PhotoScan.HighAccuracy, generic_preselection=True, reference_preselection=True,
                  filter_mask=False, keypoint_limit=350000, tiepoint_limit=0)
    chunk.alignCameras()
    doc.save()

def setCoordinateSystem(chunk, doc):
    '''
    Установить систему координат
    :return:
    '''
    chunk.crs = PhotoScan.CoordinateSystem(CK = "EPSG::4326")
    chunk.updateTransform()
    doc.save()

def buildDenseCloud(chunk, doc):
    '''
    строить плотное облако
    :param quality:
    :param filter:
    :return:
    '''
    #chunk.buildDenseCloud(quality=PhotoScan.UltraQuality, filter=PhotoScan.AggressiveFiltering)

    chunk.buildDepthMaps(quality=PhotoScan.UltraQuality, filter=PhotoScan.AggressiveFiltering)
    chunk.buildDenseCloud(point_colors=True)
    doc.save()

def exportPoints(chunk, project_path, project_name):
    '''
    Экспорт облако точек
    :param project_path: Путь до папки для экспорта
    :param project_name: Имя файла
    :param binary:
    :param precision:
    :param colors:
    :param format:
    :return:
    '''
    chunk.exportPoints(project_path + project_name + ".las", binary=True, precision=6, colors=True,
                   format=PhotoScan.PointsFormatLAS)

def buildModel(chunk, doc):
    '''
    Создать модель
    :param surface:
    :param interpolation:
    :param face_count:
    :return:
    '''
    chunk.buildModel(surface=PhotoScan.HeightField, interpolation=PhotoScan.EnabledInterpolation,
                 face_count=PhotoScan.MediumFaceCount)
    doc.save()

def buildDEM(chunk, doc):
    '''
    Построить карту высот
    :param source:
    :param interpolation:
    :return:
    '''
    chunk.buildDem(source=PhotoScan.DenseCloudData, interpolation=PhotoScan.EnabledInterpolation)
    doc.save()

def exportDem(chunk, project_path, project_name):
    '''
    Экспортировать карту высот
    :param project_path:
    :param project_name:
    :param image_format:
    :param format:
    :param nodata:
    :param write_kml:
    :param write_world:
    :return:
    '''
    chunk.exportDem(project_path + project_name + "_DEM.tif", image_format=PhotoScan.ImageFormatTIFF,
                format=PhotoScan.RasterFormatTiles, nodata=-32767, write_kml=False, write_world=True)

def buildOrtho(chunk, doc):
    '''
    Построить ортофотоплан
    :param surface:
    :param blending:
    :param color_correction:
    :return:
    '''
    #chunk.buildOrthomosaic(surface=PhotoScan.ElevationData, blending=PhotoScan.MosaicBlending)
    chunk.buildOrthomosaic(surface=PhotoScan.ElevationData, blending=PhotoScan.MosaicBlending, color_correction=True, fill_holes=True)

    doc.save()

def exportOrthomosaic(chunk, project_path, project_name):
    '''
    Экспорт ортофотоплана
    :param project_path: Папка
    :param project_name: Имя
    :param image_format:
    :param format:
    :param raster_transform:
    :param write_kml:
    :param write_world:
    :return:
    '''
    chunk.exportOrthomosaic(project_path + project_name + ".tif", image_format=PhotoScan.ImageFormatTIFF,
                        format=PhotoScan.RasterFormatTiles, raster_transform=PhotoScan.RasterTransformNone,
                        write_kml=False, write_world=True)

if __name__ == "__main__":
    creatProject()

    #self.chunk, self.doc = creatProject(PATH_DIR + '\/' + data["ID_User"] + '\/', 'project')
    #AddPhoto(self.chunk, PATH_DIR + '\/' + data["ID_User"] + '\/' + 'photo')
