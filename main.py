import json
import random
from tkinter import *
from tkinter import messagebox
import string


# GENERATE ALGORITHM
def generate_pw():
    pw_entry.delete(0, END)
    lower_letters = list(string.ascii_lowercase)
    upper_letters = list(string.ascii_uppercase)
    specials = list(string.punctuation)
    numbers = [str(char) for char in range(10)]
    pw_list = []

    for i in range(5):
        lower_letter = random.choice(lower_letters)
        pw_list.append(lower_letter)
    for i in range(3):
        upper_letter = random.choice(upper_letters)
        pw_list.append(upper_letter)
    for i in range(3):
        special = random.choice(specials)
        pw_list.append(special)
    for i in range(3):
        number = random.choice(numbers)
        pw_list.append(number)

    random.shuffle(pw_list)
    pw = "".join(pw_list)
    pw_entry.insert(0, pw)


# GUI PART


def search_password():
    web_data = website_entry.get()
    try:
        with open("data.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showwarning(title="Error", message="No data file found.")
    else:
        if web_data in data:
            messagebox.showinfo(title="Data Found.", message=f"e-Mail: {data[web_data]['mail']}"
                                                             f"\nPassword: {data[web_data]['password']}")
        else:
            messagebox.showwarning(title="Error", message=f"There is no data found about '{web_data}'")


def save():
    website = website_entry.get()
    mail = mail_entry.get()
    password = pw_entry.get()

    new_data = {
        website: {
            "mail": mail,
            "password": password
        }
    }

    if len(website) == 0 or len(password) == 0 or len(mail) == 0:
        messagebox.showwarning(title="OOPS", message="Please check the infos you've entered.")

    else:
        should_save = messagebox.askokcancel(title=website, message=f"These are the infos provided by you:"
                                                      f"\nEmail: {mail}"
                                                      f"\nPassword: {password}"
                                                      f"\nis it ready to save?")
        if should_save:
            try:
                with open("data.json", "r") as data_file:
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
            else:
                with open("data.json", "w") as data_file:
                    data.update(new_data)
                    json.dump(data, data_file, indent=4)
    website_entry.delete(0, END)
    pw_entry.delete(0, END)


window = Tk()
window.title("PW Manager")
window.config(pady=50, padx=50, bg="#3e4d6a")

img_scaled = PhotoImage(file="scaled_icon.png")

# Canvas

canvas = Canvas(height=200, width=200, highlightthickness=0, bd=0, bg="#3e4d6a")
canvas.create_image(125, 75, image=img_scaled)
canvas.grid(row=0, column=1)

# Buttons

generate_button = Button(text="Generate Password", command=generate_pw)
generate_button.grid(row=3, column=2)

add_button = Button(text="Add", width=30, command=save)
add_button.grid(row=4, column=1)

search_button = Button(text="Search", width=15, command=search_password)
search_button.grid(row=1, column=2)

# Entries

website = StringVar()
website_entry = Entry(textvariable=website, width=35)
website_entry.grid(row=1, column=1)

mail = StringVar()
mail_entry = Entry(textvariable=mail, width=54)
mail_entry.insert(0, "your_commonly_used_mail@mail.com")
mail_entry.grid(row=2, column=1, columnspan=2)

password = StringVar()
pw_entry = Entry(textvariable=password, width=35)
pw_entry.grid(row=3, column=1)

# Labels

website_label = Label(text="Website:", highlightcolor="white")
website_label.grid(row=1, column=0)

mail_label = Label(text="E-Mail:", highlightcolor="white")
mail_label.grid(row=2, column=0)

pw_label = Label(text="Password:", highlightcolor="white")
pw_label.grid(row=3, column=0)

window.mainloop()
window.destroy()
