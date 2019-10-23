from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

import re

from listcompare.forms import ListCheckerForm

# Create your views here.

def check_list_difference(listA, listB):
	return list(set(listA) - set(listB))

def check_list_intersection(listA, listB):
	return list(set(listA) & set(listB))

def splitListToItems(inputList, listToAppend):
    clean_list = inputList.split(",")
    all_items = [x for x in clean_list if x]
    for i in all_items:
        x = i.replace("\r\n", "")
        x = i.strip()
        # x = x.replace("K:", prefix)
        listToAppend.append(x)
    return listToAppend

def compare_list(request):
	print("FORM")

	if request.method == 'POST':
		listForm = ListCheckerForm(request.POST)

		if listForm.is_valid():
			clean_listA = listForm.cleaned_data['listA'].strip()
			clean_listB = listForm.cleaned_data['listB'].strip()

			multiline_list_A = []
			multiline_list_B = []

			multiline_input_A = listForm.cleaned_data['listA']
			multiline_input_B = listForm.cleaned_data['listB']

			multiline_list_A.append(multiline_input_A)
			multiline_list_B.append(multiline_input_B)


			string_A = multiline_list_A[0]
			string_B = multiline_list_B[0]

			multiline_array_A = re.findall(r"\S+", string_A)
			multiline_array_B = re.findall(r"\S+", string_B)

			# multiline_array_A = multiline_list_A[0].split("\r\n")
			# multiline_array_B = multiline_list_B[0].split("\r\n")

			# print(multiline_array_A)
			# print(multiline_array_B)

			obj_A = {}
			obj_A["list_length"] = str(len(multiline_array_A))
			obj_A["u_list_length"] = len(list(set(multiline_array_A)))

			obj_B = {}
			obj_B["list_length"] = len(multiline_array_B)
			obj_B["u_list_length"] = len(list(set(multiline_array_B)))

			unique_set = list(set(multiline_array_A + multiline_array_B))

			out = {}

			try:

				seen_A = {}
				dupes_A = []

				for x in multiline_array_A:
					if x not in seen_A:
						seen_A[x] = 1
					else:
						if seen_A[x] == 1:
							dupes_A.append(x)
						seen_A[x] += 1

				seen_B = {}
				dupes_B = []

				for x in multiline_array_B:
					if x not in seen_B:
						seen_B[x] = 1
					else:
						if seen_B[x] == 1:
							dupes_B.append(x)
						seen_B[x] += 1

				just_A = check_list_difference(multiline_array_A, multiline_array_B)
				just_B = check_list_difference(multiline_array_B, multiline_array_A)
				int_AB = check_list_intersection(multiline_array_A, multiline_array_B)

				just_A.sort()
				just_B.sort()
				int_AB.sort()
				dupes_A.sort()
				dupes_B.sort()
				unique_set.sort()			

				separator = "\n"
				multi_A = separator.join(just_A)
				multi_B = separator.join(just_B)
				multi_AB = separator.join(int_AB)
				multi_Dup_A = separator.join(dupes_A)
				multi_Dup_B = separator.join(dupes_B)
				multi_Set_AB = separator.join(unique_set)

				out["A_Only"] = multi_A
				out["B_Only"] = multi_B
				out["A_B"] = multi_AB
				out["Dup_A"] = multi_Dup_A
				out["Dup_B"] = multi_Dup_B
				out["Set_AB"] = multi_Set_AB
				out["Stats_A"] = obj_A
				out["Stats_B"] = obj_B

				return render(request, "listcompare/form.html", {"form": listForm, "out": out})

			except Exception as e:
				print(e)

			# print(list_A)
			# print(list_B)

	else:
		listForm = ListCheckerForm()
	return render(request, "listcompare/form.html", {"form": listForm})