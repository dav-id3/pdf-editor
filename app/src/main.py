import os
from pdf2image import convert_from_path
import img2pdf
from PIL import Image
import re, shutil

base_path = "data"
image_folders_path = base_path + "/img_folders"
pdf_files_path = base_path + "/pdf_files"


def main () -> None:
    if os.path.exists(base_path) == False:
        raise Exception ("Base path does not exist")
    
    img_folder_list = [i for i in os.listdir(image_folders_path) if not i.startswith(".")]
    pdf_list = [i for i in os.listdir(pdf_files_path)if not i.startswith(".")]
    
    img_folder_path_dict = {}
    for img_folder in img_folder_list:  
        img_folder_path_dict[img_folder] = image_folders_path + "/" + img_folder

    for pdf_name in pdf_list:
        pdf_file_path = pdf_files_path + "/" + pdf_name
        pdf_regex = re.compile(r"(.*)(\.pdf)")
        pdf_name = pdf_regex.sub(r"\1", pdf_name)

        if not img_folder_path_dict.get(pdf_name, False):
            continue
        
        # convert pdf to images before going through the images
        img_folder_path = img_folder_path_dict.get(pdf_name)
        pdf_img_folder_path = img_folder_path + "/temp_pdf_images"
        
        if os.path.exists(pdf_img_folder_path):
            shutil.rmtree(pdf_img_folder_path)
        os.mkdir(pdf_img_folder_path)

        pages = convert_from_path(pdf_file_path, fmt="pdf")
        for i, page in enumerate(pages):
            image_f_name = f'{pdf_name}_{str(i).zfill(3)}.png'
            page.save(os.path.join(pdf_img_folder_path, image_f_name))
      
    progress = 0
    for img_folder, img_folder_path in img_folder_path_dict.items():
        if os.path.exists(img_folder_path + "/temp_pdf_images") == False:
            # stage images in the folder
            img_paths_to_pdf = []
            for img in [i for i in os.listdir(img_folder_path) if not i.startswith(".")]:
                img_paths_to_pdf.append(img_folder_path + "/" + img)
        else:
            # compare num of images from existing pdf and images in the folder and define which images to add to the pdf
            pdf_imgs_num = len([i for i in os.listdir(img_folder_path + "/temp_pdf_images") if not i.startswith(".")])
            img_folder_imgs_num = len([i for i in os.listdir(img_folder_path) if i.endswith(".png")])
            
            if pdf_imgs_num >= img_folder_imgs_num:
                shutil.rmtree(img_folder_path + "/temp_pdf_images")
                progress += 1; print(f"Progress: {progress}/{len(img_folder_path_dict)} (No new images))")
                continue
            
            # stage images not in the pdf but in the folder
            added_imgs = [i for i in os.listdir(img_folder_path)if not i.startswith(".") and i.endswith(".png")][img_folder_imgs_num - pdf_imgs_num + 1:]
            
            img_paths_to_pdf = [img_folder_path + "/temp_pdf_images/" + i for i in os.listdir(img_folder_path + "/temp_pdf_images") if not i.startswith(".")]
            for added_img in added_imgs:
                img_paths_to_pdf.append(img_folder_path + "/" + added_img)
                
        # create pdf from images
        pdf_path = pdf_files_path + "/" + img_folder + ".pdf"
        with open(pdf_path,"wb") as f:
            f.write(img2pdf.convert([i for i in img_paths_to_pdf if i.endswith(".png")]))

        # delete temp folder for images from pdf
        if os.path.exists(img_folder_path + "/temp_pdf_images"):
            shutil.rmtree(img_folder_path + "/temp_pdf_images")

        progress += 1; print(f"Progress: {progress}/{len(img_folder_path_dict)}")

if __name__ == "__main__":
    main()


          
          

            