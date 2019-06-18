import glob
import time
import os
import subprocess
import cv2 as cv
import numpy as np
from natsort import natsorted

from utils import is_machine_generated
from service.extract_tables import crop_boundary
import shutil

def pdf_split_with_pdfseparate(file_location, page_dir_location):
		"""
		Fall back to PDFSeparate if PyPDF2 fails.
		:param file_location: PDF File location
		:type file_location: str
		:param page_dir_location: Location to store pdf pages
		:type page_dir_location: str
		:return: Page count
		:rtype: int
		"""
		pdf_separate_cmd = "pdfseparate " + file_location + " " + page_dir_location + "/" + "page-%d.pdf"
		pdf_page_count_cmd = "pdfinfo " + file_location + " | grep Pages | awk '{print $2}'"
		pdf_separate_process = subprocess.Popen(pdf_separate_cmd, shell=True, stdout=subprocess.PIPE)
		pdf_separate_process.communicate()
		pdf_page_count_process = subprocess.Popen(pdf_page_count_cmd, shell=True, stdout=subprocess.PIPE)
		page_count = pdf_page_count_process.communicate()
		if pdf_page_count_process.returncode == 0 and pdf_separate_process.returncode == 0:
				return page_count[0]
		else:
				return -1


def pdf_page_to_image(file_path,
											output_file_path,
											dpi=300,
											jpeg_compression_quality=100, ):
		"""
		Given a single page pdf's `file_path` convert it to a jpg file of `dpi` resolution and save it as
		`output_file_path`.
		:param file_path: File path of the input pdf
		:param output_file_path: File path where the resultant image should be stored
		:param jpeg_compression_quality: An integer in [1, 100]
		:param dpi: resolution of the resultant image
		"""

		args = [
				"gs",
				"-dNOPAUSE",
				"-dBATCH",
				"-dSAFER",
				"-sDEVICE=jpeg",
				f"-dJPEGQ={jpeg_compression_quality}",
				f"-r{dpi}",
				f"-sPageList={1}",
				"-dQUIET",
				f"-sOutputFile={output_file_path}",
				file_path
		]

		print(f"ARGS-->{args}")
		subprocess.check_output(args)


def convert_pdf_to_text(pdf_path, filename, raw=False):
		pdf_text_cmd = f"pdftotext" + " " + f"{'-raw' if raw else '-layout'}" + " " + pdf_path + " " + filename
		pdf_text_process = subprocess.Popen(pdf_text_cmd, shell=True, stdout=subprocess.PIPE)
		#print("-->Command-->", pdf_text_cmd)
		text = pdf_text_process.communicate()[0]
		return text


def make_machined_page_pdf(img_path, op_pdf_path):
		print(f"READ_SCANNED_PDF-3.1--->", time.time())
		pdf_path_without_ext = os.path.splitext(op_pdf_path)[0]
		cmd = "tesseract " + img_path + " " + pdf_path_without_ext + " --dpi 300 --oem 1 " + " pdf"
		print(f"READ_SCANNED_PDF-3.2--->", time.time())
		process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
		print(f"READ_SCANNED_PDF-3.3--->", time.time())
		#uncomment below
		#process.communicate()[0]
		print(f"READ_SCANNED_PDF-3.4--->", time.time())

		# cmd = [
		#			"tesseract",
		#			img_path,
		#			pdf_path_without_ext,
		#			"--oem 1",
		#			"pdf"
		# ]
		# print(subprocess.check_output(['tesseract', '--version']))
		# print(' '.join(cmd))
		# subprocess.run(cmd)


def stitch_pdfs(pdf_pages_path):
		try:
				pages = natsorted(glob.glob(os.path.join(pdf_pages_path, "*.pdf")))
				stitch_cmd = "pdfunite "
				for page in pages:
						stitch_cmd = stitch_cmd + " " + str(page)
				stitched_pdf_path = str(pdf_pages_path) + "/stitched.pdf"
				stitch_cmd = stitch_cmd + " " + stitched_pdf_path
				#print("Stictch Command->", stitch_cmd)
				process = subprocess.Popen(stitch_cmd, shell=True, stdout=subprocess.PIPE)
				process.communicate()[0]
		except Exception as e:
				print("Error Stitching")
				print(e)

