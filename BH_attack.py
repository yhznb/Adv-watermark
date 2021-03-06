from PIL import Image, ImageDraw
import numpy as np
import random
import torch
from torch.autograd import Variable
import numpy as np
from torchvision import models, transforms
from scipy.optimize import basinhopping
import os
watermark_path='Berkely'
im_watermark = Image.open(watermark_path+'.png')

scale_size=1.5







def add_watermark_to_image(image,xs, watermark,sl):
    rgba_image = image.convert('RGBA')
    rgba_watermark = watermark.convert('RGBA')

    image_x, image_y = rgba_image.size
    watermark_x, watermark_y = rgba_watermark.size

    # 缩放图片
    scale = sl
    watermark_scale = min(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
    new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
    #rgba_watermark = rgba_watermark.resize(new_size)
    rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)
    # 透明度
    rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x,int(xs[0])))
    rgba_watermark.putalpha(rgba_watermark_mask)

    watermark_x, watermark_y = rgba_watermark.size
    # 水印位置
    #rgba_image.paste(rgba_watermark, (0, 0), rgba_watermark_mask) #右下角
    ##限制水印位置

    a=np.array(xs[1])
    a=np.clip(a, 0, 224-watermark_x)

    b= np.array(xs[1])
    b = np.clip(b, 0, 224 - watermark_y)




    x_pos=int(a)
    y_pos=int(b)
    rgba_image.paste(rgba_watermark, (x_pos, y_pos), rgba_watermark_mask)  # 右上角
    rgba_watermark.save('newlogo.png')
    return rgba_image
backbone_name = 'resnet101'
model = models.__dict__[backbone_name](pretrained=True) # N x 2048
model.eval()
if torch.cuda.is_available():
        model.cuda()

def label_model(input):
    transform = transforms.Compose([
        transforms.Resize(224),
        transforms.CenterCrop(224),
        transforms.ToTensor()]
    )
    input=transform(input)
    input = Variable(torch.unsqueeze(input, dim=0).float(), requires_grad=False)
    return model(input.cuda())
def predict_classes(img,xs, watermark, target_class,sl):
    # Perturb the image with the given pixel(s) x and get the prediction of the model
    imgs_perturbed = add_watermark_to_image(img,xs, watermark,sl)
    imgs_perturbed = imgs_perturbed.convert('RGB')


    predictions = label_model(imgs_perturbed).cpu().detach().numpy()
    # This function should always be minimized, so return its complement if needed
    predictions=predictions[0][target_class]
    return predictions
