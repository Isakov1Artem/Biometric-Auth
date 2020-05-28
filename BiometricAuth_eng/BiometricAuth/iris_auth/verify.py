##-----------------------------------------------------------------------------
##  Import
##-----------------------------------------------------------------------------
import argparse
from time import time

from .fnc.extractFeature import extractFeature
from .fnc.matching import matching


# #------------------------------------------------------------------------------
# #	Argument parsing
# #------------------------------------------------------------------------------
# parser = argparse.ArgumentParser()

# parser.add_argument("--file", type=str,
#                     help="Path to the file that you want to verify.")

# parser.add_argument("--temp_dir", type=str, default="../Saved",
# 					help="Path to the directory containing templates.")

# parser.add_argument("--thres", type=float, default=0.38,
# 					help="Threshold for matching.")

# #My
# # parser.add_argument("--id", type=int,
# # 					help="Id of user")

# args = parser.parse_args()


# ##-----------------------------------------------------------------------------
# ##  Execution
# ##-----------------------------------------------------------------------------
# # Extract feature
# start = time()
# print('>>> Start verifying {}\n'.format(args.file))
# template, mask, file = extractFeature(args.file)
# # print(template)

# # Matching
# result = matching(template, mask, args.temp_dir, args.thres)

# if result == -1:
# 	print('>>> No registered sample.')

# elif result == 0:
# 	print('>>> No sample matched.')

# else:
# 	print('>>> {} samples matched (descending reliability):'.format(len(result)))
# 	for res in result:
# 		print("\t", res)


# # Time measure
# end = time()
# print('\n>>> Verification time: {} [s]\n'.format(end - start))

def verify(file_path):
	template, mask, file = extractFeature(file_path)
	# Matching
	result = matching(template, mask, args.temp_dir, args.thres)
	if result == -1:
		print('>>> No registered sample.')

	elif result == 0:
		print('>>> No sample matched.')

	else:
		print('>>> {} samples matched (descending reliability):'.format(len(result)))
		for res in result:
			print("\t", res)