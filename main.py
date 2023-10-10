# Refer "libraries_needed.txt" to download all the necessary libraries.
# Add a valid directory path at line 85

import nltk

nltk.download('stopwords')

from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from PIL import Image, ImageTk
from tkPDFViewer import tkPDFViewer as Pdf

from resume_reader import ResumeReader

FONT = ("Ariel", 20, "bold")
BTN_FONT = ("Ariel", 12, "normal")
BACKGROUND_COLOR = "#EEF2FF"
PRIMARY_BTN = "#1C658C"
SECONDARY_BTN = "#398AB9"
FONT_FG = "#2C3333"

keyword_file = ""
domain = ""
selected_pdfs = []
domain_based_resumes = []
resume_objects = []


# ----------------------------------------- TOOLS (BACK-END) -----------------------------------------
# --------- SET SORTING KEYWORDS ---------
def tech():
    global keyword_file, domain
    keyword_file = "tech_skills.txt"
    domain = "Technology"
    select_files()


def hr():
    global keyword_file, domain
    keyword_file = "hr_skills.txt"
    domain = "Human Resources"
    select_files()


def acc():
    global keyword_file, domain
    keyword_file = "accounting_skills.txt"
    domain = "Accounting"
    select_files()


def mkt():
    global keyword_file, domain
    keyword_file = "marketing_skills.txt"
    domain = "Marketing"
    select_files()


# --------- SORT & CREATE RESUME OBJECTS ---------
def sort_resumes():
    global resume_objects
    for resume in selected_pdfs:
        resume_object = ResumeReader(resume, keyword_file)
        resume_objects.append(resume_object)


# --------- DOMAIN BASED RESUMES ---------
def sort_domain_based():
    global domain_based_resumes
    domain_based_resumes = []
    for res in resume_objects:
        if res.no_of_skills != 0:
            domain_based_resumes.append(res)
        else:
            continue
    # print(len(domain_based_resumes))
    # for i in domain_based_resumes:
    #     # print(i.name)


# --------- CHOOSE FILES ---------
def select_files():
    global selected_pdfs
    loading_window.pack()
    main_window.pack_forget()
    window.filename = filedialog.askopenfilenames(initialdir=r"C:\enter\your\path", title="Select resumes",
                                                  filetypes=(("pdf files", "*.pdf"), ("all files", "*.*")))
    selected_pdfs = list(window.filename)
    if not selected_pdfs:
        loading_window.pack_forget()
        main_window.pack()
        messagebox.showerror(title="No resume selected", message="Please select at least one resume to proceed")
    else:
        sorting_resume_load_screen()


# --------- GO BACK TO SORTED RESUME WINDOW ---------
def back_to_main():
    global selected_pdfs, domain_based_resumes, resume_objects
    selected_pdfs = []
    domain_based_resumes = []
    resume_objects = []
    results.pack_forget()
    main_window.pack()

    for widget in results.winfo_children():
        widget.destroy()


# --------- OPEN PDF ---------
def view_pdf(path):
    pdf_window = Toplevel(window)
    pdf_window.geometry("650x600")
    pdf_window.title("PDF viewer")
    make_pdf = Pdf.ShowPdf()
    make_pdf.img_object_li.clear()
    place_pdf = make_pdf.pdf_view(pdf_window, pdf_location=path, width=75, height=35)
    place_pdf.config()
    place_pdf.grid(row=0, column=0)


# --------- JUMP TO FRAME [2] (LOADING WINDOW) ---------
def sorting_resume_load_screen():
    sort_resumes()
    loading_window.pack_forget()
    sort_domain_based()
    view_sorted_resumes()


# --------- JUMP TO FRAME [3] (VIEW SORTED RESUMES) ---------
def view_sorted_resumes():
    results.pack()

    results_head = Label(results, text=f"Resumes sorted according to {domain} domain.\n\n",
                         bg=BACKGROUND_COLOR, font=("times new roman", 22, "bold"), fg=FONT_FG)
    results_head.grid(row=0, column=0, padx=20)

    back = Button(results, text="Back", command=back_to_main, bg=SECONDARY_BTN, fg="white", width=15,
                  font=BTN_FONT)
    back.grid(row=0, column=1)

    button_list = []
    for obj in domain_based_resumes:
        def get_file_loc(res_obj=obj):
            view_pdf(res_obj.pdf_path)

        button_list.append(Button(results, text=obj.name, bg=SECONDARY_BTN, fg="white", font=BTN_FONT, width=15,
                                  command=get_file_loc))
        button_list[domain_based_resumes.index(obj)].grid(row=domain_based_resumes.index(obj) + 1, column=0, pady=15)