true_lsit=[2, 3, 6, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 22, 23, 24, 25, 26, 30, 33, 34, 35, 42, 43, 44, 46, 48, 51, 52, 53, 55, 56, 57, 59, 63, 65, 66, 68, 71, 73, 74, 76, 77, 78, 79, 80, 81, 85, 88, 90, 94, 96, 97]
classes=['65', '970', '230', '809', '516', '57', '334', '415', '674', '332', '109', '286', '370', '757', '595', '147', '108', '23', '478', '517', '334', '173', '948', '727', '23', '846', '270', '167', '55', '858', '324', '573', '150', '981', '586', '887', '32', '398', '777', '74', '516', '756', '129', '198', '256', '725', '565', '167', '717', '394', '92', '29', '844', '591', '358', '468', '259', '994', '872', '588', '474', '183', '107', '46', '842', '390', '101', '887', '870', '841', '467', '149', '21', '476', '80', '424', '159', '275', '175', '461', '970', '160', '788', '58', '479', '498', '369', '28', '487', '50', '270', '383', '366', '780', '373', '705', '330', '142', '949', '349', '473', '159', '872', '878', '201', '906', '70', '486', '632', '608', '122', '720', '227', '686', '173', '959', '638', '646', '664', '645', '718', '483', '852', '392', '311', '457', '352', '22', '934', '283', '802', '553', '276', '236', '751', '343', '528', '328', '969', '558', '163', '328', '771', '726', '977', '875', '265', '686', '590', '975', '620', '637', '39', '115', '937', '272', '277', '763', '789', '646', '213', '493', '647', '504', '937', '687', '781', '666', '583', '158', '825', '212', '659', '257', '436', '196', '140', '248', '339', '230', '361', '544', '935', '638', '627', '289', '867', '272', '103', '584', '180', '703', '449', '771', '118', '396', '934', '16', '548', '993', '704', '457', '233', '401', '827', '376', '146', '606', '922', '516', '284', '889', '475', '978', '475', '984', '16', '77', '610', '254', '636', '662', '473', '213', '25', '463', '215', '173', '35', '741', '125', '787', '289', '425', '973', '1', '167', '121', '445', '702', '532', '366', '678', '764', '125', '349', '13', '179', '522', '493', '989', '720', '438', '660', '983', '533', '487', '27', '644', '750', '865', '1', '176', '694', '695', '798', '925', '413', '250', '970', '821', '421', '361', '920', '761', '27', '676', '92', '194', '897', '612', '610', '283', '881', '906', '899', '426', '554', '403', '826', '869', '730', '0', '866', '580', '888', '43', '64', '69', '176', '329', '469', '292', '991', '591', '346', '1', '607', '934', '784', '572', '389', '979', '654', '420', '390', '702', '24', '102', '949', '508', '361', '280', '65', '777', '359', '165', '21', '7', '525', '760', '938', '254', '733', '707', '463', '60', '887', '531', '380', '982', '305', '355', '503', '818', '495', '472', '293', '816', '195', '904', '475', '481', '431', '260', '130', '627', '460', '622', '696', '300', '37', '133', '637', '675', '465', '592', '741', '895', '91', '109', '582', '694', '546', '208', '488', '786', '959', '192', '834', '879', '649', '228', '621', '630', '107', '598', '420', '134', '133', '185', '471', '230', '974', '74', '76', '852', '383', '267', '419', '359', '484', '510', '33', '177', '935', '310', '998', '270', '598', '199', '998', '836', '14', '97', '856', '398', '319', '549', '92', '765', '412', '945', '160', '265', '638', '619', '722', '183', '674', '468', '468', '885', '675', '636', '196', '912', '721', '16', '199', '175', '775', '944', '350', '557', '361', '361', '594', '861', '257', '606', '734', '767', '746', '788', '346', '153', '739', '414', '915', '940', '152', '943', '849', '712', '100', '546', '744', '764', '141', '39', '993', '758', '190', '888', '18', '584', '341', '875', '359', '388', '894', '437', '987', '517', '372', '286', '662', '713', '915', '964', '146', '529', '416', '376', '147', '902', '26', '398', '175', '270', '335', '532', '540', '607', '495', '222', '801', '982', '304', '166', '56', '868', '448', '744', '567', '277', '298', '651', '377', '684', '832', '39', '219', '863', '868', '794', '80', '983', '269', '238', '498', '223', '521', '830', '260', '491', '896', '220', '680', '48', '542', '961', '820', '148', '114', '99', '143', '691', '796', '986', '346', '367', '939', '875', '625', '482', '464', '812', '705', '860', '466', '781', '499', '338', '488', '858', '795', '437', '11', '625', '965', '874', '928', '600', '86', '133', '149', '865', '480', '325', '499', '834', '421', '298', '900', '905', '184', '740', '258', '762', '295', '129', '240', '833', '471', '385', '899', '162', '288', '450', '850', '227', '273', '954', '965', '611', '643', '147', '290', '866', '186', '156', '776', '775', '998', '333', '325', '572', '927', '744', '777', '833', '551', '301', '716', '848', '102', '790', '959', '404', '987', '415', '455', '242', '600', '517', '16', '320', '632', '568', '338', '216', '331', '726', '959', '605', '134', '677', '288', '10', '718', '852', '440', '104', '712', '388', '261', '609', '620', '341', '579', '450', '628', '217', '878', '763', '209', '126', '663', '864', '232', '776', '942', '336', '733', '681', '512', '78', '668', '699', '746', '46', '618', '330', '615', '427', '62', '116', '127', '955', '306', '425', '190', '370', '187', '971', '534', '397', '657', '840', '718', '116', '836', '994', '419', '764', '214', '285', '641', '951', '882', '13', '829', '624', '216', '665', '521', '268', '468', '418', '728', '356', '449', '194', '362', '948', '924', '249', '524', '992', '571', '283', '608', '129', '486', '859', '498', '21', '467', '591', '924', '556', '97', '898', '586', '10', '202', '67', '501', '141', '603', '727', '101', '995', '278', '964', '240', '423', '634', '533', '424', '451', '555', '732', '514', '803', '300', '551', '753', '411', '315', '963', '129', '389', '601', '526', '839', '299', '578', '112', '960', '632', '867', '273', '61', '427', '367', '924', '413', '34', '773', '654', '131', '874', '282', '891', '956', '201', '267', '969', '200', '673', '423', '907', '57', '27', '459', '863', '322', '934', '663', '424', '687', '837', '958', '645', '120', '306', '930', '121', '694', '524', '205', '137', '849', '681', '380', '586', '916', '478', '182', '874', '715', '590', '111', '19', '161', '915', '730', '678', '822', '818', '699', '601', '673', '233', '501', '624', '679', '400', '581', '665', '903', '622', '585', '800', '899', '669', '81', '746', '595', '935', '668', '295', '893', '266', '628', '987', '367', '294', '727', '12', '876', '186', '589', '70', '129', '454', '17', '946', '200', '181', '163', '80', '940', '587', '21', '198', '25', '932', '339', '480', '764', '883', '454', '807', '287', '868', '614', '814', '591', '919', '508', '479', '452', '155', '41', '163', '606', '7', '269', '576', '858', '506', '23', '447', '397', '595', '753', '5', '186', '667', '305', '46', '303', '673', '927', '91', '34', '757', '406', '390', '76', '517', '806', '330', '34', '130', '103', '56', '545', '78', '31', '372', '235', '516', '159', '187', '930', '888', '96', '444', '991', '872', '302', '566', '33', '818', '694', '406', '20', '18', '371', '320', '724', '994', '730', '613', '105', '878', '311', '883', '367', '243', '627', '944', '43', '412', '921', '332', '474', '276', '629', '917', '77', '643', '556', '998', '328', '723', '161', '250', '1', '919', '392', '264', '408', '633', '495', '188', '884', '335', '795', '241', '842', '71', '862', '254', '27', '409', '444', '433', '324', '322', '688', '579', '562', '917', '803', '863', '44', '719', '16', '384', '328', '348', '194', '678', '593', '9', '371', '25', '913', '667', '104', '72', '223', '268', '283', '477', '53', '465', '100', '543', '133', '159', '439', '151', '355', '392', '577', '72', '383', '846', '145', '109', '988', '824', '293', '411', '718', '484', '966', '259', '344', '132', '128', '154', '210', '508', '445', '138', '233', '376', '720', '464', '960', '999', '455', '613', '314', '993', '17', '759', '843', '721', '331', '508', '432', '778', '370', '468', '489', '375', '263', '164', '418', '377', '878', '283', '838', '442', '380', '641', '628', '592', '59', '224', '587', '724', '207', '228', '8', '962', '575', '988', '889', '551', '990', '141', '120', '207', '121', '946', '463', '786', '167', '256', '986', '28', '283', '834', '720', '411', '80', '173', '29', '606', '636', '156', '91', '734', '569', '458', '84', '230', '274', '707', '75', '965', '260', '978', '767', '372', '717', '764', '96', '958', '857', '327', '140', '88', '156', '137', '842', '556', '492', '771', '653', '484', '269', '787', '827', '644', '393', '386', '654', '137', '715', '906', '724', '823', '516', '64', '850', '321', '611', '392', '509', '207', '655', '397', '949', '188', '830', '750', '259', '294', '450', '511', '477', '255', '814', '781', '177', '654', '911', '680', '769', '830', '273', '24', '463', '321', '480', '331', '21', '556', '481', '420', '179', '216', '212', '152', '333', '646', '152', '635', '128', '993', '351', '928', '266', '830', '371', '335', '319', '786', '816', '334', '509', '444', '155', '902', '527', '817', '346', '848', '173', '438', '443', '745', '374', '548', '552', '619', '411', '451', '278', '715', '629', '855', '694', '709', '611', '168', '113', '782', '974', '147', '69', '546', '11', '543', '629', '127', '413', '349', '345', '922', '484', '78', '200', '399', '192', '543', '89', '423', '323', '764', '970', '829', '645', '542', '809', '195', '732', '474', '915', '820', '238', '643', '978', '214', '844', '717', '925', '57', '911', '444', '827', '245', '250', '930', '791', '401', '648', '773', '978', '875', '637', '975', '586', '873', '472', '978', '909', '102', '878', '784', '398', '355', '643', '279', '92', '523', '50', '510', '765', '281', '870', '748', '253', '749', '754', '452', '775', '261', '562', '506', '289', '827', '456', '449', '117', '97', '101', '291', '346', '809', '997', '168', '896', '714', '126', '593', '8', '432', '72', '158', '958', '662', '945', '47', '919', '427', '924', '185', '685', '124', '660', '449', '434', '178', '356', '128', '819', '157', '404', '23', '943', '155', '756', '797', '916', '254', '9', '471', '577', '255', '882', '654', '261', '931', '950', '360', '246', '872', '982', '519', '826', '556', '220', '928', '402', '911', '601', '179', '639', '302', '767', '778', '697', '178', '500', '912', '557', '745', '611', '401', '571', '621', '206', '89', '394', '481', '627', '333', '701', '644', '364', '450', '972', '199', '621', '795', '265', '118', '705', '565', '519', '641', '75', '757', '590', '749', '374', '986', '76', '83', '14', '945', '683', '770', '318', '268', '429', '269', '828', '503', '150', '344', '858', '45', '959', '884', '333', '953', '86', '204', '62', '960', '222', '178', '178', '274', '21', '552', '147', '555', '566', '74', '264', '399', '285', '768', '296', '327', '502']