def read_scanned_image(filename, doc_dir_location, erosion_val=0):
		try:
				print("***1***")
				page_dir_location = os.path.join(doc_dir_location, 'pages') 
				image_dir_location = os.path.join(doc_dir_location, 'images')
				machined_pdf_location = os.path.join(doc_dir_location, 'pdfs')
				text_dir = os.path.join(doc_dir_location, 'texts')

				print("***2***")
				os.makedirs(page_dir_location)
				os.makedirs(image_dir_location)
				os.makedirs(machined_pdf_location)
				os.makedirs(text_dir)
				print("***3***")

				try:
						crop_boundary( filename )
				except:
						pass
				img = cv.imread( filename, 0 )
				img = cv.resize(img, None, fx=1.5, fy=1.3, interpolation=cv.INTER_CUBIC)
				img = cv.medianBlur(img, 5)
				#ret, th1 = cv.adaptiveThreshold(img,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY,11,2)
				#ret, th1 = cv.threshold(img,180,255,cv.THRESH_BINARY)
				ret, th1 = cv.threshold(img,180,255,cv.THRESH_BINARY)
				cv.imwrite( filename, th1)

				print("***4***", filename)

				pdf_page_name_without_ext = os.path.basename(filename).split('.')[0] + ".pdf"
				print("pdf_page_name_without_ext=======>", pdf_page_name_without_ext)
				make_machined_page_pdf( filename, os.path.join(machined_pdf_location, pdf_page_name_without_ext))
				print("===CREATED_PDF===")
				print("***5***")
				stitch_pdfs( page_dir_location )
				stitch_pdfs(machined_pdf_location)
				print("***6***")


				machined_pages = natsorted(glob.glob(os.path.join(machined_pdf_location, "*.pdf")))
				for mach_page in machined_pages:
						#print("************MACHINE_PAGE************", mach_page)
						pdf_page_name_without_ext = os.path.basename(mach_page).split('.')[0] + ".txt"
						convert_pdf_to_text(mach_page, os.path.join(text_dir, pdf_page_name_without_ext))
				print("***7***")

				stitched_file = os.path.join( machined_pdf_location, 'stitched.pdf')
				return {'text_file_path': text_dir, 'stitched_pdf_path': stitched_file}


		except Exception as error:
				print("read_scanned_image ERROR===>", error)
				pass

def get_string(img_path):
		print("=======START=======")
		# Read image using opencv
		img = cv.imread(img_path)
		file_name = os.path.basename(img_path).split('.')[0]
		file_name = file_name.split()[0]

		"""
		output_path = os.path.join(output_dir, file_name)
		if not os.path.exists(output_path):
				os.makedirs(output_path)
		"""

		# Crop the areas where provision number is more likely present
		#img = crop_image(img, pnr_area[0], pnr_area[1], pnr_area[2], pnr_area[3])
		img = cv.resize(img, None, fx=1.2, fy=1.2, interpolation=cv.INTER_CUBIC)

		# Convert to gray
		img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

		# Apply dilation and erosion to remove some noise
		kernel = np.ones((1, 1), np.uint8)
		img = cv.dilate(img, kernel, iterations=1)
		#img = cv.erode(img, kernel, iterations=1)

		#  Apply threshold to get image with only black and white
		#img = apply_threshold(img, method)
		img = cv.adaptiveThreshold(cv.GaussianBlur(img, (5, 5), 0), 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 31, 2)
		#save_path = os.path.join(output_path, file_name + "_filter_" + str(method) + ".jpg")
		cv.imwrite(img_path, img)
		print("=======END=======")

def check_for_rotated_image(image_path):
		import re

		print("check_for_rotated_image********")
		#command = ['tesseract', image_path, 'stdout', '-l', 'eng', '--psm', '0']
		try:
				command = ['tesseract', image_path, 'stdout', '--psm', '0']
				res = subprocess.check_output(command)
				result = str(res)
				print("check_for_rotated_image********", result, "********")
				degree = re.findall(r"Rotate: (\d+)", result)[0]
		except:
				degree = '0'
		print("check_for_rotated_image********", degree, "********")
		img = cv.imread(image_path, 0)

		if degree == '0':
				rotated = img
				#return img
		elif degree == '90':
				rotated = cv.rotate(img, cv.ROTATE_90_CLOCKWISE)
				#return rotated
		elif degree == '270':
				rotated = cv.rotate(img, cv.ROTATE_90_COUNTERCLOCKWISE)
				#return rotated
		elif degree == '180':
				rotated = cv.rotate(img, cv.ROTATE_180)
				#return rotated
	
		cv.imwrite(image_path, rotated)	