# ----------------------------------------- UI SETUP (FRONT-END) -----------------------------------------
# --------- ROOT ---------
window = Tk()
window.title("Resume Parser")
window.config(padx=30, pady=30, bg=BACKGROUND_COLOR)
window.geometry("1100x800")
window.geometry("+100+0")
window.iconbitmap("logo.ico")
image = Image.open("sorting_process.png")
resize_image = image.resize((400, 400))
window.state("zoomed")

# --------- FRAMES ---------
main_window = Frame(window, bg=BACKGROUND_COLOR)  # F1
loading_window = Frame(window, bg=BACKGROUND_COLOR)  # F2
results = Frame(window, bg=BACKGROUND_COLOR)  # F3
# pdf_window = Frame(window, bg=BACKGROUND_COLOR)  # F4

# --------- FRAME [1] (MAIN WINDOW) ---------
# [1] LOGO
canvas = Canvas(main_window, width=600, height=500, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.pack()
img = ImageTk.PhotoImage(resize_image)
canvas.create_image(200, 350, image=img)
canvas.grid(row=0, column=0, rowspan=3)

# [1] LABELS
# welcome_screen_head = Label(main_window, text="Hire-me!", bg=BACKGROUND_COLOR,
#                             font=("times new roman", 22, "bold"), fg=FONT_FG)
# welcome_screen_head.grid(row=1, column=0, columnspan=2)

# welcome_screen_slogan = Label(main_window, text="A powerful resume parser.", bg=BACKGROUND_COLOR,
#                               font=FONT, fg=FONT_FG)
# welcome_screen_slogan.grid(row=2, column=0, columnspan=2)

welcome_screen_start = Label(main_window, text="Choose a domain:",
                             bg=BACKGROUND_COLOR, font=FONT, fg=FONT_FG, anchor=S, height=9)
welcome_screen_start.grid(row=0, column=1, columnspan=2)

# [1] BUTTONS
tech_sort = Button(main_window, text="Technology", command=tech, bg=SECONDARY_BTN, fg="white", width=15,
                   font=BTN_FONT)
tech_sort.grid(row=1, column=1, padx=10)

hr_sort = Button(main_window, text="Human Resources", command=hr, bg=SECONDARY_BTN, fg="white", width=15,
                 font=BTN_FONT)
hr_sort.grid(row=1, column=2, padx=10)

acc_sort = Button(main_window, text="Accounting", command=acc, bg=SECONDARY_BTN, fg="white", width=15,
                  font=BTN_FONT)
acc_sort.grid(row=2, column=1)

mkt_sort = Button(main_window, text="Marketing", command=mkt, bg=SECONDARY_BTN, fg="white", width=15,
                  font=BTN_FONT)
mkt_sort.grid(row=2, column=2)

# --------- FRAME [2] (LOADING WINDOW) ---------
loading = Label(loading_window, text="Sorting selected resumes. Please wait...",
                bg=BACKGROUND_COLOR, font=("times new roman", 22, "bold"), fg=FONT_FG)
loading.grid(row=0, column=0, pady=300)

main_window.pack()
window.mainloop()

acc_sort.grid(row=5, column=0)

mkt_sort = Button(main_window, text="Marketing", command=mkt, bg=SECONDARY_BTN, fg="white", width=15,
                  font=BTN_FONT)
mkt_sort.grid(row=5, column=1, pady=20)

# --------- FRAME [2] (LOADING WINDOW) ---------
loading = Label(loading_window, text="Sorting selected resumes. Please wait...",
                bg=BACKGROUND_COLOR, font=("times new roman", 22, "bold"), fg=FONT_FG, wraplength=490)
loading.grid(row=0, column=0, pady=180)

main_window.pack()
window.mainloop()
