from tkinter import *
import random

window = Tk()
window.title("Sorting Visualizer")
worker = None
speed = 10

def swap(pos_0, pos_1):
	bar11, _, bar12, _ = myCanvas.coords(pos_0)
	bar21, _, bar22, _ = myCanvas.coords(pos_1)

	myCanvas.move(pos_0, bar21-bar11, 0)
	myCanvas.move(pos_1, bar12-bar22, 0)

def _bubble_sort():
	for i in range(len(bar_length) - 1):
		for j in range(len(bar_length) - i - 1):
			if(bar_length[j] > bar_length[j + 1]):
				bar_length[j] , bar_length[j + 1] = bar_length[j + 1] , bar_length[j] # change length
				bar_list[j], bar_list[j + 1] = bar_list[j + 1] , bar_list[j] # chaneg list
				swap(bar_list[j + 1] , bar_list[j])
				yield

def _insertion_sort():
	for i in range(len(bar_length)):
		cursor = bar_length[i]
		cursorBar = bar_list[i]
		pos = i

		while pos > 0 and bar_length[pos - 1] > cursor:
			bar_length[pos] = bar_length[pos - 1]
			bar_list[pos], bar_list[pos - 1] = bar_list[pos - 1], bar_list[pos]
			swap(bar_list[pos],bar_list[pos-1])   
			yield                                      
			pos -= 1                                   

		bar_length[pos] = cursor
		bar_list[pos] = cursorBar
		swap(bar_list[pos],cursorBar)

def _selection_sort():
	for i in range(len(bar_length)):
		min = i
		for j in range(i + 1 ,len(bar_length)):
			if(bar_length[j] < bar_length[min]):
				min = j
		bar_length[min], bar_length[i] = bar_length[i] ,bar_length[min]
		bar_list[min] , bar_list[i] = bar_list[i] , bar_list[min]
		swap(bar_list[min] , bar_list[i])
		yield

def shuffle():
	global bar_list
	global bar_length
	myCanvas.delete('all')
	barstart = 10
	barend = 30
	bar_list = []
	bar_length = []
	s = 22
	e = 22
	min_color = '#db3236'
	max_color = '#f4c20d'

	number_of_box = box_slider.get()

	if number_of_box > 30:
		s = e = 12
		barstart = 10
		barend = 20
	if number_of_box > 50:
		s = e = 8
		barstart = 10
		barend = 18
	if number_of_box > 75:
		s = e = 7
		barstart = 3
		barend = 8

	for _ in range(number_of_box):
		randomY = random.randrange(10, 300)
		bar = myCanvas.create_rectangle(barstart, 500, barend, randomY, fill='#5c6e91', outline='#EBEDEF')
		bar_list.append(bar)
		barstart += s
		barend += e

	for b in bar_list:
		pos = myCanvas.coords(b)
		length = pos[3] - pos[1]
		bar_length.append(length)

	# Minimum is colored in red
	# Maximum is colored in green
	for i in bar_length:
		if i == min(bar_length):
			myCanvas.itemconfig(bar_list[bar_length.index(i)], fill=min_color)
		if i == max(bar_length):
			myCanvas.itemconfig(bar_list[bar_length.index(i)], fill=max_color)

	myCanvas.create_rectangle(8, 8, 16, 16, fill=min_color)
	myCanvas.create_text(55, 12, fill='black', text="- minimum", font='10')
	myCanvas.create_rectangle(8, 18, 16, 26, fill=max_color)
	myCanvas.create_text(55, 22, fill='black', text="- maximum", font='10')

def getThrottle(e):
	shuffle()
	val = box_slider.get()
	box_label = Label(frame, text=f"Size:   {val}", pady=10,bg='#fafafa').grid(row=3, column=0)

def getSpeed(e):
	global speed
	val = speed_slider.get()
	speed = val
	speed_label = Label(frame, text=f"Delay:    {val} ms",pady=10,bg='#fafafa').grid(row=4, column=0)

def sort():
	textCanvas.delete('all')
	algo_name = name.get()
	textCanvas.create_text(100, 20, fill='black', text=algo_name, font='sanserif 14')
	textCanvas.create_text(100, 50, fill='#333333', text="(Time Complexity)")
	textCanvas.create_text(100, 150, fill='#333333', text="(Space Complexity)")
	textCanvas.create_line(20, 135, 180, 135, fill='grey')
	
	if algo_name == 'Bubble sort' or algo_name == 'Insertion sort':
		l = ["O(n)", "O(n^2)", "O(n^2)", "O(1)"]
	if algo_name == 'Selection sort':
		l = ["O(n^2)", "O(n^2)", "O(n^2)", "O(1)"]

	textCanvas.create_text(100, 80, fill='green',  text="Best Case: " + l[0], font='14')
	textCanvas.create_text(100, 100, fill='orange', text="Average Case: " + l[1], font='14')
	textCanvas.create_text(100, 120, fill='red', text="Worst Case: " + l[2], font='14')
	textCanvas.create_text(100, 180, fill='red', text="Worst Case: " + l[3], font='14')

	if algo_name == 'Bubble sort':
		global worker
		worker = _bubble_sort()
		animate()
	if algo_name == 'Insertion sort':
		worker = _insertion_sort()
		animate()
	if algo_name == 'Selection sort':
		worker = _selection_sort()
		animate()

def animate():
	global worker
	if worker is not None:
		try:
			next(worker)
			window.after(speed, animate)
		except StopIteration:            
			worker = None
		finally:
			window.after_cancel(animate)


frame = LabelFrame(window, text="Control", pady=20, bg='#fafafa')
frame.grid(row=0, column=0, pady=5, padx=5)

name = StringVar()
name.set("Bubble sort")
select_sort = Label(frame, text="Algorithms:", padx=10,bg='#fafafa').grid(row=1, column=0,)
drop = OptionMenu(frame, name, "Bubble sort", "Insertion sort", "Selection sort")
drop.grid(row=2, column=0, padx=10)


box_label = Label(frame, text="Size:   5 ", pady=20,bg='#fafafa').grid(row=3, column=0)
box_slider = Scale(frame, from_=5, to=100, orient=HORIZONTAL, command=getThrottle, showvalue=0)
box_slider.grid(row=3, column=1)


speed_label = Label(frame, text="Delay:    10 ms",pady=20,bg='#fafafa').grid(row=4, column=0)
speed_slider = Scale(frame, from_=10, to=100, orient=HORIZONTAL, showvalue=0, command=getSpeed)
speed_slider.grid(row=4, column=1)

shuffle_label = Label(frame, text="Click to shuffle :", pady=10,bg='#fafafa').grid(row=5, column=0)
shuffle_button = Button(frame, text="Shuffle",padx=2, pady=4, command=shuffle)
shuffle_button.grid(row=5, column=1)

sort_button = Button(frame, text="Sort",padx=2, pady=4, width=10 , command=sort)
sort_button.grid(row=6, column=1, pady=20)


textCanvas = Canvas(frame, width=200, height=200)
textCanvas.grid(row=7, column=0, columnspan=3, padx=20)

myCanvas = Canvas(window, width=700, height=500, bg='#EBEDEF')
myCanvas.grid(row=0, column=1, padx=10, pady=10)



shuffle()
window.mainloop()