def read_scanned_pdf(pdf_path, output_dir_location, erosion_val=0):
		print(f"READ_SCANNED_PDF----{pdf_path}---{erosion_val}")
		try:
				file_name = pdf_path
				doc_dir_location = output_dir_location
				page_dir_location = os.path.join(doc_dir_location, 'pages')
				print("page-->", page_dir_location)
				image_dir_location = os.path.join(doc_dir_location, 'images')
				machined_pdf_location = os.path.join(doc_dir_location, 'pdfs')
				text_dir = os.path.join(doc_dir_location, 'texts')
				stitched_file = os.path.join(page_dir_location, 'stitched.pdf')
				return {'text_file_path': text_dir, 'stitched_pdf_path': stitched_file}

				try:
						shutil.rmtree(page_dir_location)
						shutil.rmtree(image_dir_location)
						shutil.rmtree(machined_pdf_location)
						shutil.rmtree(text_dir)
				except:
						pass
				print("READ_SCANNED_PDF--->11", time.time())
				if doc_dir_location is not None and pdf_path is not None:
						print("READ_SCANNED_PDF--->12", time.time())
						if not os.path.exists(page_dir_location):
								os.makedirs(page_dir_location)
								os.makedirs(image_dir_location)
								os.makedirs(machined_pdf_location)
								os.makedirs(text_dir)

						pdf_split_with_pdfseparate(pdf_path, page_dir_location)
						pages = natsorted(glob.glob(os.path.join(page_dir_location, "*.pdf")))
						for page in pages:
								print(page)
								page_name_without_ext = os.path.basename(page).split('.')[0] + ".jpg"
								image_path = os.path.join(image_dir_location, page_name_without_ext)
								pdf_page_to_image(page, os.path.join(image_dir_location, page_name_without_ext))
								#check_for_rotated_image(image_path)
								#try:
								#		crop_boundary(image_path)
								#except:
								#		pass

								img = cv.imread( image_path, 0 )
								print(f"READ_SCANNED_PDF-1--->", time.time())
								if erosion_val != 0:
										print(f"READ_SCANNED_PDF-2--->EROSION_VAL-->{erosion_val}")
										kernel = np.ones((erosion_val, erosion_val), np.uint8)
										img = cv.erode(img, kernel, iterations=1)
										
								print(f"READ_SCANNED_PDF-2--->", time.time())
								img = cv.medianBlur(img, 5)
								ret, th1 = cv.threshold(img,127,255,cv.THRESH_BINARY)
								#ret, th1 = cv.threshold(img,180,255,cv.THRESH_BINARY)
								cv.imwrite(image_path, th1)
								print(f"READ_SCANNED_PDF-3--->", time.time())

								if is_machine_generated(page):
										print(f"READ_SCANNED_PDF-1.1--->", time.time())
										text_page_name_without_ext = os.path.basename(page).split('.')[0] + ".txt"
										print(f"READ_SCANNED_PDF-1.2--->", time.time())
										convert_pdf_to_text(page, os.path.join(text_dir, text_page_name_without_ext))
										print(f"READ_SCANNED_PDF-1.3--->", time.time())

								else:
										print(f"READ_SCANNED_PDF-2.1--->", time.time())
										images = natsorted(glob.glob(os.path.join(image_dir_location, "*.jpg")))
										print(f"READ_SCANNED_PDF-2.2--->", time.time())
										for image in images:
												print(f"READ_SCANNED_PDF-2.3--->", time.time())
												pdf_page_name_without_ext = os.path.basename(image).split('.')[0] + ".pdf"
												print(f"READ_SCANNED_PDF-2.4--->", time.time())
												make_machined_page_pdf(image, os.path.join(machined_pdf_location, pdf_page_name_without_ext))
												print(f"READ_SCANNED_PDF-2.5--->", time.time())
								print(f"READ_SCANNED_PDF-5--->", time.time())

				stitch_pdfs( page_dir_location )
				machined_pages = natsorted(glob.glob(os.path.join(machined_pdf_location, "*.pdf")))
				scannes_pages = natsorted(glob.glob(os.path.join( page_dir_location, "*.pdf") ))
				stitch_pdfs(machined_pdf_location)
				machined_pages = natsorted(glob.glob(os.path.join(machined_pdf_location, "*.pdf")))
				for mach_page in machined_pages:
						pdf_page_name_without_ext = os.path.basename(mach_page).split('.')[0] + ".txt"
						convert_pdf_to_text(mach_page, os.path.join(text_dir, pdf_page_name_without_ext))
				print('********************************************************')
				return {'text_file_path': text_dir, 'stitched_pdf_path': stitched_file}
		except Exception as e:
				print("Error-->SCANNED_CONTROLLER", e)
				return {'text_file_path': None}

