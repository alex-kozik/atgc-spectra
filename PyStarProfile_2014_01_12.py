#!/usr/bin/python

########################
#    COPYRIGHT  2014   #
#    Alexander Kozik   #
########################

def Image_Profile(in_name, out_name, pix_scale, zero_beam_pos, color_mode, im_title):

	print in_name
	print out_name
	print pix_scale
	print im_title
	
	rgb_array = {}
	bw_array  = {}
	
	# MAX PROFILE VALUE #
	max_bw = 0
	# luminance #
	r_lum = 0.2126
	g_lum = 0.7152
	b_lum = 0.0722
	# SKIP THIS NUMBER OF PIXELS TO CALCULATE MAX PROFILE VALUE #
	offset_zero_beam = 250
	
	# SIZE OF OUTPUT PNG IMAGE #
	png_image_height = 800
	png_graph_height = 600
	
	# OUTPUT FILES #
	out_file1 = open(out_name + '.Profile.tab' , "wb")
	png_name = out_name + '.Profile.png'
	
	# OPEN INPUT IMAGE/SPECTRUM #
	im = Image.open(in_name)
	
	# CONVERT INTO GRAY SCALE #
	gs = im.convert('L')
	width, height = im.size
	print in_name, width, height
	
	#######################
	###   COLOR IMAGE   ###
	if color_mode == "RGB":
		out_file1.write('Pixel' + '\t' + 'Blue' + '\t' + 'Green' + '\t' + 'Red' + '\t' + '***' + '\t' + 'BGR' + '\t' + 'BGR_Norm' + '\t' + '***' + '\t' + 'Coord' + '\t' + 'Angstrom' + '\t' + 'BW' + '\t' + 'BW_Norm' + '\n')
		n = 0
		# IMAGE COLUMNs #
		while n < width:
			m = 0
			r_sum = 0
			g_sum = 0
			b_sum = 0
			bw_sum = 0
			norm_coord = n - zero_beam_pos
			angstrom_v = round(norm_coord*pix_scale,2)
			# FOR EACH IMAGE COLUMN CALCULATE PIXEL VALUES #
			while m < height: 
				# COLOR VALUES #
				current_pixel = im.getpixel((n, m))
				# GRAY SCALE VALUE #
				current_pixel_gs = gs.getpixel((n, m))
				# luminance is calculated as a weighted sum of the three linear-intensity values #
				r = current_pixel[0]*r_lum
				g = current_pixel[1]*g_lum
				b = current_pixel[2]*b_lum
				bw = current_pixel_gs
				r_sum = round((r_sum + r),2)
				g_sum = round((g_sum + g),2)
				b_sum = round((b_sum + b),2)
				bw_sum = bw_sum + bw
				# END OF COLUMN - SUMMARIZE DATA #
				if m == height - 1:
					rgb_sum = round((r_sum + g_sum + b_sum),2)
					rgb_norm = float(rgb_sum)/height
					rgb_int = round(rgb_norm,2)
					rgb_array[n] = rgb_int
					bw_norm = float(bw_sum)/height
					bw_int = round(bw_norm,2)
					# ARRAY WITH GRAY SCALE VALUES #
					bw_array[n] = bw_int
					# MAX PROFILE VALUE #
					if bw_int >= max_bw and n >= offset_zero_beam:
						max_bw = bw_int
					print `n` + '\t' + `b_sum` + '\t' + `g_sum` + '\t' + `r_sum` + '\t' + "***" + '\t' + `rgb_sum` + '\t' + `rgb_int` + '\t' + "***" + '\t' + `norm_coord` + '\t' + `angstrom_v` + '\t' + `bw_sum` + '\t' + `bw_int`
					# WRITE DATA SUMMARY TO TEXT FILE #
					out_file1.write(`n` + '\t' + `b_sum` + '\t' + `g_sum` + '\t' + `r_sum` + '\t' + "***" + '\t' + `rgb_sum` + '\t' + `rgb_int` + '\t' + "***" + '\t' + `norm_coord` + '\t' + `angstrom_v` + '\t' + `bw_sum` + '\t' + `bw_int`)
					out_file1.write('\n')
				m = m + 1
			n = n + 1 
	
	############################
	###   GRAY SCALE IMAGE   ###
	if color_mode == "BW":
		out_file1.write('Pixel' + '\t' + "***" + '\t' + 'Coord' + '\t' + 'Angstrom' + '\t' + 'BW' + '\t' + 'BW_Norm' + '\n')
		n = 0
		# IMAGE COLUMNs #
		while n < width:
			m = 0
			bw_sum = 0
			norm_coord = n - zero_beam_pos
			angstrom_v = round(norm_coord*pix_scale,2)
			# FOR EACH IMAGE COLUMN CALCULATE PIXEL VALUES #
			while m < height: 
				current_pixel = im.getpixel((n, m))
				bw = current_pixel
				bw_sum = bw_sum + bw
				# END OF COLUMN - SUMMARIZE DATA #
				if m == height - 1:
					bw_norm = float(bw_sum)/height
					bw_int = round(bw_norm,2)
					# ARRAY WITH GRAY SCALE VALUES #
					bw_array[n] = bw_int
					# MAX PROFILE VALUE #
					if bw_int >= max_bw and n >= offset_zero_beam:
						max_bw = bw_int
					print `n` + '\t' + "***" + '\t' + `norm_coord` + '\t' + `angstrom_v` + '\t' + `bw_sum` + '\t' + `bw_int`
					# WRITE DATA SUMMARY TO TEXT FILE #
					out_file1.write(`n` + '\t' + "***" + '\t' + `norm_coord` + '\t' + `angstrom_v` + '\t' + `bw_sum` + '\t' + `bw_int`)
					out_file1.write('\n')
				m = m + 1
			n = n + 1 
	
	###############################
	###        DRAW IMAGE       ###
	font = ImageFont.load_default()
	png_height = png_image_height
	png_graph = Image.new("RGB", (width, png_height), (0, 24, 48))
	draw_png = ImageDraw.Draw(png_graph)
	
	###############################################
	# ADJUST PROFILE VALUES TO FIT INTO PNG IMAGE #
	correction_coef = (png_graph_height-50)/max_bw
	print correction_coef
	
	######################################
	# PLOT PROFILE VALUES INTO PNG IMAGE #
	k = 0
	while k < width:
		x = k
		y = bw_array[k]*correction_coef
		# ZERO-BEAM IN 10x SCALE #
		if k <= offset_zero_beam:
			y_scaled = y/10
			y_scaled = png_graph_height - y_scaled
			draw_png.rectangle([x,y_scaled,x+1,y_scaled+1],fill=(255,0,0),outline=(255,0,0))
		# MAIN GRAPH IN NORMAL SCALE #
		y = png_graph_height - y
		draw_png.rectangle([x,y,x+1,y+1],fill=(255,255,0),outline=(255,255,0))
		k = k + 1
	
	##################################
	# PRINT INFO LABELS ON PNG GRAPH #
	draw_png.text([400,160],fill=(255,255,255),text=(im_title),font=font)
	draw_png.text([400,200],fill=(255,255,255),text=('Max_Value='),font=font)
	draw_png.text([480,200],fill=(255,255,255),text=(`max_bw`),font=font)
	draw_png.text([400,240],fill=(255,255,255),text=('Pix_Scale='),font=font)
	draw_png.text([480,240],fill=(255,255,255),text=(`pix_scale`),font=font)
	draw_png.text([400,280],fill=(255,255,255),text=('Zero_Beam='),font=font)
	draw_png.text([480,280],fill=(255,255,255),text=(`zero_beam_pos`),font=font)
	draw_png.text([400,320],fill=(255,255,255),text=('File_Name='),font=font)
	draw_png.text([480,320],fill=(255,255,255),text=(in_name),font=font)
	
	####################################################
	# COPY-PASTE ORIGINAL RESIZED IMAGE INTO PNG GRAPH #
	offset = (0,650)
	mini = im.resize((width,100),Image.ANTIALIAS)
	png_graph.paste(mini,offset)
	
	###########################
	# PRINT PIXEL COORDINATES #
	p = 0
	while p < width:
		tick_update1 = math.fmod(p-zero_beam_pos,100)
		tick_update2 = math.fmod(p-zero_beam_pos,500)
		if tick_update1 == 0:
			draw_png.rectangle([p,775,p+1,780],fill=(255,255,255),outline=(255,255,255))
		if tick_update2 == 0:
			draw_png.rectangle([p,775,p+1,790],fill=(255,255,255),outline=(255,255,255))
			draw_png.text([p,760],fill=(255,255,255),text=(`p-zero_beam_pos`),font=font)
		p = p + 1
	
	##############################
	# PRINT ANGSTROM COORDINATES #
	a = 0
	while a < 10000:
		tick_update3 = math.fmod(a, 100)
		tick_update4 = math.fmod(a, 500)
		tick_update5 = math.fmod(a,1000)
		x = zero_beam_pos+(float(a)/pix_scale)
		if tick_update3 == 0:
			draw_png.rectangle([x,625,x+1,630],fill=(255,255,255),outline=(255,255,255))
		if tick_update4 == 0:
			draw_png.rectangle([x,625,x+1,640],fill=(255,255,255),outline=(255,255,255))
		if tick_update5 == 0:
			draw_png.rectangle([x,625,x+1,645],fill=(255,255,255),outline=(255,255,255))
			draw_png.text([x,610],fill=(255,255,255),text=(`a`),font=font)
		a = a + 1
	
	#################################
	# PRINT SELECTED SPECTRAL LINES #
	
	# H-Alpha 6563
	x = 6563.0/pix_scale + zero_beam_pos
	draw_png.rectangle([x,100,x,600],fill=(128,128,128),outline=(128,128,128))
	# H-Beta  4861
	x = 4861.0/pix_scale + zero_beam_pos
	draw_png.rectangle([x,100,x,600],fill=(128,128,128),outline=(128,128,128))
	# H-Gamma 4341
	x = 4341.0/pix_scale + zero_beam_pos
	draw_png.rectangle([x,100,x,600],fill=(128,128,128),outline=(128,128,128))
	
	##########################################
	#           SAVE PNG IMAGE FILE          #
	png_graph.save(png_name, png_graph.format)
	#         CLOSE OUTPUT TEXT FILE         #
	out_file1.close()
	
	
import sys
import math
import string
import Image
import ImageDraw
import ImageFont
import ImageFilter
if __name__ == "__main__":
	if len(sys.argv) <= 6 or len(sys.argv) > 7:
		print "Program usage: "
		print "[input_file] [output_file] [Pixel_to_Angstrom_Scale] [Zero_Beam_Pos] [Color_Mode] [Image_Title]"
		print "Script generates stellar spectral profile from image file"
		exit
	if len(sys.argv) == 7:
		in_name   = sys.argv[1]
		out_name  = sys.argv[2]
		pix_scale = float(sys.argv[3])
		zero_beam_pos = int(sys.argv[4])
		color_mode = sys.argv[5]
		im_title  = sys.argv[6]
		
		if in_name != out_name:
			Image_Profile(in_name, out_name, pix_scale, zero_beam_pos, color_mode, im_title)
		else:
			print "Output should have different name than Input"
			exit
		########################################################