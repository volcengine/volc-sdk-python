# coding:utf-8
from __future__ import print_function

from volcengine.visual.VisualService import VisualService

if __name__ == '__main__':
    visual_service = VisualService()

    # call below method if you dont set ak and sk in $HOME/.volc/config
    visual_service.set_ak('ak')
    visual_service.set_sk('sk')
    # visual_service.set_host('host')

    # below shows the sdk usage for all common apis,
    # if you cannot find the needed one, please check other example files in the same dir
    # or contact us for further help
    form = dict()
    form["image_base64"] = "image_base64_str"

    # 车牌检测
    # resp = visual_service.car_plate_detection(form)

    # 人像畸变矫正
    # resp = visual_service.distortion_free(form)

    # 图片拉伸修复
    # resp = visual_service.stretch_recovery(form)

    # 图片流动
    # form["motion_ratio"] = 2
    # resp = visual_service.image_flow(form)

    # 图片评分
    # resp = visual_service.image_score(form)

    # 图片配文
    # resp = visual_service.poem_material(form)

    # 表情编辑
    # form["service_choice"] = 0
    # resp = visual_service.emoticon_edit(form)

    # 闭眼转睁眼
    # resp = visual_service.eye_close2open(form)

    # 车辆分割
    # resp = visual_service.car_segment(form)

    # 车辆检测
    # resp = visual_service.car_detection(form)

    # 天空分割
    # resp = visual_service.sky_segment(form)

    # 老照片修复
    # resp = visual_service.convert_photo(form)

    # 图像增强
    # resp = visual_service.enhance_photo(form)

    # 通用分割
    # resp = visual_service.general_segment(form)

    # 人体分割
    # form["refine"] = 0
    # form["return_foreground_image"] = 0
    # resp = visual_service.human_segment(form)

    # 人像漫画风
    # form["cartoon_type"] = "jpcartoon_head"
    # form["rotation"] = 0 # this param is valid only when cartoon_type == jpcartoon_head
    # resp = visual_service.jpcartoon(form)

    # 人脸融合
    # form["template_base64"] = "template_base64_str"
    # form["action_id"] = "faceswap"
    # resp = visual_service.face_swap(form)

    # 通用OCR
    # resp = visual_service.ocr_normal(form)

    # 身份证OCR
    # resp = visual_service.id_card(form)

    # 银行卡OCR
    # resp = visual_service.bank_card(form)

    # 营业执照OCR
    # resp = visual_service.clue_license(form)

    # 驾驶证OCR
    # resp = visual_service.driving_license(form)

    # 行驶证OCR
    # resp = visual_service.vehicle_license(form)

    # 出租车票OCR
    # resp = visual_service.taxi_invoice(form)

    # 火车票OCR
    # resp = visual_service.train_ticket(form)

    # 行程单OCR
    # resp = visual_service.flight_invoice(form)

    # 增值税发票OCR
    # resp = visual_service.vat_invoice(form)

    # 定额发票OCR
    # resp = visual_service.quota_invoice(form)

    # 发型编辑
    # resp = visual_service.hair_style(form)

    # 智能变美
    # resp = visual_service.face_pretty(form)

    # 活照片
    # resp = visual_service.image_animation(form)

    # 视频选封面
    # resp = visual_service.cover_video(form)

    # 希区柯克
    # resp = visual_service.dolly_zoom(form)

    # 人像特效
    # resp = visual_service.potrait_effect(form)

    # 图像风格转换
    # resp = visual_service.image_style_conversion(form)

    # 3d游戏风
    # resp = visual_service.three_d_game_cartoon(form)

    # 头发抠图
    # resp = visual_service.hair_segment(form)
    # form["mode"] = 0
    # form["refine_mask"] = 0
    # form["flip_test"] = 0

    # 印章识别
    # resp = visual_service.ocr_seal(form)

    # pdf识别
    # resp = visual_service.ocr_pdf(form)

    # 高速公路过路费
    # resp = visual_service.ocr_pass_invoice(form)

    # 商标证
    # resp = visual_service.ocr_trade(form)

    # 软件著作权
    # resp = visual_service.ocr_ruanzhu(form)

    # 化妆品生产许可证
    # resp = visual_service.ocr_cosmetic_product(form)

    # 表格识别
    # resp = visual_service.ocr_table(form)

    # 智能绘图（文本转图片通用版）
    # resp = visual_service.t2i_ldm(form)

    # 智能绘图（名画版）
    # resp = visual_service.img2img_style(form)

    # 智能绘图（漫画版）
    # resp = visual_service.img2img_anime(form)

    print(resp)
