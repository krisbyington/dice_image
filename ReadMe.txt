Install python to run

Step 1)
	find an image you want that is .jpg
	Put that image in the “regular images” folder
Step 2) 
	Run dice_image_v2
Step 3) 
	Follow the prompt and give the name of the file
Step 4) 
	The dice Image will be in the dice Image folder 
Step 5) 
	Instructions are easy to read tables of the numbers on the dice so that its easy to use while you build your real dice image

Important limitations: 

1) The max size is 128 by 128 which means the biggest project this can do is 16,384 dice. I hope that this amount
	is pushing the limits of what you would want to do anyway. 

2) I am having a problem with PIL where it will randomly crash and give a permissionError13 
	while making the previews. The best way that I have found to fix it is to just wait 10 min and try again.  

3) The resolution that you input will be adjusted, The tool I am using is supposed to be used to make thumbnails so it favors a ratio of 4:3 and 3:2 in terms of (width : Height)