# xs = np.array([80,110,100])
# # im_after = add_watermark_to_image(im_before, xs,im_watermark)
# # im_after=im_after.convert('RGB')
# # im_after.save('watermark.png')
# # predict=label_model(im_after).detach().numpy()

def attack_success( img, xs,watermark,sl,target_class,targeted_attack=False, verbose=False):
    # Perturb the image with the given pixel(s) and get the prediction of the model
    attack_image = add_watermark_to_image(img,xs,watermark,sl)
    attack_image = attack_image.convert('RGB')
    predict = label_model(attack_image).cpu().detach().numpy()

    predicted_class = np.argmax(predict)
    # If the prediction is what we want (misclassification or
    # targeted classification), return True
    attack_image.save('temp1_VGG.png')
    if verbose:
        print('Confidence:', predict[0][target_class])
    if ((targeted_attack and predicted_class == target_class) or
            (not targeted_attack and predicted_class != target_class)):

        return True

### (0,180) (0,169) （0，169）
#success = attack_success(im_before, xs, im_watermark, int(classes[true_lsit[3]]), verbose=True)
#print('Attack success:', success == True)

def attack(im_before,label,im_watermark,sl,target=None, watermark_count=1,maxiter=5,
           popsize=400,verbose=False):
    watermark_x1, watermark_y1 = im_watermark.size
    watermark_scale = min(224 / (sl * watermark_x1), 224 / (sl * watermark_y1))
    print(watermark_scale)
    watermark_x1 = int(watermark_x1 * watermark_scale)
    watermark_y1= int(watermark_y1 * watermark_scale)

    xs = [100, 0, 0]

    def predict_fn(xs):
        return predict_classes(im_before, xs, im_watermark, int(label),sl)

    def callback_fn(xs, f, accept):
        return attack_success(im_before, xs, im_watermark, sl,int(label), verbose=True)

    class MyTakeStep(object):
        def __init__(self, stepsize=10):
            self.stepsize = stepsize

        def __call__(self, x):
            s = self.stepsize
            x[0] += np.random.uniform(-2* s, 2 * s)
            x[1] += np.random.uniform(-5 * s, 5* s)
            x[2] += np.random.uniform(-5* s, 5 * s)
            return x
    mytakestep = MyTakeStep()


    class MyBounds(object):
        def __init__(self,xmax=[255,224-watermark_x1,224-watermark_y1],xmin=[0,0,0]):
            self.xmax=np.array(xmax)
            self.xmin=np.array(xmin)
        def __call__(self,**kwargs):
            x=kwargs["x_new"]
            tmax=bool(np.all(x<=self.xmax))
            tmin=bool(np.all(x>=self.xmin))
            return tmax and tmin
    mybounds=MyBounds()



    attack_result = basinhopping(func=predict_fn, x0=xs, callback=callback_fn, take_step=mytakestep,accept_test=mybounds)
    return attack_result


