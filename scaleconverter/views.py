from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import math

from scaleconverter.forms import ScaleConverterForm

# Create your views here.

def scale_app(request):
	print("FORM")
	out = {}
	if request.method == 'POST':

		scale_form = ScaleConverterForm(request.POST)
		try:
			if scale_form.is_valid():

				print("IS VALID")

				in_view_scale = scale_form.cleaned_data['view_scale']
				in_original_drawing_size = scale_form.cleaned_data['original_drawing_size']
				in_printed_drawing_size = scale_form.cleaned_data['printed_drawing_size']

				# print(in_view_scale)
				# print(in_original_drawing_size)
				# print(in_printed_drawing_size)

				drawing_size_list = ["","A5","A4","A3","A2","A1","A0"]

				difference = drawing_size_list.index(in_original_drawing_size) - drawing_size_list.index(in_printed_drawing_size)
				square_root = math.sqrt(2)

				power = square_root ** difference

				ratio = int(in_view_scale) * power

				new_ratio = str(ratio).split(".")[0]

				export_string = "ORIGINAL SCALE 1:" + str(in_view_scale) + " @ " + str(in_original_drawing_size) + " | NEW SCALE" + " 1:" + str(new_ratio) + " @ " + str(in_printed_drawing_size)

				print(export_string)

				out["original_scale"] = str(in_view_scale)
				out["original_paper"] = str(in_original_drawing_size)
				out["new_scale"] = str(new_ratio)
				out["new_paper"] = str(in_printed_drawing_size)

				return render(request, 'scaleconverter/form.html', {"form": scale_form,"out": out})
				# return JsonResponse({"working": out})

			else:
				return JsonResponse({"working": "False"})
		except Exception as e:
			return JsonResponse({"working": e})
	else:
		scaleForm = ScaleConverterForm()
	return render(request, 'scaleconverter/form.html', {"form": scaleForm})