#print(attack(im_before,'332',im_watermark,watermark_count=1).x)
true_list=[]
count=0

for i in range(1000):

    path='imagenet/'+str(i)+'.png'
    img = Image.open(path).convert("RGB")

    predict=label_model(img).cpu().detach().numpy()
    #print(np.argmax(predict))

    if np.argmax(predict)==int(classes[i]):
        print("*****")
        print(i)
        result=attack(img,classes[i],im_watermark,scale_size)
        # print(result)

        result_img=Image.open('temp1_VGG.png')
        result_img=result_img.convert('RGB')
        new_predict = label_model(result_img).cpu().detach().numpy()
        if np.argmax(new_predict)==int(classes[i]):
            count=count+1
            print('success')
        if not os.path.exists('ACMMMlogo/scale_'+str(scale_size)+'/'+watermark_path):
            os.makedirs('ACMMMlogo/scale_'+str(scale_size)+'/'+watermark_path)
        result_img.save('ACMMMlogo/scale_'+str(scale_size)+'/'+watermark_path+'/advwatermark_'+str(i)+'.png')
        print("*****")
        print(np.argmax(predict))
        true_list.append(i)
print('攻击之后：',count)
print('攻击之前：',len(true_list))
print('攻击成功率：',1-count/len(true_list))

